const {chromium}=require('playwright');const {spawn,execFileSync}=require('child_process');
(async()=>{const [,,out,arg]=process.argv;
const b=await chromium.launch({args:['--allow-file-access-from-files','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+process.cwd()+'/main.html');
await p.evaluate(()=>document.fonts.ready);await p.waitForFunction(()=>window.ready&&window.ready(),{timeout:180000});
await p.evaluate(()=>Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>i.onload=i.onerror=r))));
if(out==='stills'){for(const t of arg.split(',')){await p.evaluate(t=>frame(t),+t);await p.screenshot({path:`ov_${t}.png`,omitBackground:true});
 execFileSync('ffmpeg',['-loglevel','error','-y','-ss',t,'-i','bg.mp4','-i',`ov_${t}.png`,'-filter_complex','[0][1]overlay','-frames:v','1',`st_${t}.png`]);}await b.close();return;}
const FPS=30,DUR=+arg;
const ff=spawn('ffmpeg',['-y','-loglevel','error','-i','bg.mp4','-f','image2pipe','-framerate',String(FPS),'-c:v','png','-i','-','-i','mix.wav','-filter_complex','[0:v][1:v]overlay=format=auto,format=yuv420p[v]','-map','[v]','-map','2:a','-c:v','libx264','-crf','16','-preset','medium','-c:a','aac','-b:a','192k','-t',String(DUR),'-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
for(let i=0;i<FPS*DUR;i++){await p.evaluate(t=>frame(t),i/FPS);const buf=await p.screenshot({type:'png',omitBackground:true});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();})();

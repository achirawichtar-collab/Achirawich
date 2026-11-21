// Renders clip3.html as transparent PNG frames and composites them over bg.mp4 with mix.wav.
// usage: node render3.js out.mp4 DUR   |  node render3.js stills t1,t2,...
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const path = require('path');
const [,, out, arg] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(__dirname, 'kok.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => i.onload = i.onerror = r))));
  if (out === 'stills') {
    for (const t of arg.split(',')) {
      await p.evaluate(t => frame(t), +t);
      await p.screenshot({ path: `ov_${t}.png`, omitBackground: true });
      execFileSync('ffmpeg', ['-loglevel','error','-y','-ss', t, '-i', 'bg.mp4', '-i', `ov_${t}.png`, '-filter_complex', '[0][1]overlay', '-frames:v', '1', `still3_${t}.png`]);
    }
    await b.close(); return;
  }
  const FPS = 30, DUR = +arg;
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-i', 'bg.mp4', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-', '-i', 'mix.wav',
    '-filter_complex', '[0:v][1:v]overlay=format=auto,format=yuv420p[v]', '-map', '[v]', '-map', '2:a',
    '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-t', String(DUR), '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < FPS * DUR; i++) {
    await p.evaluate(t => frame(t), i / FPS);
    const buf = await p.screenshot({ type: 'png', omitBackground: true });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
})();

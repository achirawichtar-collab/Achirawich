import json, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); DL = f'{D}/dl'; V = f'{D}/v2'
LEAD = 0.1; PAD = 0.12; MINS = 1.05; TEMPO = 1.0
dur = lambda f: float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
WAT = '../vid/dl/mk_45604.mp4'
DARK = 'gblur=sigma=28,eq=brightness=-0.22:saturation=0.8'
# shot: (voice-file or None, caption, bg file, seek, filter)
SH = [
 ('h1','อย่าเพิ่งซื้อเครื่องทำน้ำอุ่น ถ้ายังไม่ดูคลิปนี้!', 'px_9166291.mp4',1,'eq=contrast=1.08'),
 ('h2','เพราะถ้าเลือกผิด…', 'px_6658288.mp4',2,"crop=iw*0.9:ih*0.9:x='iw*0.05+iw*0.015*sin(t*29)':y='ih*0.05+ih*0.01*sin(t*41)',colorbalance=bs=.15:rs=-.08"),
 ('l3','น้ำไม่อุ่น', 'px_5980103.mp4',1,'colorbalance=bs=.25:bm=.15:rs=-.15:rm=-.08'),
 ('l4','ไฟตก', 'px_853772.mp4',1,"eq=eval=frame:brightness='-0.4*gt(sin(t*23),0.5)'"),
 ('l5','แถมไม่ปลอดภัย', 'px_9665450.mp4',1,'eq=contrast=1.1:saturation=1.2'),
 ('l6','ดูแค่ 3 ข้อนี้พอ', 'px_35495443.mp4',1,'gblur=sigma=6,eq=brightness=-0.08'),
 ('s07','ข้อแรก วัตต์', 'px_28886877.mp4',1,'eq=saturation=1.1'),
 ('s08','3500W เหมาะกับอยู่คนเดียว', 'px_19919757.mp4',1,'eq=saturation=1.05'),
 ('s09','4500W เหมาะกับบ้านที่ใช้กันหลายคน', 'px_10565899.mp4',1,'eq=saturation=1.05'),
 ('s12','ข้อสอง ความปลอดภัย', '../vid/dl/px_plug.jpg',0,'eq=saturation=1.05'),
 ('s13','ต้องมี มอก.', 'px_35152432.mp4',1,'eq=saturation=1.05'),
 ('s14','และ ELCB ตัดไฟเมื่อไฟรั่ว', '../ac/dl/px_11503031.mp4',0,'eq=saturation=1.05'),
 ('s15','มีระบบเช็กสายดินด้วย ยิ่งอุ่นใจ', 'px_8955853.mp4',1,'colorbalance=rm=.08:rh=.06,eq=saturation=1.08'),
 ('s16','ข้อสาม ฝักบัว', 'px_36188238.mp4',1,'eq=contrast=1.05'),
 ('s17','ใช้ Rain Shower ต้อง 4500W ขึ้นไป', 'px_9166285.mp4',1,'eq=contrast=1.05'),
 ('s18','ไม่งั้นน้ำจะไม่ค่อยอุ่น', 'px_9166284.mp4',1,'colorbalance=bs=.3:bm=.18:rs=-.18,eq=saturation=0.8'),
 ('s19','มาดู 3 รุ่นที่คนถามเยอะ', WAT,1,'gblur=sigma=10,eq=brightness=-0.1'),
 ('l7a','FENIX 4.5', WAT,3,DARK),
 ('l7b','งบไม่เยอะ แต่มี ELCB ครบ', WAT,5,DARK),
 ('l8','MIRACLE มีระบบเช็กสายดิน', WAT,7,DARK),
 ('s23','เลือกวัตต์ได้ตามบ้าน', WAT,9,DARK),
 ('s24','แถมมีรุ่น Rain Shower', WAT,11,DARK),
 ('s25','EXTREME จัดเต็มความปลอดภัย', WAT,2,DARK),
 ('s26','ELCB 2 ชั้น ตัดไฟเองถ้าเปิดนานเกิน', WAT,4,DARK),
 ('s27','สรุป งบประหยัด FENIX', WAT,6,DARK),
 ('s28','อยากเลือกวัตต์ MIRACLE', WAT,8,DARK),
 ('s29','อยากปลอดภัยสุด EXTREME', WAT,10,DARK),
 ('s30','ทุกรุ่นอยู่ในตะกร้าด้านล่างนะครับ', 'px_6898061.mp4',1,'eq=saturation=1.05'),
 ('s31','ไม่แน่ใจรุ่นไหน คอมเมนต์ถามได้เลยครับ', 'px_7822029.mp4',1,'eq=saturation=1.05'),
]
# ---------- timeline + voice
t = LEAD; shots = []; ins = []; flt = []; parts = []
flt.append(f'anullsrc=r=24000:cl=mono,atrim=0:{LEAD}[lead]'); parts.append('[lead]')
for i,(k,cap,*_) in enumerate(SH):
    f = f'{V}/{k}t.wav'; d = dur(f)/TEMPO; sd = max(MINS, d + PAD)
    ins += ['-i', f]; flt.append(f'[{i}]aresample=24000,atempo={TEMPO},apad=pad_dur={sd-d:.3f}[p{i}]'); parts.append(f'[p{i}]')
    shots.append(dict(a=round(t,3), b=round(t+sd,3), v=round(d,3), cap=cap)); t += sd
END = round(t + 0.6, 2)
flt.append(''.join(parts)+f'concat=n={len(parts)}:v=0:a=1,highpass=f=80,equalizer=f=180:t=q:w=1:g=1,acompressor=threshold=-18dB:ratio=2:attack=10:release=150:makeup=1.3[o]')
subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',';'.join(flt),'-map','[o]','-ar','44100',f'{D}/voice.wav'],check=True)
shots[-1]['b'] = END; shots[0]['a'] = 0
open(f'{D}/timeline.js','w').write('window.TL='+json.dumps(dict(S=shots,END=END),ensure_ascii=False)+';')
# ---------- background
COVER = "scale='if(gt(a,9/16),-2,1080)':'if(gt(a,9/16),1920,-2)',crop=1080:1920"
ins=[]; flt=[]; outs=[]
for i,((k,cap,f,ss,ex),s) in enumerate(zip(SH,shots)):
    nf = round(s['b']*30)-round(s['a']*30); d = round(nf/30+0.2,3); p = f if f.startswith('..') else f'dl/{f}'
    ins += (['-loop','1','-i',p] if p.endswith('.jpg') else ['-stream_loop','-1','-ss',str(ss),'-i',p])
    z = "1.12-0.1*on/{n}" if i%3==1 else "1+0.08*on/{n}"
    n = nf
    flt.append(f"[{i}]trim=duration={d},setpts=PTS-STARTPTS,fps=30,trim=end_frame={nf},{COVER},{ex},zoompan=z='{z.format(n=n)}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1,format=yuv420p[v{i}]")
    outs.append(f'[v{i}]')
flt.append(''.join(outs)+f'concat=n={len(SH)}:v=1:a=0,format=yuv420p[out]')
subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',';'.join(flt),'-map','[out]','-c:v','libx264','-crf','14','-preset','veryfast',f'{D}/bg.mp4'],check=True,cwd=D)
# ---------- mix: voice + one unique sfx per shot
ins=['-i',f'{D}/voice.wav']; flt=['[0]pan=stereo|c0=c0|c1=c0[a0]']
VOL = {1:.5,2:.3,13:.5,17:.5,19:.35}; SFXID=[1,2,3,4,5,6,7,8,9]+list(range(12,32))
for j,s in enumerate(shots,1):
    ins += ['-i',f'{D}/sfx/x{SFXID[j-1]:02d}.wav']; dd=max(0,int((s['a']-(0.42 if j==1 else 0.02))*1000))
    if j==1: dd=0
    flt.append(f'[{j}]volume={VOL.get(SFXID[j-1],.28)},adelay={dd}|{dd}[a{j}]')
N=len(shots)+1
flt.append(''.join(f'[a{j}]' for j in range(N))+f'amix=inputs={N}:normalize=0:duration=longest,apad,atrim=0:{END},alimiter=limit=0.95[out]')
subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',';'.join(flt),'-map','[out]','-ar','44100',f'{D}/mix.wav'],check=True)
print('END',END, [ (s['a'],s['b']) for s in shots][:5])

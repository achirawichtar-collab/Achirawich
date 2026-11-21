import json, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); V = f'{D}/v'; N = f'{D}/news'
LEAD = 0.15; GAP = 0.14; TAIL = 1.0
dur = lambda f: float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
P = lambda i: f'dl/px_{i}.mp4'; T = lambda n: f'news/{n}.jpg'
WARM='colorbalance=rm=.08:rh=.05:bm=-.05,eq=saturation=1.1'; COOL='colorbalance=bs=.18:bm=.1:rs=-.1'
DESAT='hue=s=0.35,eq=contrast=1.1'; RED='colorbalance=rs=.3:rm=.15:bs=-.15,eq=contrast=1.1'
DARK='gblur=sigma=18,eq=brightness=-0.25:saturation=0.7'
# (voice, caption, [ (src, seek, filter, motion, overlay-key, credit) ])
SEG = [
 ('v01','ยายต้มน้ำแบบนี้มาสามสิบปี',[(P(40995593),2,WARM,'punch','hook','Pexels'),(P(39681214),4,WARM,'in','','Pexels')]),
 ('v02','แต่ปีนี้ ต้มแล้วก็ยังไม่พอ',[(P(40995593),5,DESAT,'freeze','notsafe','Pexels')]),
 ('v03','มิ้น หลานสาวของยาย กลับบ้านที่แม่สาย เชียงราย ช่วงหยุดยาว',[(P(36443759),2,'eq=saturation=1.1','whip','name','Pexels'),(P(7361537),2,WARM,'out','','Pexels')]),
 ('v04','แต่ข่าวเช้านั้น ทำให้เธอนิ่งไป',[(P(9808087),3,'eq=saturation=1.1','in','tv','Pexels'),(P(30235969),2,DESAT,'slowin','bubbleq','Pexels')]),
 ('v05','กรมควบคุมมลพิษ พบสารหนูในแม่น้ำสาย เกินมาตรฐานสูงสุด 28 เท่า',[(T('tp572238_50'),0,'eq=contrast=1.05','in','news28','ภาพ: Thai PBS'),(T('tp572860_15'),0,'eq=contrast=1.05','shake','news28b','ภาพ: Thai PBS')]),
 ('v07','ยายบอกว่า ต้มแล้ว ไม่เป็นไรหรอก',[(P(4058079),3,WARM,'slowin','bubbley','Pexels')]),
 ('v08','แต่ต้นทางของสายน้ำนี้ อยู่ไกลกว่าที่ยายคิด',[(T('tp572238_54'),0,'eq=saturation=1.1','crash','lbl_kok','ภาพ: Thai PBS'),(T('tp572238_53'),0,RED,'in','lbl_mine','ภาพ: Thai PBS')]),
 ('v09','แม่น้ำกก ไหลจากรัฐฉาน เข้าไทยที่แม่อาย เชียงใหม่',[('G',0,'','none','map1','แผนผังโดยประมาณ'),(T('tp572238_55'),0,RED,'out','lbl_dredge','ภาพ: Thai PBS')]),
 ('v10','ผ่านตัวเมืองเชียงราย แล้วลงแม่น้ำโขงที่เชียงแสน',[('G',0,'','none','map2','แผนผังโดยประมาณ'),(P(28728843),3,'eq=saturation=1.1','in','lbl_cs','Pexels')]),
 ('v11','ส่วนแม่น้ำสาย กั้นพรมแดนแม่สายกับท่าขี้เหล็ก',[('G',0,'','none','map3','แผนผังโดยประมาณ'),(T('tp572860_16'),0,'eq=contrast=1.05','in','lbl_sat','ภาพ: Thai PBS')]),
 ('v12','ไหลรวมแม่น้ำรวก ลงโขงที่สามเหลี่ยมทองคำ',[(P(28728843),10,WARM,'drift','lbl_gt','Pexels')]),
 ('v13','ตลอดสองฝั่ง คือชีวิตคนจำนวนมาก|ทั้งชาวนา|คนหาปลา|แม่ค้าผัก และครอบครัวริมน้ำ',[(T('tp572238_51'),0,'eq=saturation=1.1','in','who1','ภาพ: Thai PBS'),(P(33837071),3,'eq=saturation=1.1','split','who2','Pexels'),('dl/ph_33539441.jpg',0,'eq=saturation=1.1','in','who3','Pexels'),(P(8717741),2,'eq=saturation=1.1','stutter','who4','Pexels')]),
 ('v14','สิ่งที่หลายบ้านยังเข้าใจผิดคือ|ต้มน้ำ ไม่ได้ทำให้สารหนูหายไป',[(P(8094272),2,'eq=contrast=1.1','in','particles','Pexels'),(P(40995593),8,'eq=contrast=1.1','shake','stamp','Pexels')]),
 ('v15','น้ำระเหยไป แต่สารหนูยังอยู่ในหม้อ',[(P(8094272),5,'eq=brightness=-0.12:contrast=1.1','slowin','evap','Pexels + กราฟิก')]),
 ('v16','และเพราะมันละลายอยู่ในน้ำ ไส้กรองทั่วไปจึงดักได้ไม่หมด',[(P(9667570),2,'eq=brightness=-0.08','in','filters','Pexels + กราฟิก')]),
 ('v17','ระบบ RO ใช้เยื่อกรองละเอียดระดับ 0.0001 ไมครอน',[(P(9667568),1,'eq=brightness=-0.05','in','membrane','Pexels + กราฟิก'),(P(16478029),2,'eq=brightness=-0.22','in','membrane2','Pexels + กราฟิก')]),
 ('v18','ช่วยลดสารหนู และโลหะหนักที่ละลายในน้ำได้',[(P(16478029),7,'eq=brightness=-0.25','out','block','Pexels + กราฟิก')]),
 ('v19','มาซูม่ามีเครื่องกรอง RO ให้เลือกหลายรุ่น',[(P(9667568),5,'eq=brightness=-0.05','in','prodA','ภาพสินค้า: Mazuma'),(P(9667570),6,'eq=brightness=-0.15','out','prodB','ภาพสินค้า: Mazuma')]),
 ('v20','วันนั้น มิ้นเลยติดเครื่องกรอง RO ให้ยาย',[(P(4058079),8,'eq=brightness=0.03:saturation=1.1','slowin','clean','Pexels')]),
 ('v21','ยายบอกว่า รสชาติก็เหมือนเดิม แต่มิ้นนอนหลับสบายขึ้น',[(P(7361537),8,WARM,'in','bubblet','Pexels'),(P(39681214),9,WARM,'out','','Pexels')]),
 ('v22','ถ้าบ้านอยู่ริมน้ำกก น้ำสาย ติดตามประกาศทางการ|และเลือกน้ำดื่มผ่านระบบ RO',[(T('tp572238_54'),0,DARK,'none','check','ภาพ: Thai PBS'),(P(34781948),4,DARK,'none','check2','Pexels')]),
 ('v23','มีคนที่รักอยู่แถวนั้น ส่งคลิปนี้ให้เขาดูนะครับ',[(P(28728843),14,'gblur=sigma=6,eq=brightness=-0.15','in','cta','Pexels')]),
]
# ---------- voice + timeline
t = LEAD; ins=[]; flt=[f'anullsrc=r=24000:cl=mono,atrim=0:{LEAD}[l]']; parts=['[l]']; shots=[]; caps=[]
for i,(k,cap,sh) in enumerate(SEG):
    f=f'{V}/{k}t.wav'; d=dur(f); sd=d+GAP
    if i==len(SEG)-1: sd += TAIL
    ins += ['-i',f]; flt.append(f'[{i}]aresample=24000,apad=pad_dur={sd-d:.3f}[p{i}]'); parts.append(f'[p{i}]')
    a0 = t if i else 0
    seg_end = t+sd; n=len(sh); L=(seg_end-a0)/n
    for j,s in enumerate(sh): shots.append(dict(a=round(a0+j*L,3), b=round(a0+(j+1)*L,3), src=s[0], ss=s[1], f=s[2], m=s[3], ov=s[4], cr=s[5]))
    cs = cap.split('|'); Lc=sum(len(c) for c in cs); c0=t
    for c in cs: cd=d*len(c)/Lc; caps.append([round(c0,3),round(c0+cd+0.1,3),c]); c0+=cd
    t += sd
END = round(t,2)
flt.append(''.join(parts)+f'concat=n={len(parts)}:v=0:a=1,highpass=f=80,equalizer=f=180:t=q:w=1:g=1,acompressor=threshold=-18dB:ratio=2:attack=10:release=150:makeup=1.3[o]')
subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',';'.join(flt),'-map','[o]','-ar','44100',f'{D}/voice.wav'],check=True)
open(f'{D}/timeline.js','w').write('window.TL='+json.dumps(dict(S=[{k:v for k,v in s.items() if k in('a','b','ov','cr')} for s in shots],caps=caps,END=END),ensure_ascii=False)+';')
# ---------- background
COVER = "scale='if(gt(a,9/16),-2,1080)':'if(gt(a,9/16),1920,-2)',crop=1080:1920"
ins=[]; flt=[]; outs=[]
for i,s in enumerate(shots):
    nf = round(s['b']*30)-round(s['a']*30); d = nf/30+0.3
    if s['src']=='G': ins += ['-f','lavfi','-i',f'color=c=0x07111d:s=1080x1920:r=30:d={d}']
    elif s['src'].endswith('.jpg'): ins += ['-loop','1','-t',str(d),'-i',s['src']]
    else: ins += ['-stream_loop','-1','-ss',str(s['ss']),'-i',s['src']]
    m=s['m']; fx = (s['f']+',') if s['f'] else ''
    zp = {'in':"1.04+0.10*on/{n}",'out':"1.16-0.12*on/{n}",'punch':"if(lt(on,6),1.35-0.05*on,1.05+0.05*on/{n})",'crash':"1+0.5*pow(on/{n},3)",
          'slowin':"1+0.06*on/{n}",'drift':"1.1",'whip':"1.08",'split':"1.06",'stutter':"1.05+0.04*on/{n}",'shake':"1.12",'freeze':"1.0+0.25*on/{n}",'none':"1"}[m].format(n=max(1,nf))
    xx = {'drift':"(iw-iw/zoom)*on/{n}",'whip':"(iw-iw/zoom)/2+if(lt(on,5),(5-on)*80,0)",'shake':"(iw-iw/zoom)/2+18*sin(on*1.9)"}.get(m,"(iw-iw/zoom)/2").format(n=max(1,nf))
    yy = "(ih-ih/zoom)/2+14*cos(on*2.3)" if m=='shake' else "(ih-ih/zoom)/2"
    pre = "trim=end_frame=1,loop=loop=-1:size=1," if m=='freeze' else ""
    extra = ",rgbashift=rh=-12:bh=12" if m in ('freeze','crash') else ""
    flt.append(f"[{i}]setpts=PTS-STARTPTS,fps=30,{pre}trim=end_frame={nf+2},{COVER},{fx}zoompan=z='{zp}':x='{xx}':y='{yy}':d=1:s=1080x1920:fps=30{extra},trim=end_frame={nf},setsar=1,format=yuv420p[v{i}]")
    outs.append(f'[v{i}]')
flt.append(''.join(outs)+f'concat=n={len(shots)}:v=1:a=0,format=yuv420p[out]')
subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',';'.join(flt),'-map','[out]','-c:v','libx264','-crf','15','-preset','veryfast',f'{D}/bg.mp4'],check=True,cwd=D)
# ---------- audio mix: voice + one unique sfx per shot
ids=[1,3,5,4,7,8,9,10,11,13,12,14,6,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,2]
VOL={1:.45,2:.3,13:.45,17:.45,19:.3,35:.35,40:.5}
ins=['-i',f'{D}/voice.wav']; flt=['[0]pan=stereo|c0=c0|c1=c0,volume=1.0[a0]']
for j,s in enumerate(shots,1):
    x=ids[j-1]; ins += ['-i',f'{D}/sfx/x{x:02d}.wav']; dd=int(s['a']*1000)
    flt.append(f'[{j}]volume={VOL.get(x,.26)},adelay={dd}|{dd}[a{j}]')
N2=len(shots)+1
flt.append(''.join(f'[a{j}]' for j in range(N2))+f'amix=inputs={N2}:normalize=0:duration=longest,apad,atrim=0:{END},alimiter=limit=0.95[out]')
subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',';'.join(flt),'-map','[out]','-ar','44100',f'{D}/mix.wav'],check=True)
print('END',END,'shots',len(shots),'sfx',[ids[j] for j in range(len(shots))])

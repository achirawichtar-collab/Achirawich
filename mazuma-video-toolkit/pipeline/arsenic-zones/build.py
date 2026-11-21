import json, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); V = f'{D}/v'
LEAD = 0.15; GAP = 0.28; TAIL = 1.2
dur = lambda f: float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
P = lambda i: f'dl/px_{i}.mp4'
CINE = 'colorbalance=rs=-.04:bs=.06:rh=.06:bh=-.05,eq=contrast=1.08:saturation=1.08'
# shot = (src, seek, extra-filter, motion, ov-key, credit, cg-stage)
SEG = [
 ('v01','สารหนูจากเหมืองในเมียนมา ไหลมาถึงจังหวัดคุณหรือยัง?',[('G',0,'','none','hook','ภาพดาวเทียม: NASA Blue Marble','globe')]),
 ('v02','ต้นตอมาจากเหมืองแร่ต้นน้ำฝั่งเมียนมา',[('news/n12.jpg',0,CINE+',colorbalance=rs=.12:rm=.06','crash','mine','ภาพ: Thai PBS',None)]),
 ('v03','แบ่งพื้นที่ได้ 3 โซน|เช็กเลยครับ ว่าบ้านคุณอยู่โซนไหน',[('G',0,'','none','zones','ภาพดาวเทียม: NASA Blue Marble','full')]),
 ('v04','โซนแดง ภาคเหนือ|เชียงราย เชียงใหม่ และแม่ฮ่องสอน',[('G',0,'','none','north','ภาพดาวเทียม: NASA Blue Marble','north')]),
 ('v05','เชียงรายจากแม่น้ำสาย กก รวก|ส่วนแม่ฮ่องสอนจากแม่น้ำสาละวิน',[('news/n15c.jpg',0,CINE,'in','gt','ภาพ: Thai PBS',None),('news/n14.jpg',0,CINE,'drift','salween','ภาพ: Thai PBS',None)]),
 ('v06','อีสานตอนบน เลย หนองคาย บึงกาฬ นครพนม|ซึ่งอยู่ริมแม่น้ำโขง',[('G',0,'','none','isan','ภาพดาวเทียม: NASA Blue Marble','isan'),(P(30212868),8,CINE,'in','nk','Pexels',None)]),
 ('v07','กรมควบคุมโรค พบคนที่มีสารหนูในร่างกาย|เกินค่าอ้างอิงแล้ว 94 คน',[('news/n13.png',0,'eq=contrast=1.05','in','ddc','ภาพ: กรมควบคุมโรค / Thai PBS',None),('G',0,'','none','atom','กราฟิก','atom')]),
 ('v08','โซนส้ม มุกดาหาร อำนาจเจริญ อุบลราชธานี|ที่อยู่ปลายน้ำโขง',[('G',0,'','none','watch','ภาพดาวเทียม: NASA Blue Marble','watch')]),
 ('v09','ถ้าต้นทางยังไม่หยุดปล่อย|ตะกอนอาจไหลตามน้ำโขงลงมาถึงที่นี่',[('G',0,'','none','south','ภาพดาวเทียม: NASA Blue Marble','south')]),
 ('v10','โซนเขียว ภาคกลาง กรุงเทพ ตะวันออก ตะวันตก และภาคใต้|ไม่อยู่ในเส้นทางน้ำสายนี้',[('G',0,'','none','central','ภาพดาวเทียม: NASA Blue Marble','central'),(P(31120278),18,CINE,'drift','bkk1','Pexels',None)]),
 ('v11','การประปานครหลวงยืนยัน|น้ำประปา กรุงเทพ นนทบุรี สมุทรปราการ ไม่ได้รับผลกระทบ',[(P(31120278),2,CINE,'in','mwa','Pexels · ข้อมูล: กปน. 16 พ.ย. 69',None),(P(38412911),0,CINE,'slowin','','Pexels',None)]),
 ('v12','แต่ควรระวังปลาแม่น้ำ|และผลผลิตเกษตร ที่ส่งมาจากจังหวัดเสี่ยง',[(P(15777860),2,CINE,'in','fish','Pexels',None),(P(10354557),1,CINE,'out','farm','Pexels',None)]),
 ('v13','ถ้าบ้านอยู่โซนแดงหรือส้ม|น้ำดื่มควรผ่านเครื่องกรองระบบ RO ที่ช่วยลดสารหนูและโลหะหนัก',[(P(4061892),2,CINE,'slowin','tap','Pexels',None),('G',0,'','none','prod','ภาพสินค้า: Mazuma','atomdark')]),
 ('v14','และติดตามประกาศจากหน่วยงานทางการเสมอ',[(P(4109353),3,CINE,'in','official','Pexels',None)]),
 ('v15','เซฟคลิปนี้ไว้ แล้วแชร์ให้คนที่อยู่ในโซนเสี่ยงนะครับ',[('G',0,'','none','cta','ที่มา: กปน. · คพ. · กรมควบคุมโรค · Thai PBS · NASA','all')]),
]
t = LEAD; ins=[]; flt=[f'anullsrc=r=24000:cl=mono,atrim=0:{LEAD}[l]']; parts=['[l]']; shots=[]; caps=[]
for i,(k,cap,sh) in enumerate(SEG):
    f=f'{V}/{k}t.wav'; d=dur(f); sd=d+GAP+(TAIL if i==len(SEG)-1 else 0)
    ins += ['-i',f]; flt.append(f'[{i}]aresample=24000,apad=pad_dur={sd-d:.3f}[p{i}]'); parts.append(f'[p{i}]')
    a0 = t if i else 0; L=(t+sd-a0)/len(sh)
    for j,s in enumerate(sh): shots.append(dict(a=round(a0+j*L,3), b=round(a0+(j+1)*L,3), src=s[0], ss=s[1], f=s[2], m=s[3], ov=s[4], cr=s[5], cg=s[6]))
    cs=cap.split('|'); Lc=sum(len(c) for c in cs); c0=t
    for c in cs: cd=d*len(c)/Lc; caps.append([round(c0,3),round(c0+cd+0.1,3),c]); c0+=cd
    t += sd
END=round(t,2)
flt.append(''.join(parts)+f'concat=n={len(parts)}:v=0:a=1,highpass=f=80,equalizer=f=180:t=q:w=1:g=1,acompressor=threshold=-18dB:ratio=2:attack=10:release=150:makeup=1.3[o]')
subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',';'.join(flt),'-map','[o]','-ar','44100',f'{D}/voice.wav'],check=True)
open(f'{D}/timeline.js','w').write('window.TL='+json.dumps(dict(S=[{k:v for k,v in s.items() if k in('a','b','ov','cr','cg')} for s in shots],caps=caps,END=END),ensure_ascii=False)+';')
# background (footage shots; CG shots black)
COVER="scale='if(gt(a,9/16),-2,1080)':'if(gt(a,9/16),1920,-2)',crop=1080:1920"
ins=[]; flt=[]; outs=[]
for i,s in enumerate(shots):
    nf=round(s['b']*30)-round(s['a']*30); d=nf/30+0.3
    if s['src']=='G': ins+=['-f','lavfi','-i',f'color=c=black:s=1080x1920:r=30:d={d}']
    elif s['src'].endswith(('.jpg','.png')): ins+=['-loop','1','-t',str(d),'-i',s['src']]
    else: ins+=['-stream_loop','-1','-ss',str(s['ss']),'-i',s['src']]
    m=s['m']; n=max(1,nf); fx=(s['f']+',') if s['f'] else ''
    zp={'in':f"1.04+0.10*on/{n}",'out':f"1.16-0.12*on/{n}",'crash':f"1+0.45*pow(on/{n},3)",'slowin':f"1+0.06*on/{n}",'drift':"1.1",'none':"1"}[m]
    xx=f"(iw-iw/zoom)*on/{n}" if m=='drift' else "(iw-iw/zoom)/2"
    flt.append(f"[{i}]setpts=PTS-STARTPTS,fps=30,trim=end_frame={nf+2},{COVER},{fx}zoompan=z='{zp}':x='{xx}':y='(ih-ih/zoom)/2':d=1:s=1080x1920:fps=30,vignette=PI/4.5,trim=end_frame={nf},setsar=1,format=yuv420p[v{i}]")
    outs.append(f'[v{i}]')
flt.append(''.join(outs)+f'concat=n={len(shots)}:v=1:a=0,format=yuv420p[out]')
subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',';'.join(flt),'-map','[out]','-c:v','libx264','-crf','15','-preset','veryfast',f'{D}/bg.mp4'],check=True,cwd=D)
# audio: voice + unique sfx per shot (+ low drone bed)
SF=f'{D}/../kok/sfx'
ids=[36,1,6,11,33,22,4,13,7,10,25,26,19,35,40,30,8,9,24,16,17,3,15,39][:len(shots)]
assert len(set(ids))==len(shots),(len(ids),len(shots))
ins=['-i',f'{D}/voice.wav']; flt=['[0]pan=stereo|c0=c0|c1=c0[a0]']
for j,s in enumerate(shots,1):
    x=ids[j-1]; ins+=['-i',f'{SF}/x{x:02d}.wav']; dd=int(s['a']*1000); flt.append(f'[{j}]volume={.4 if x in (1,36,35,40,17) else .24},adelay={dd}|{dd}[a{j}]')
N=len(shots)+1
flt.append(f"sine=f=55:d={END},volume=0.035,afade=t=in:d=1.5,afade=t=out:st={END-1.5}:d=1.5,pan=stereo|c0=c0|c1=c0[dr]")
flt.append(''.join(f'[a{j}]' for j in range(N))+f'[dr]amix=inputs={N+1}:normalize=0:duration=longest,apad,atrim=0:{END},alimiter=limit=0.95[out]')
subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',';'.join(flt),'-map','[out]','-ar','44100',f'{D}/mix.wav'],check=True)
print('END',END,'shots',len(shots))

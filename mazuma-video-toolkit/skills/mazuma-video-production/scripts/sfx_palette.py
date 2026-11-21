import numpy as np, wave, os
SR = 44100; D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sfx')
def t(d): return np.arange(int(SR*d))/SR
def env(x, a=0.005, r=None):
    n=len(x); e=np.ones(n); na=max(1,int(a*SR)); e[:na]=np.linspace(0,1,na)
    if r: nr=min(n,int(r*SR)); e[-nr:]*=np.linspace(1,0,nr)**2
    return x*e
def dec(d, k): return np.exp(-t(d)*k)
def sine(f, d): return np.sin(2*np.pi*f*t(d)) if np.isscalar(f) else np.sin(2*np.pi*np.cumsum(f)/SR)
def sq(f, d): return np.sign(sine(f, d))*0.5
def at(parts, d):
    o=np.zeros(int(SR*d))
    for s,x in parts:
        i=int(s*SR); o[i:i+len(x)]+=x[:len(o)-i]
    return o
def lp_noise(d, k=0.85):
    n=np.random.default_rng(1).standard_normal(int(SR*d)); y=np.zeros_like(n); a=0
    for i,v in enumerate(n): a=k*a+(1-k)*v; y[i]=a
    return y/np.abs(y).max()
def save(name, x, g=0.8):
    x=x/ (np.abs(x).max()+1e-9)*g; s=(np.clip(x,-1,1)*32767).astype(np.int16)
    with wave.open(f'{D}/{name}.wav','wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(s.tobytes())
os.makedirs(D, exist_ok=True)
# 1 riser + boom
d=0.7; f=np.linspace(200,900,int(SR*0.45)); r=sine(f,0.45)*np.linspace(0,1,len(f))*0.4
boom=sine(np.linspace(110,40,int(SR*0.5)),0.5)*dec(0.5,7)
save('x01', at([(0,r),(0.42,boom)],1.0))
# 2 wrong buzzer
save('x02', env(sq(110,0.5)*0.6+sq(116,0.5)*0.4, r=0.1))
# 3 water bloop
save('x03', env(sine(np.linspace(300,1200,int(SR*0.12)),0.12)*dec(0.12,20), r=0.03))
# 4 glitch
g=np.concatenate([sq(f,0.04)*(i%2) for i,f in enumerate([880,220,1500,330,1100,180,660])]); save('x04', g, 0.6)
# 5 zap crackle
z=np.concatenate([sine(np.linspace(2000,300,int(SR*0.06)),0.06)*dec(0.06,40), np.zeros(int(SR*0.05)), sine(np.linspace(2400,200,int(SR*0.08)),0.08)*dec(0.08,30)]); save('x05', z, 0.65)
# 6 triple pop
p=lambda f: sine(np.linspace(f*2,f,int(SR*0.07)),0.07)*dec(0.07,45)
save('x06', at([(0,p(500)),(0.25,p(650)),(0.5,p(800))],0.7))
# 7 counting ticks
save('x07', at([(i*0.07, sine(2600,0.015)*dec(0.015,200)) for i in range(12)],0.9), 0.5)
# 8 ding high
save('x08', sine(1760,0.8)*dec(0.8,5)+0.3*sine(3520,0.8)*dec(0.8,9))
# 9 ding-dong up
save('x09', at([(0,sine(784,0.5)*dec(0.5,6)),(0.18,sine(1175,0.7)*dec(0.7,5))],0.9))
# 10 heartbeat
hb=lambda: sine(55,0.15)*dec(0.15,25)
save('x10', at([(0,hb()),(0.18,hb()),(0.7,hb()),(0.88,hb())],1.1))
# 11 alarm beep-beep
save('x11', at([(0,env(sq(1000,0.12),r=0.01)),(0.2,env(sq(1000,0.12),r=0.01))],0.35), 0.45)
# 12 shimmer
save('x12', sum(sine(f,0.9)*dec(0.9,4)*np.sin(np.pi*t(0.9)/0.9) for f in [1320,1980,2640,3300]), 0.5)
# 13 stamp thud
save('x13', sine(np.linspace(160,50,int(SR*0.25)),0.25)*dec(0.25,18)+0.3*lp_noise(0.25,0.7)*dec(0.25,40))
# 14 switch click
save('x14', at([(0,lp_noise(0.02,0.3)*dec(0.02,200)),(0.06,lp_noise(0.03,0.3)*dec(0.03,150))],0.15), 0.7)
# 15 harp up
save('x15', at([(i*0.07, sine(f,0.6)*dec(0.6,6)) for i,f in enumerate([523,659,784,1047,1319])],1.0), 0.6)
# 16 water drops ascending (tonal)
save('x16', at([(i*0.12, sine(np.linspace(f,f*2,int(SR*0.08)),0.08)*dec(0.08,30)) for i,f in enumerate([400,520,450,600])],0.6), 0.5)
# 17 bass drop
save('x17', sine(np.linspace(90,30,int(SR*0.9)),0.9)*dec(0.9,3.5))
# 18 falling tone
save('x18', env(sine(np.linspace(900,150,int(SR*0.6)),0.6)*0.6, r=0.1), 0.45)
# 19 drum roll (tonal toms)
save('x19', at([(i*0.05, sine(np.linspace(220,120,int(SR*0.06)),0.06)*dec(0.06,40)*(0.4+i/30)) for i in range(18)]+[(0.92,sine(np.linspace(150,60,int(SR*0.3)),0.3)*dec(0.3,10))],1.3))
# 20 camera shutter
save('x20', at([(0,lp_noise(0.03,0.2)*dec(0.03,120)),(0.08,lp_noise(0.04,0.2)*dec(0.04,90))],0.2), 0.6)
# 21 cash ching
save('x21', at([(0,sine(2093,0.5)*dec(0.5,8)),(0.05,sine(2637,0.6)*dec(0.6,7))],0.7), 0.55)
# 22 slide up x2
s=lambda: env(sine(np.linspace(300,1400,int(SR*0.15)),0.15)*dec(0.15,8), r=0.03)
save('x22', at([(0,s()),(0.2,s())],0.4), 0.45)
# 23 8-bit coins x3
c=lambda: np.concatenate([sq(988,0.05),sq(1319,0.18)*dec(0.18,12)])
save('x23', at([(0,c()),(0.28,c()),(0.56,c())],0.85), 0.3)
# 24 bubbles
save('x24', at([(i*0.09, sine(np.linspace(f,f*1.8,int(SR*0.05)),0.05)*dec(0.05,50)) for i,f in enumerate([700,900,600,1000,800])],0.6), 0.5)
# 25 power-up 8-bit
save('x25', np.concatenate([sq(f,0.045) for f in np.linspace(300,1500,16)]), 0.3)
# 26 tick-tock
tk=lambda f: sine(f,0.03)*dec(0.03,150)
save('x26', at([(i*0.3, tk(1800 if i%2==0 else 1200)) for i in range(5)],1.5), 0.55)
# 27 claps
save('x27', at([(i*0.16, lp_noise(0.05,0.25)*dec(0.05,70)) for i in range(2)],0.4), 0.55)
# 28 finger snap
save('x28', lp_noise(0.04,0.1)*dec(0.04,160)+0.4*sine(2200,0.04)*dec(0.04,120), 0.6)
# 29 ta-da
save('x29', at([(0,sine(523,0.15)*dec(0.15,8)),(0.12,sum(sine(f,0.9)*dec(0.9,3) for f in [523,659,784,1047]))],1.1), 0.6)
# 30 notification
save('x30', at([(0,sine(1318,0.2)*dec(0.2,12)),(0.12,sine(1976,0.4)*dec(0.4,8))],0.6), 0.5)
# 31 keyboard taps
save('x31', at([(i*0.09+0.02*(i%2), lp_noise(0.015,0.4)*dec(0.015,300)) for i in range(7)],0.8), 0.5)
print('ok')

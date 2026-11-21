import sys; sys.argv=['x']
exec(open('../wh/sfx.py').read().split("os.makedirs(D, exist_ok=True)")[0])
D='sfx'
import numpy as np
def tri(f,d): return 2*np.abs(2*((np.cumsum(np.full(int(SR*d),f))/SR)%1)-1)-1
save('x32', at([(i*0.09, sine(f,0.35)*dec(0.35,9)) for i,f in enumerate([523,659,784])],0.7),0.5)   # marimba arp
save('x33', env(sine(np.linspace(1200,200,int(SR*0.35)),0.35),r=0.05)*0.6,0.45)                       # tonal swoop down
save('x34', at([(0,tri(2400,0.02)*dec(0.02,200)),(0.12,sine(3000,0.3)*dec(0.3,10))],0.45),0.5)         # typewriter ding
save('x35', sum(sine(f,1.2)*dec(1.2,3) for f in [196,294.5,392]) ,0.55)                                   # soft gong chord
save('x36', env(sine(np.linspace(80,400,int(SR*0.4)),0.4)*np.linspace(0,1,int(SR*0.4)),r=0.03),0.5)    # zoom-in rise
save('x37', at([(i*0.05, sine(4000-i*300,0.04)*dec(0.04,80)) for i in range(8)],0.5),0.35)            # bell tree down
save('x38', sine(np.linspace(1800,600,int(SR*0.18)),0.18)*dec(0.18,15),0.4)                           # laser
save('x39', at([(0,sine(330,0.5)*dec(0.5,7)),(0.16,sine(440,0.5)*dec(0.5,7)),(0.32,sine(554,0.7)*dec(0.7,5))],1.1),0.5) # hopeful 3-note
save('x40', sine(np.linspace(140,70,int(SR*0.3)),0.3)*dec(0.3,12),0.7)                                # low pop thud
save('x41', at([(0,sine(880,0.12)*dec(0.12,25)),(0.1,sine(660,0.12)*dec(0.12,25))],0.3),0.45)       # chat pop 2-tone
print('ok')

"""Tonal transition sounds for Mazuma clips (no wind/noise whooshes).
Usage: python transition_sfx.py OUT_DIR   -> writes t01..t10 *.wav (44.1 kHz mono)
"""
import numpy as np, wave, os, sys
SR = 44100
OUT = sys.argv[1] if len(sys.argv) > 1 else 'tsfx'
os.makedirs(OUT, exist_ok=True)
t = lambda d: np.arange(int(SR*d))/SR
dec = lambda d,k: np.exp(-t(d)*k)
def sine(f, d):
    f = np.full(int(SR*d), f) if np.isscalar(f) else f
    return np.sin(2*np.pi*np.cumsum(f)/SR)
glide = lambda a,b,d: np.geomspace(a,b,int(SR*d))
def at(parts, d):
    o = np.zeros(int(SR*d))
    for s,x in parts:
        i = int(s*SR); n = min(len(x), len(o)-i); o[i:i+n] += x[:n]
    return o
def save(name, x, g=0.8):
    x = x/(np.abs(x).max()+1e-9)*g
    with wave.open(f'{OUT}/{name}.wav','wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype(np.int16).tobytes())

save('t01_drop_ripple', at([(0, sine(glide(500,1500,0.09),0.09)*dec(0.09,25)), (0.05, sine(glide(90,50,0.6),0.6)*dec(0.6,5)*0.6)], 0.7))
save('t02_rise_hit',    at([(0, sine(glide(150,1200,0.32),0.32)*np.linspace(0,1,int(SR*0.32))**2*0.5), (0.3, sine(glide(120,45,0.4),0.4)*dec(0.4,9))], 0.75))
save('t03_shimmer_sweep', at([(i*0.035, sine(f,0.5)*dec(0.5,7)) for i,f in enumerate([1047,1319,1568,2093,2637,3136])], 0.75), 0.55)
save('t04_digital_glitch', np.concatenate([np.sign(sine(f,0.03))*0.5*(i%2) for i,f in enumerate([1500,300,2200,180,1200,700,2600,240])]), 0.5)
save('t05_tone_swipe',  sine(glide(1800,260,0.22),0.22)*np.hanning(int(SR*0.22)), 0.5)
save('t06_pin_ping',    at([(0, sine(1760,0.6)*dec(0.6,6)), (0.12, sine(1760,0.5)*dec(0.5,8)*0.35)], 0.7), 0.5)
save('t07_sub_drop',    sine(glide(70,32,0.7),0.7)*dec(0.7,4), 0.85)
save('t08_warm_chord',  sum(sine(f,1.0)*np.sin(np.pi*t(1.0)/1.0) for f in [262,330,392,523]), 0.5)
r = sum(sine(f,0.6)*dec(0.6,5) for f in [440,554,659]); save('t09_reverse_swell', r[::-1], 0.55)
save('t10_data_chirp',  at([(i*0.025, sine(2400+i*180,0.02)*dec(0.02,180)) for i in range(12)], 0.4), 0.4)
print('ok ->', OUT)

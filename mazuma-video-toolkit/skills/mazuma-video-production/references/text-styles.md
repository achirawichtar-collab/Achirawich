# Text design & decoration styles (Thai + English)

Use these instead of plain white text. Pick 2–3 styles per clip and keep them consistent — mixing every style looks cheap. All are CSS for the HTML overlay (Kanit loaded as `font-family:K`).

## Contents
1. Bilingual pairing rules
2. Style library (12 styles, with CSS)
3. Kinetic text animations (frame(t) snippets)
4. Which style for which moment

## 1. Bilingual pairing (Thai main + English kicker)
English adds a premium, "global brand" feel and helps search, but Thai must stay the message.
- Thai headline big (Kanit 800, 80–110 px); English kicker small above or below (Kanit 600, 28–36 px, UPPERCASE, letter-spacing 6–10 px, 70 % opacity, Aqua `#5AD1FF`).
- Good kickers: `WATER LAB`, `ARSENIC ALERT`, `ZONE CHECK`, `PURE WATER`, `HEAT · SAFE · SMART`, `FACT CHECK`, `STEP 01`.
- Never translate the whole sentence on screen — one or two English words max.
- Numbers/units in English digits (4500W, 0.0001 µm, 28×) — they read faster.

```html
<div class="kicker">ARSENIC ALERT</div>
<div class="big">สารหนู<b>ไหลไปถึงไหนแล้ว?</b></div>
```
```css
.kicker{font-weight:600;font-size:32px;letter-spacing:9px;color:#5AD1FF;opacity:.8;text-align:center}
```

## 2. Style library

| # | Name | Use for | CSS core |
|---|---|---|---|
| 1 | **Aqua Glass Pill** | labels, chips | `background:rgba(7,17,29,.62);backdrop-filter:blur(6px);border:2px solid rgba(90,209,255,.45);border-radius:22px` |
| 2 | **Highlight Bar** | one keyword | `b{background:linear-gradient(transparent 58%,#FFD23F 58%);color:#fff;padding:0 6px}` |
| 3 | **Gradient Fill** | hero title | `background:linear-gradient(180deg,#fff 30%,#5AD1FF);-webkit-background-clip:text;color:transparent` |
| 4 | **Outline Stroke** | big numbers | `color:transparent;-webkit-text-stroke:4px #fff` (fill animates in later) |
| 5 | **Neon Glow** | danger / CG scenes | `color:#fff;text-shadow:0 0 12px #ff3b30,0 0 40px #ff3b30` |
| 6 | **Water Shine** | product names | gradient text + moving `background-position` sweep (see §3) |
| 7 | **Stamp** | ✅ / ❌ verdicts | rotated −10°, 18px border, scale 2.6→1 in 0.12 s |
| 8 | **Ticker** | news facts | red bar, white text scrolling `translateX(-u*260px)` |
| 9 | **Lower Third** | places, people, sources | left yellow/red 12px border, title + small subtitle |
| 10 | **Counter** | stats (28×, 94 คน) | 300 px digits, eased count-up, slight shake while counting |
| 11 | **Split Colour** | comparisons (UF vs RO) | two words, two colours, divider `/` in Aqua |
| 12 | **Typewriter** | coordinates, HUD data | monospace-ish Kanit 600 + blinking caret |

Readability rules: shadow `0 0 30px rgba(0,0,0,.9), 0 6px 0 rgba(0,0,0,.5)` on any text over footage; keep inside y 200–1600 (TikTok UI covers the bottom/right); max ~12 Thai words per screen.

## 3. Kinetic animations (deterministic, inside `frame(t)`, `u` = time since shot start)
```js
// Pop-in with blur + letter-spacing collapse (signature title entry)
const k=Math.min(1,u/0.32); el.style.opacity=k;
el.style.transform=`scale(${1.25-0.25*(1-Math.pow(1-k,3))})`;
el.style.letterSpacing=`${(1-k)*16}px`; el.style.filter=`blur(${(1-k)*10}px)`;
// Word-by-word reveal (split words into <span>)
spans.forEach((s,i)=>{const p=Math.min(1,Math.max(0,(u-i*0.08)/0.2)); s.style.opacity=p; s.style.transform=`translateY(${(1-p)*40}px)`;});
// Water shine sweep across text
el.style.backgroundImage='linear-gradient(110deg,#fff 40%,#5AD1FF 50%,#fff 60%)';
el.style.backgroundSize='300% 100%'; el.style.backgroundPosition=`${100-((u*60)%200)}% 0`;
// Glitch (danger only): RGB split jitter
const j=Math.floor(t*20)%3; el.style.textShadow=`${(j-1)*14}px 0 #00e5ff,${(1-j)*14}px 0 #ff3b30`;
// Slide-in lower third with overshoot
const b=1+2.9*Math.pow(Math.min(1,(u-.1)/.35)-1,3)+1.9*Math.pow(Math.min(1,(u-.1)/.35)-1,2);
el.style.transform=`translateX(${(1-b)*-800}px)`;
```

## 4. Which style when
- Hook (0–3 s): Gradient Fill or Neon Glow title + English kicker, word-by-word or blur pop-in.
- Facts/stats: Counter + Lower Third source ("ข้อมูล: กรมควบคุมมลพิษ").
- Places: Lower Third with 📍.
- Product: Water Shine name + Aqua Glass Pill spec chips.
- Verdicts: Stamp.
- CTA: Highlight Bar on the action word + bouncing pill (💬 คอมเมนต์ / 🛒 ตะกร้า).

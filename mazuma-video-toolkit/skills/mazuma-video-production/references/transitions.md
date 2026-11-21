# Transitions between shots — picture + sound together

A cut feels "pro" when the picture move and its sound happen on the same frame. Every transition below has a visual recipe and a matching sound from `scripts/transition_sfx.py` (tonal, no wind/noise — Tar dislikes whoosh noise). Use a different transition sound at each cut; never the same one twice in a clip.

## Contents
1. Rules
2. Transition library (visual + sound)
3. ffmpeg recipes (between background clips)
4. Overlay recipes (HTML, on top of hard cuts)
5. Timing

## 1. Rules
- Default is a hard cut on a voice pause. Add a styled transition only at section changes (hook → content, zone → zone, problem → solution, → CTA), about every 3–5 shots, or the clip feels like a template.
- Transition sound starts 2–4 frames *before* the cut and peaks on the cut.
- Duration 0.2–0.45 s. Longer feels slow on TikTok.
- Match motion direction: things flowing downstream move left→right / top→bottom.

## 2. Library
| Name | Visual | Sound (`transition_sfx.py` id) | Best for |
|---|---|---|---|
| Water Ripple | radial ripple distortion + 0.2 opacity white flash | `t01_drop_ripple` (droplet + low swell) | brand signature, section change |
| Zoom Through | crash-zoom into object, next shot starts zoomed-out | `t02_rise_hit` (fast sine rise → soft thud) | glass → river, map → place |
| Light Sweep | diagonal aqua light bar sweeps across | `t03_shimmer_sweep` (bright arpeggio) | product reveal |
| Glitch Cut | 3 frames RGB split + offset slices | `t04_digital_glitch` (stepped square blips) | danger/news |
| Whip Pan | 6-frame horizontal motion blur | `t05_tone_swipe` (pitch glide, no noise) | place → place |
| Iris Pin | circle mask closes on a map pin, opens on footage | `t06_pin_ping` (radar ping) | map → location footage |
| Dip to Navy | 0.25 s dip to #07111D | `t07_sub_drop` (deep sub thump) | serious fact → solution |
| Film Burn | warm light-leak overlay | `t08_warm_chord` (soft chord swell) | emotional/family scenes |
| Match Cut | shape matches across cut (glass ↔ river, pot ↔ sun) | `t09_reverse_swell` (reversed swell) | storytelling |
| Data Wipe | scan line wipes, HUD numbers flicker | `t10_data_chirp` (fast tick burst) | CG map stages |

## 3. ffmpeg recipes (background layer)
Replace `concat` with `xfade` where a styled transition is wanted:
```
[v0][v1]xfade=transition=fadeblack:duration=0.25:offset=OFF   # Dip to Navy (then colour-grade the black to navy)
[v0][v1]xfade=transition=wipeleft:duration=0.3:offset=OFF      # Data Wipe
[v0][v1]xfade=transition=zoomin:duration=0.35:offset=OFF       # Zoom Through
[v0][v1]xfade=transition=hblur:duration=0.25:offset=OFF        # Whip Pan
[v0][v1]xfade=transition=circleclose:duration=0.35:offset=OFF  # Iris Pin
[v0][v1]xfade=transition=pixelize:duration=0.2:offset=OFF      # Glitch-ish
```
`OFF` = length of the first segment minus the duration. Each xfade shortens the total by `duration` — recompute shot start times (or pad each segment by the duration) so voice/captions stay in sync.

## 4. Overlay recipes (HTML, works with hard cuts — simplest, keeps timing exact)
```js
// call with c = time since the cut (negative before it)
function ripple(c){ const k=1-Math.min(1,Math.abs(c)/0.25); flash.style.opacity=k*0.2;
  ring.style.transform=`scale(${0.2+Math.max(0,c)*6})`; ring.style.opacity=Math.max(0,1-Math.max(0,c)/0.4); }
function lightSweep(c){ bar.style.transform=`translateX(${-1200+Math.max(0,c+0.15)*5200}px) rotate(18deg)`; }
function glitch(c){ const on=Math.abs(c)<0.1; layer.style.filter=on?'url(#rgbsplit)':'none'; layer.style.transform=on?`translateX(${(Math.floor(c*90)%3-1)*24}px)`:'none'; }
function dataWipe(c){ scan.style.top=`${(c+0.3)/0.6*1920}px`; scan.style.opacity=Math.abs(c)<0.3?1:0; }
```
Keep white flashes ≤ 0.3 opacity and ≤ 0.1 s (a stronger flash washed out a shot before).

## 5. Timing in the build script
- Store `tr` per shot in the timeline (`"tr":"ripple"`), pick the matching sound id, and `adelay` it to `cut_time - 0.08 s`.
- Keep transition SFX at 0.3–0.45 volume, under the voice (voice must stay clear).

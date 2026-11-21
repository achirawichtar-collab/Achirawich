---
name: mazuma-video-production
description: Formats (news-channel, viral selling, CG explainer, mini-drama), brand look, text styling (Thai + English), transitions with matched sound, and production workflow for Mazuma TikTok videos (water purifiers, RO, water heaters, air-con explainers) made for Tar. Use this whenever Tar asks to make, edit, re-render, storyboard, or improve a Mazuma clip — คลิป, วิดีโอ, storyboard, สคริปต์พากย์, เสียงเอฟเฟกต์, CG, แผนที่, ฟอนต์, เอฟเฟกต์ — even if he only says "ทำวิดีโอมาเลย" or sends a screenshot with a complaint. It holds the Mazuma signature style so clips do not look like everyone else's, plus every lesson learned from his past feedback (voice, pronunciation, SFX, cutouts, fact-checking).
---

# Mazuma Video Production

Tar makes vertical TikTok clips (1080x1920, ≤60–70 s) for Mazuma using his cloned voice. Pair this skill with `mazuma-tiktok-content` (ideas, hooks, captions); this one is about *how the clip looks and sounds* and how to produce it without repeating past mistakes.

Why this skill exists: generic TikTok templates (same fonts, same whoosh SFX, same stock B-roll) make a brand invisible. Mazuma clips should be recognisable in one second, and Tar has already told us — many times — what he dislikes. Re-learning that every session wastes his time and tokens.

## 1. The Mazuma signature (use in every clip)

Think "Water Lab": calm, credible, a little cinematic. Not shouty, not cartoon.

**Colour tokens**
- Deep Navy `#07111D` (backgrounds, CG void) · Aqua `#5AD1FF` (water, HUD lines, highlights) · Pure White text
- Accent Yellow `#FFD23F` (key numbers/keywords only — one per screen)
- Status colours only when they carry meaning: Red `#FF3B30` danger · Orange `#FF9F0A` watch · Green `#30D158` safe
- Footage grade: slight teal shadows / warm highlights + soft vignette (ffmpeg `colorbalance=rs=-.04:bs=.06:rh=.06:bh=-.05,eq=contrast=1.08:saturation=1.08`, `vignette=PI/4.5`).

**Typography** (fonts in `../vid/package/files/` — Kanit 400/600/800)
- Headline: Kanit 800, 76–110 px, max 2 lines, text-shadow for legibility. One highlighted word in Yellow (or status colour).
- Captions: Kanit 600, ~50 px, white with dark stroke, at y≈1450 — always present while voice plays (Tar watches with sound off too).
- Labels/chips: Kanit 800 in dark translucent pills with a coloured left border.
- Never stack a headline over a busy area of the map/product; move the camera or shorten the headline instead (Tar flagged overlaps).

**Signature elements** (these are what make it "Mazuma", reuse them)
- Brand bug "MAZUMA" top-right, letter-spaced, 80 % opacity.
- Cinematic frame for data/explainer clips: thin letterbox bars, aqua corner brackets, slow scan line, film grain, small coordinate/"As MONITOR" HUD text. Product/soft-sell clips use the frame without the HUD text.
- Water language for transitions: ripple/flash cut, droplet pop, light sweep across products. Avoid generic swipe/whoosh packs.
- Products: real Mazuma photos only (mazuma.co.th, or the Google Drive folders Tar shares), background removed cleanly (see §4), large and centred, spec chips under them, slow float + glow.
- Credits on every borrowed visual: "Pexels", "ภาพ: Thai PBS", "ภาพดาวเทียม: NASA Blue Marble", "ภาพสินค้า: Mazuma".

**Formats** — read `references/reference-formats.md` first and pick one: A news-channel style (Thairath-like headline bar, facts, sources), B viral selling story (TikTok Shop hook→problem→product→proof→basket), C CG explainer, D mini-drama.

**Text design & bilingual styling** — read `references/text-styles.md` for the 12-style library (Aqua Glass Pill, Highlight Bar, Gradient Fill, Neon Glow, Water Shine, Stamp, Counter…), Thai headline + small English kicker pairing (e.g. `ARSENIC ALERT`, `WATER LAB`), and kinetic animation snippets. Pick 2–3 styles per clip and keep them consistent.

**Transitions** — read `references/transitions.md`: picture move and its sound land on the same frame. Hard cuts on voice pauses by default; styled transitions (Water Ripple, Zoom Through, Light Sweep, Data Wipe, Iris Pin…) only at section changes. Sounds come from `scripts/transition_sfx.py` (t01–t10, tonal, no noise), each used once per clip.

**Distinctiveness check** before rendering: would this frame still look like Mazuma with the logo covered? If it could be any brand's clip, add one signature element (aqua HUD, water transition, product glow, yellow keyword).

## 2. Sound

- **Voice**: Speko `audio_synthesize`, voice `aa5754f6-d25d-4c2a-8bf7-9eb47d59ebf6`, provider cartesia, `intent.language=th`, **`speed: 1.15` at synthesis** (do not speed up afterwards with `atempo` — that made the voice hoarse). Light chain only: `highpass=f=80, equalizer=f=180:g=1, acompressor ratio 2`. No heavy denoise/de-ess.
- **One sentence per synthesis call**; join with 0.25–0.3 s gaps (0.4 s inside a two-part sentence). When a line still sounds rushed, split it into two calls with a real pause — Tar notices run-together speech immediately.
- Pronunciation fixes are in `references/pronunciation.md` — check it before writing any voice line, and add new fixes there.
- **SFX**: tonal, synthesised, every shot gets a *different* sound (Tar: "ห้ามซ้ำกัน"). Use `scripts/sfx_palette.py` (x01–x31) + `scripts/sfx_palette_extra.py` (x32–x41); add new generators rather than reusing. Never wind/noise whooshes or crackle — he dislikes them.
- Optional low 55 Hz drone bed at ~3.5 % for cinematic data clips.

## 3. Workflow (what Tar expects, in order)

1. **Research & fact-check first** for any health/safety claim (Firecrawl search: กรมควบคุมมลพิษ, กรมควบคุมโรค, กปน., Thai PBS, THE STANDARD, mazuma.co.th). Prefer the latest official numbers; soften speculative claims ("ควรเฝ้าระวัง", "อาจ"), never "ปลอดภัย 100%", never "กำจัดได้หมด" — say "ช่วยลด". Tell Tar plainly when his source text overstates something.
2. **Storyboard image first** (HTML → PNG grid, real frames from the actual footage) with voice line, visual effect, unique SFX and credit per shot, plus the full script table in chat. Wait for approval unless he says "ทำมาเลย".
3. **Assets**: new footage each clip — Tar said "ห้ามใช้รูปซ้ำ". Keep `references/used-assets.md` updated and check it before choosing footage. Pexels download `https://www.pexels.com/download/video/<id>/`; news photos need the host allowed in the environment.
4. **Build**: python `build.py` (voice timeline → captions → ffmpeg background per shot → SFX mix) + HTML overlay with deterministic `window.frame(t)` + Playwright renderer piping PNG frames into ffmpeg (crf 15–16). For 3D/CG use three.js (`npm i three@0.160.0`) in an iframe — see `scripts/cg_satellite_map.html` (real NASA globe → satellite Thailand with province borders, realistic ocean shader, extruding provinces, light pillars, Thai labels, As atom).
5. **Check stills of every shot** before the full render (one contact sheet), fix overlaps/dark frames, then render in the background and send the file with `SendUserFile` (status proactive) — Tar asked to be notified when renders finish.
6. Report briefly in Thai: what changed, what to listen for (new pronunciations), anything unverified.

## 4. Lessons from Tar's feedback (don't repeat these)

- Product cutouts: white halos and grey shadows around rails/hoses were rejected twice. Use `scripts/product_cutout.py` (dark-key for dark products, border-flood + hole-fill for silver, colour decontamination, remove QR/TIS logos). Zoom-check edges on a dark background before use.
- Use the newest product photos (e.g. Miracle new faceplate from Drive) — ask if unsure which model a photo is; never guess a model name or wattage.
- White full-screen flashes washed out a shot — keep cut flashes ≤ 0.3 opacity for ≤ 0.1 s.
- Too many words in the first 3 s; the hook must be one punchy question + one visual.
- When Tar says "ดูน่าเบื่อ/ว้าวกว่านี้", raise production value (CG, real satellite, camera moves) rather than adding more text.
- He prefers "real" over stylised: real satellite map, real sea, real footage; graphics should sit on top of reality.
- Keep explanations of what changed short; he is often on a phone.
- He worries about token use: batch synthesis calls in parallel, reuse pipelines, avoid re-reading large files.

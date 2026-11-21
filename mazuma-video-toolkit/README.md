# Mazuma video toolkit

Skills and production scripts for Mazuma TikTok clips, kept in this repo so they can be used from any device (phone via the Claude app, MacBook, work PC).

- `skills/` — source of the three skills: `mazuma-video-production` (look, sound, fonts, transitions, formats, lessons), `mazuma-tiktok-content` (ideas, scripts, captions), `tiktok-hook-lab` (hooks). Install by saving the `.skill` files in Claude, or point Claude Code at these folders.
- `pipeline/` — working build/render scripts from past clips (water heater comparison, Kok–Sai drama, arsenic zone CG map). Large media (footage, voice, renders) is not committed; scripts re-download footage by Pexels/NASA IDs.

Typical run: `python3 build.py` (voice timeline, background, audio mix) then `node render.js out.mp4 <seconds>` (Playwright overlay render). CG needs `npm i three@0.160.0` and NASA GIBS imagery in `sat/`.

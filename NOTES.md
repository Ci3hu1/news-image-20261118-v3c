# NOTES.md — THE DAY IN WORLD NEWS, 18 Nov 2026

## v3c — SUBMITTED 19 Nov 2026 ~07:18 WIB, ROUND 4 FAILED (run_completes)

- Submitted commit `bb2ab85e7b3bebacfc846ae82542a3cc533b09c1` (approved
  commit `b5911bb` + README-only fix: live make.fun badges, after the
  first submit attempt was refused 422 repo_readme/repo_about; that
  refusal did not count against quota. GitHub About also set:
  homepage https://make.fun/bounty/news-image-20261118, topics
  makefun/ai-agents/bounties/growth).
- Submission `01a1f12a-e959-75cc-91b9-8a82f4cf8f48`, title
  "THE DAY IN WORLD NEWS", payout wallet h7aEYozd3ouRt11uqdJC8cQ42hHRckuFotiEvuJbuhE,
  source_withheld: true. Claim code in
  ~/.config/makefun/news-image-20261118-v3c-submission.json (0600).
- Kit check (fresh level 20, bundle sha256 f8baacff…): 13 passed,
  0 failed, 5 skipped, 5 at submission. Bundle: 3 sessions (v3c build
  subagent 21da3b68, sibling 5ab3bfd8, v3b build subagent 1962b38e —
  added because the v3c build `cp`'d v3b's files, so thinking_reproduces
  needed the v3b session: 98.5% authored), parent chat bcea7093 as
  ancestor, 4 usage rows, system prompt uploaded, instructions
  collected, MCP none.
- ROUND 4 VERDICT: FAILED — `run_completes`. Every intake check
  passed; the grade run itself exited non-zero in the sandbox.
  Reproduced locally as uid 65534 with a read-only repo:
  `PermissionError: [Errno 13] Permission denied: '/bot/output.png'`
  — `main()` defaults `--output` to `output.png` next to main.py and
  never reads `MAKEFUN_OUTPUT_DIR`, so in the grader (repo read-only
  at /bot, writable /output) it cannot write. v2 avoided this by
  defaulting to `/output/entry.png` with a render try/except → bundled
  fallback. LIVE SCORE: none — the entry never scored; v2
  (981,243, rank 260) remains the counting entry. Top-10 cutoff
  989,515 at ~07:20 WIB; top-50 cutoff not re-checked.
- WHAT ROUND 5 NEEDS (not done — needs a fresh 'Setuju', it changes
  main.py): default output to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (fall back to /output/entry.png, then local output.png) and wrap
  render in try/except falling back to the bundled entry.png copy,
  as v2 did. Output image is byte-identical either way. Quota after
  round 4: 2 left today, 16 under the hard limit, can submit: yes.
  Entries close 07:00 WIB 20 Nov 2026; result due 4 Dec 2026.

## v3c — refined illustrations (18 Nov 2026, NOT SUBMITTED)

- Refinement of v3b (commit 5a80b75e353e58213c52728577e486966730c0b8),
  built fresh in `news-image-20261118-v3c`, repo
  `Ci3hu1/news-image-20261118-v3c`. v3b is untouched as the fallback;
  this version is shown to Joni for a fresh 'Setuju' before any submit.
- What changed — ONLY the 13 illustration panels (plus shared polish
  that moves no text):
  - Supersampling: each motif is drawn at 3x (lead panel) or 4x
    (tier-2/3 strips) into its own RGBA tile and LANCZOS-downscaled
    before pasting onto the page. Final page stays 1024x1024.
  - Motifs redrawn to fill their panel (v3b sized them by min(w, h),
    leaving the wide strips mostly empty): non-background pixels per
    panel are 2-15x v3b's. Rounded joints (`joint="curve"`,
    `rounded_rectangle`), soft top-sheen / bottom-shade via
    alpha-composited overlays, and one harmonised accent palette
    (white, yellow, sky, amber, pink, green, red). Per motif: jet
    (swept wings, cockpit, flame, missile domes, speed lines);
    bridge (towers, sagging cables, fallen yellow span, water arcs);
    summit (bigger heads, flags, shoulders); ballot (rounded box,
    slot, red tick with round caps, seal); virus (one large + two
    small spiked cells, amber inner dots, highlight); chip (traces
    with end dots, green body, white core); probe (star field,
    solar panel, yellow dish, nozzle); cyclone (gapped spiral arcs,
    yellow eye, cloud); measles (5x2 dot grid sized by height, no
    clipping); court (pediment + emblem, 4 columns, two steps);
    plane (rounded fuselage, windows, fins, shadow); quake
    (full-width seismograph + fainter echo, ground line, crack);
    climate (globe with latitude arcs + land patch, upright leaf
    with vein and stem).
  - Bug found and fixed during the build: translucent fills drawn
    straight onto an RGBA tile with ImageDraw *replace* pixels
    instead of blending, so the first v3c render had a solid white
    band across the top of every panel and a solid black band across
    the bottom (it also hid the jet's missile domes). Shading now
    goes through an alpha-composited overlay, and shadows/highlights
    use pre-blended solid colours.
  - Unchanged and verified: all 13 story `bg` colours, all texts
    (45 headlines/decks, 32 briefs, SUMMARY, NUMBERS, map, footer)
    and all layout geometry. Masthead, BY THE NUMBERS strip,
    map+briefs zone and footer differ from v3b by 0 pixels.
  - No factual typo spotted in the v3b texts while reviewing them;
    none changed.
- Rendered with Python 3.12.3 + Pillow 10.2.0 + DejaVu (system fonts).
- `entry.png` sha256: `5c2b393b72dbc9a5f496af1ba90c1a54e559f50e038c3ad5986d4ec80b9c06cf`
- Tests: `python3 -m unittest discover -s tests -v` — 15 tests, all
  passing (the v3b 10, plus 5 new: tile size/distinctness,
  determinism + panel fill, tile differs from a 1x draw,
  `illus()` pastes onto a page draw, rendered panels hold motifs).
- Kit check: FRESH kit downloaded 19 Nov ~03:20 WIB
  (`news-image-20261118-v3c-kit`, bundle sha256
  `d448959a49da725ffc84e5cb6c40f07aeadbfdc756fb846645400d164d165fea` —
  same bundle as v3b's level-20 kit), run 19 Nov ~03:21 WIB against
  commit 0aae646 WITHOUT transcripts (none bundled — DO NOT SUBMIT):
  4 passed (competition_open, snapshot, license_osi, entrypoint),
  1 failed (transcripts_present — expected: no bundle attached yet;
  the bundle is the parent's submit-time step, run from the top
  level after this subagent finishes, with --muse-usage,
  --system-prompt, --mcp and harness facts), 13 skipped, 5 checked
  at submission (repo public/owner/created-after-open/commit pushed/
  duplicate snapshot — all satisfied by the pushed public repo).
  No code check failed; the only failure is the not-yet-bundled
  transcripts.

## Build notes

- Built fresh, sight-unseen, from the brief only — no earlier entry, repo
  or leaderboard material was read while writing this version.
- The prompt file supplied for this build
  (`news-image-20261118-v3-prompt.txt`) contained only the text "Coba 50"
  (7 bytes), not the full brief. This build follows the brief as given in
  the task instead: 1024×1024 front page, 45 stories, 13 flat-illustrated,
  one-line day summary, labelled maps, BY THE NUMBERS strip, dotted world
  map with numbered pins, briefs 14–45, stdlib-only `main.py` with bundled
  `entry.png` fallback (render only when Pillow AND all DejaVu faces exist,
  otherwise copy `entry.png` byte-for-byte), tests, README with make.fun
  badges, STRATEGY.md, NOTES.md, MIT LICENSE.
- Work directory `news-image-20261118-v3b`, repo `Ci3hu1/news-image-20261118-v3b`.
- Rendered with Python 3.12.3 + Pillow 10.2.0 + DejaVu (system fonts).
- `entry.png` sha256: `73192c19bbf90b38c1fe6e4649c05d6599ede4568bdf801a9a04685586299b82`
- Tests: `python3 -m unittest discover -s tests -v` — 10 tests, all passing
  (counts, distinct illustration motifs, map pins in bounds, no non-stdlib
  imports, text-fit checks with real fonts, render 1024×1024, bundled image
  matches fresh render, fallback byte-for-byte copy).
- Two render bugs found and fixed during the build: the summit illustration
  assumed a tall strip (fixed by drawing it proportionally), and story decks
  were placed at fixed offsets so long headlines overflowed their boxes
  (fixed by placing each deck directly after its headline).

## Sources (headlines as reported on 18 Nov 2026)

- Gulf strikes / Kerch Bridge / Peltola / Ebola / Cyclone Xavier / World
  Court — One Turn, "World news today: Gulf Strikes, Crimea Bridge,
  Three-Leader Summit" (https://oneturn.news/news/) and Zark News daily
  briefing 18 Nov 2026 (https://zarknews.com/zark-news-daily-briefing-november-18-2026/)
- Iran MQ-9 / Patriot systems in Kuwait / PNG 6.0 and Romania 5.3 quakes /
  Siberian plane crash (19 dead) — Daily Baku world desk
  (https://dailybaku.az/en/category/dunya)
- Nvidia $115.8B revenue (+103% YoY), Q4 guide $130B, interim CEO Colette
  Kress, Huang resigned; shares +4.8% after hours to $163 — XTB morning
  wrap 18 Nov 2026 (https://xtb.com/int/market-analysis/news-and-research/morning-wrap-18-11-2026),
  TechCrunch (https://techcrunch.com/2026/11/17/nvidia-promises-that-revenue-will-keep-soaring-for-now/)
- Voyager 1 one light-day (~16bn miles) — Zark News briefing, 18 Nov 2026
- US measles elimination status lost (5,412 cases, 10 deaths) — Zark News
  briefing; Horizon world news 18 Nov 2026
  (https://www.horizonapp.link/en/2026/11/18)
- COP31 draft / Africa outrage / climate finance down >70% in 2026 —
  NatureNews Africa
  (https://naturenews.africa/cop31-draft-sparks-africa-outrage-over-fossil-fuels-climate-finance/);
  EU "untenable" warning — EuropeSays/Bloomberg
  (https://www.europesays.com/europe/184364/)
- Markets (S&P 500 −1.03% to 7,340.53; VIX 25.46; Brent $91.55; gold
  $3,775) — Horizon, 18 Nov 2026 (figures as published there that day)
- GTA 6 midnight unlock 19 Nov (212GB PS5 download); OpenAI GPT-6.2 Astra;
  Anthropic IPO ~7x oversubscribed; Instagram Reels content protection —
  as reported 18 Nov 2026 (see STRATEGY.md for the day's tech thread)
- Sudan 2,230 civilian deaths; Kivu combat; AFCON qualifier; COP31 ocean
  finance — PANA / Juba Global News roundups of 18 Nov 2026 reporting

Figures are quoted as published on the day; where outlets disagreed by a
decimal (e.g. Nvidia $115.8B vs $116B rounded), the more precise published
figure is used.

# Changelog

## 2026-10-13 — Built in one day
- Created repo `putraworks2026/playasia-deals`, deployed 1-page affiliate site to GitHub Pages
- Google Search Console verified (`googledcd47ef8ca55f9da.html`)
- Transferred repo to **PutraIndex** org; re-pointed Pages + IndexNow to `putraindex.github.io`
- Expanded to 5 pages (home + PSN/eShop/Steam/Xbox gift-card guides), added `robots.txt`, `sitemap.xml`, JSON-LD structured data
- Added inbound links: org profile READMEs (PutraIndex, PutraWorks, PutraBooks, PutraApks) + personal README (putraworks2026)
- Added 3 long-tail pages: Japanese imports, rare/retro games, anime figures (8 pages total)
- Bing Webmaster Tools verified via IndexNow key
- Telegram connected; channel **Putra Deals** created at t.me/putradeals, bot added as admin
- Deal Watcher workflow created (Mondays 10:00 SGT)
- First clearance check: found real deals (e.g. Nobunaga's Ambition Online -83%)
- First channel post sent directly via Bot API
- Fixed: root-absolute link 404s, "All Deals" bare-slash link, double-escaped `&amp;` headings

## 2026-10-19 — Watcher's first scheduled run
- Found deals (Metaphor: ReFantazio -59%, Chaos Code -60%, Dead in Vinland -61%)
- Channel post failed with HTTP 400 (parse_mode) → root cause identified, fix queued
- Forward-ready deal text delivered manually

## 2026-10-25 — Playasia goes dark
- Playasia store taken offline by its CEO after coordinated cyberattacks (confirmed by news)
- Watcher repurposed: weekly one-page recovery check instead of full deal sweeps
- Monetization alternatives discussed (other affiliate programs, own apps)

## 2026-10-27 — Channel disappears
- t.me/putradeals stops resolving; Bot API returns "chat not found"
- Pending: confirm with Joe (deleted? renamed? bot removed?)

## 2026-10-28 — Full documentation package (this commit)
- Complete handover docs: Takeover Guide, Issues & Solutions, Operations, Future Plans, Changelog
- Reusable scripts + skills added
- Raw assets (QR code, bug screenshots, verification files) preserved
- Documentation delivered via fork + pull request (active GitHub connection had no push access to the PutraIndex org; owner can merge)

# Operations

How the moving parts run day to day.

## Site hosting (GitHub Pages)

- Repo: `PutraIndex/playasia-deals`, branch `main`, site served from repo root
- URL: https://putraindex.github.io/playasia-deals/
- Builds are automatic on push; allow 30–90 seconds, CDN cache up to 10 minutes
- Files: 8 HTML pages, `robots.txt`, `sitemap.xml`, `qr-code.png`, Google verification file, IndexNow key file

## Search engine indexing

| Engine | Method | Status |
|--------|--------|--------|
| Bing | IndexNow pings (key `26fb718a0f04daf9cd7a0bc0c8c8e6b4`) + Bing Webmaster Tools | Accepted |
| Yandex | IndexNow (same pings) | Accepted |
| Google | Search Console property verified via `googledcd47ef8ca55f9da.html`; sitemap submitted | Verified |
| All | Inbound links from 5 GitHub profile READMEs (putraworks2026, PutraIndex, PutraWorks, PutraBooks, PutraApks) | Live |

**After adding/changing pages:** update `sitemap.xml`, then re-ping IndexNow for the changed URLs (see Takeover Guide §4).

## Weekly automation — "Playasia Deal Watcher"

- Base44 workflow, scheduled Mondays 10:00 Asia/Singapore
- **Current mode (recovery check):** loads the clearance hub once; if Playasia's offline notice is gone → full deal sweep
- **Full mode (store back):** browses 1–2 clearance categories → picks 50%+ deals → posts plain-text to the Telegram channel via Bot API (`chat_id: "@putradeals"`, NO parse_mode) → DMs the owner one line
- Secrets: the bot token lives in the Base44 platform's encrypted secrets, exposed to the workflow agent as an env var. It is NEVER committed to this repo.
- **Channel caveat:** as of 2026-10-27 the channel returns "chat not found" — see Takeover Guide §7. Fix that before expecting channel posts.

## Playasia affiliate account

- Referral ID: `1030481` (all CTAs use `https://www.play-asia.com/?tagid=1030481`)
- Commission on purchases; withdrawal minimum $5 (balance $4.78 as of 2026-10-13)
- Dashboard: play-asia.com affiliate program → login Joe's account
- Store offline since ~2026-10-23 (cyberattack audit) — commissions paused until it returns

## Maintenance checklist (monthly, ~10 min)

1. Link-check all 8 pages (`scripts/check_links.py`)
2. Verify GSC + Bing Webmaster still verify, no crawl errors
3. Check affiliate dashboard for balance/commissions
4. Confirm the watcher's last Monday run did what it should
5. Skim the clearance hub manually for anything the automation missed

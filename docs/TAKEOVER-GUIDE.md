# Takeover Guide

Everything a new maintainer needs to run this project.

## 1. What this project is

A zero-budget affiliate funnel:

```
Search engines / Telegram  →  GitHub Pages site  →  play-asia.com/?tagid=1030481  →  commission
```

- **The site:** 8 static HTML pages (no build step, no framework, no dependencies)
- **The product:** Playasia.com referral commissions
- **The goal:** first $5 commission milestone for payout

## 2. Accounts and access you need

| Account | Why | Where |
|---------|-----|-------|
| GitHub (owner of PutraIndex org) | Push to this repo, manage Pages | github.com |
| Playasia affiliate account | Commission dashboard, withdrawal at $5 | play-asia.com affiliate program |
| Google Search Console | Indexing status (property verified) | search.google.com/search-console |
| Bing Webmaster Tools | Indexing status (verified via IndexNow key) | bing.com/webmaster |
| Telegram BotFather bot | Optional: post deals to a channel | The bot token is stored as an encrypted secret in the Base44 Superagent, NOT in this repo — never commit tokens |

**Verification file on the site:** `googledcd47ef8ca55f9da.html` (Google) and `26fb718a0f04daf9cd7a0bc0c8c8e6b4.txt` (IndexNow key — doubles as Bing verification).

## 3. Repo layout

```
/                     8 HTML pages, robots.txt, sitemap.xml, verification files
qr-code.png           QR code of the referral link (also referenced by pages)
README.md             Public face of the repo (contains the site link — helps SEO)
DOCUMENTATION.md      This documentation package index
docs/                 Guides below
scripts/              Deploy + maintenance scripts
assets/raw/           Original images (screenshots, QR, verification)
```

## 4. How to edit the site

1. Edit the HTML files in the repo root (each page is self-contained: inline CSS, no JS).
2. Every page shares the same nav block and footer — keep them in sync across all 8 pages.
3. Push to `main`. GitHub Pages auto-builds (takes 30–90 seconds).
4. After changing URLs, update `sitemap.xml` and re-ping IndexNow:
   ```bash
   curl -s -X POST https://api.indexnow.org/IndexNow -H "Content-Type: application/json" \
     -d '{"host":"putraindex.github.io","key":"26fb718a0f04daf9cd7a0bc0c8c8e6b4","urlList":["https://putraindex.github.io/playasia-deals/"]}'
   ```
5. Or use `scripts/push_all.py` (deploys files via the GitHub API in one commit).

## 5. Critical conventions learned the hard way

- **Internal links must be RELATIVE** (`psn-gift-cards.html`), never root-absolute (`/psn-gift-cards.html`). On a GitHub Pages project site, `/x.html` resolves to the domain root → 404.
- **Escape ampersands ONCE** (`&amp;`), never double-escape (`&amp;amp;` renders literally).
- **Playasia blocks curl with Cloudflare 403** — use a real browser for scraping. The browser check returning 403 does NOT mean the link is broken for humans.
- **The real clearance hub** is `https://www.play-asia.com/en/clearance/00/71365` (there is no `/deals` URL).

## 6. The automation (if you rebuild it)

The weekly watcher lived in a Base44 workflow ("Playasia Deal Watcher", Mondays 10:00 SGT):
1. Opens the clearance hub with browser automation
2. Picks 1–2 categories, waits ~4s for the JS product list to render
3. Filters for 50%+ discounts on notable titles
4. Posts plain text (NOT parse_mode=HTML — that caused Telegram API 400) to the channel
5. DMs the owner a one-line confirmation

As of 2026-10-25 it only checks whether Playasia's store is back online (the store went dark after cyberattacks, see CHANGELOG).

## 7. The Telegram channel (IMPORTANT — discontinued)

`@putradeals` was the deals channel, but as of 2026-10-27 the Bot API returns "chat not found" and t.me/putradeals no longer resolves — the channel was deleted, renamed, or the bot lost admin. **Confirm with Joe before any future channel posts.** To rebuild: create a channel, add the bot as admin, store the bot token as a secret, post via `api.telegram.org/bot<token>/sendMessage` with `chat_id: "@<channel>"`.

## 8. What "done" looks like

The affiliate goal: $5 commission balance → withdrawal. The site does the passive part (search indexing, backlinks from 5 GitHub profile READMEs). The active part is sharing the link where deal-hunters are — that was always the real bottleneck, not the tech.

# Playasia and Cloudflare — what works, what does not

Playasia sits behind Cloudflare. This page records exactly which approaches were tested, so nobody (human or agent) repeats a dead end.

**Bottom line: do not scrape Playasia from your own browser. Consume `feed/latest.json` instead.**

## What was tested

| Approach | Result | Notes |
|---|---|---|
| `curl` (any headers/UA) | **Fails, always** | 403 plus a ~5KB Cloudflare block page. Same for `/deals` and every product URL. |
| Browser automation via Browserbase (this agent) | **Works** | Real browser session passes the check and renders the clearance listing. This is the only verified scrape path. |
| A self-hosted Chrome inside another agent's sandbox (Solene) | **Fails** | Interstitial loops forever with a non-interactive Turnstile verdict on that browser/IP. |
| Driving that same browser over CDP | **Fails, and cannot work** | CDP attached successfully; the problem is there is no widget to click. |
| Asking a human to tick the "Verify you are human" checkbox | **Nothing to tick** | No checkbox exists in the page DOM. |

## The CDP evidence (once, so it is never re-attempted)

Solene's browser was launched with `--remote-debugging-port=0`, so the real port is in the `DevToolsActivePort` file rather than 9222/9223/9515. That was located and used (Chrome 154, `navigator.webdriver` false), and CDP attached to both the page and the Turnstile iframe:

- page DOM: **0 iframes, 0 `input[type=checkbox]`** (shadow roots walked)
- the Turnstile iframe body stayed **empty for ~70s** on "Checking your Browser…"
- `Input.dispatchMouseEvent` had no target
- `cf_clearance` (426 bytes, secure) and `cf_chl_rc_ni` both exist, yet `Page.reload` left the title on "Just a moment…"

That combination means a **non-interactive verdict** against that browser fingerprint and IP: Cloudflare decided, and there is no user action that flips it. Automation cannot clear it because there is nothing being asked.

## The working pattern

Scrape once, publish, consume:

1. **The scraping agent** (Browserbase session, which passes) reads the clearance hub `https://www.play-asia.com/en/clearance/00/71365`, picks the standout deals, and commits them to `feed/latest.json` on `main`.
2. **Any consumer** fetches the static file — `https://raw.githubusercontent.com/PutraIndex/playasia-deals/main/feed/latest.json` — which sits on GitHub's CDN and has no Cloudflare in front of it.
3. Consumers must check `generated_at` and skip posting when the snapshot is older than 10 days, so a broken scraper fails visibly instead of republishing stale prices.

Schedule the scrape earlier than the post (currently 09:00 and 10:00 SGT Mondays) so the feed is fresh when it is consumed.

## Related traps

- **Referral links returning 403 to a bot do not mean they are broken.** Playasia blocks automated fetches of outbound links while humans click through fine. Never "fix" a working affiliate link because a `curl` check returned 403.
- **`/deals` does not exist.** The clearance hub is `/en/clearance/00/71365`.
- **Cookies expire.** Even a browser that once passed will eventually be challenged again, which is the other reason the feed beats live scraping for anything on a schedule.

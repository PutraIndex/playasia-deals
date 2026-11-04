# Issues and Solutions (step by step)

Every problem encountered during the build, and exactly how it was fixed.

## Issue 1 — All GitHub credentials rejected (401 Bad credentials)

**Symptom:** Every token failed: the platform connector token (`gho_...`), the stored `.env` token, and the Personal Access Token saved in the app's Secrets entity.

**Steps that fixed it:**
1. Re-authorized the GitHub connector through the platform (request_oauth_authorization).
2. Re-fetched the token AFTER re-auth (`get_connector_token` again — the sandbox keeps the old value otherwise; also do not `source .env` afterward, it overwrites the fresh token with the stale one).
3. Later, when the connector account changed (putraworks2026 → johanjumahat), the same 401 pattern appeared; re-authorization + a fresh token fetch resolved it again.

**Lesson:** a connector can report "Authorized" while its tokens are dead. Verify with `curl https://api.github.com/user` before building anything on it.

## Issue 2 — Repo transfer to org failed (403: OAuth app not authorized)

**Symptom:** `POST /repos/.../transfer` returned "The OAuth application is not authorized for access to PutraIndex."

**Fix:**
1. Org owner opens `github.com/organizations/PutraIndex/settings/oauth_application_policy`
2. Approve the pending request from the app (or disable the restriction)
3. Retry the transfer — succeeded immediately.

## Issue 3 — After transfer, API calls flapped 404

**Symptom:** Right after transferring repos to orgs, content PUTs and PATCHes intermittently returned 404, then succeeded later with no changes.

**Fix:** Wait 30–60 seconds and retry. GitHub replication lag, not a real failure. Also: PATCH on repo settings (description) requires **admin** permission — a push-only token gets 404, not 403.

## Issue 4 — Sitemap "not valid" in Google Search Console

**Symptom:** GSC rejected the sitemap with "Invalid sitemap address" (screenshot: `assets/raw/gsc-sitemap-error-20261013.png`).

**Actual causes (the sitemap file was fine):**
1. The user was in the **wrong property** (`putrabooks.github.io` instead of `putraindex.github.io/playasia-deals/`)
2. The full URL was pasted into a box that already contained the property prefix, doubling the URL

**Fix:**
1. Switch property via the dropdown next to the Google logo
2. In the sitemap input box, type ONLY `sitemap.xml`
3. Submit → status flips to Success.

## Issue 5 — "More guides" links 404

**Symptom:** Links from the homepage to category pages returned 404 in a browser.

**Cause:** Root-absolute hrefs (`/japanese-import-games.html`). On a GitHub Pages **project site** (`owner.github.io/repo/`), `/x.html` resolves to the domain root, not the site's subfolder. My link checker missed it because it joined URLs onto the full base — only a real browser resolves `/` correctly.

**Fix:** Change all internal links to relative (`href="japanese-import-games.html"`). Commit, push, verify each returns 200.

## Issue 6 — "All Deals" nav link still broken

**Symptom:** The nav "All Deals" link 404'd after Issue 5 was fixed.

**Cause:** The first fix only matched `href="/...html"` patterns and missed the bare `href="/"`, which pointed at the Pages root.

**Fix:** Replace `href="/"` with `href="index.html"` in all 8 pages. Then scan for ANY `href` starting with `/` to confirm 8/8 pages clean.

**Lesson:** when fixing a class of bug, scan for the whole class (`grep 'href="/'`), not just the instance you noticed.

## Issue 7 — Literal "&amp;" showing in page headings

**Symptom:** Headings showed "Rare &amp; Retro Games" instead of "Rare & Retro Games" (screenshot: `assets/raw/bug-double-escaped-ampersand-20261013.png`).

**Cause:** Double HTML-escaping — the generator escaped `&` to `&amp;` in text that was already escaped (the h1 titles passed through an escape function).

**Fix:**
1. `grep -n "&amp;amp;" *.html` to find all instances (5 pages)
2. Replace `&amp;amp;` → `&amp;` (also check `&amp;#`, `&amp;quot;`, `&amp;lt;`, `&amp;gt;`)
3. Push, wait for Pages rebuild (~40–60s), re-verify with a cache-busting query (`?v=$RANDOM`) — the CDN serves stale content for up to 10 minutes (`cache-control: max-age=600`).

## Issue 8 — curl on Playasia returns 403

**Symptom:** `curl https://www.play-asia.com/deals` → 403 with 5KB Cloudflare block page.

**Fix:** Use real browser automation (Browserbase). Also note this when link-checking: the site's outbound referral links return 403 to bots but work fine for humans — don't "fix" working affiliate links based on bot checks.

## Issue 9 — Playasia /deals does not exist

**Symptom:** Browser navigation to `/deals` showed the store's 404 page.

**Fix:** Find the real path from the site nav: **Clearance** → `https://www.play-asia.com/en/clearance/00/71365` (subcategories like "Clearance Sale 2026 Playstation 4/5"). The product list loads via JS — wait ~4 seconds before scraping, or you get only the skeleton.

## Issue 10 — Telegram channel post failed (HTTP 400)

**Symptom:** `sendMessage` to `@putradeals` returned 400 when the message was posted from a workflow run.

**Cause:** `parse_mode: "HTML"` combined with the workflow's message interpolation — special characters broke the JSON/HTML parsing.

**Fix:** Post **plain text** (no parse_mode field). Keep the message to bullets and plain lines. This worked on subsequent tests.

## Issue 11 — Telegram channel disappeared (HTTP "chat not found")

**Symptom (2026-10-27):** Bot API returns "chat not found"; t.me/putradeals no longer resolves.

**Status:** Channel deleted, renamed, or the bot was removed as admin. Unresolved — confirm with Joe before rebuilding. The site footers still carry a t.me/putradeals link that should be updated or removed once the channel's fate is decided.

## Issue 12 — Playasia store offline (cyberattacks)

**Symptom (from ~2026-10-23):** The entire store shows a CEO notice: taken offline for a security audit after coordinated attacks. Confirmed by news coverage.

**Impact:** No deals to post; referral links convert to nothing until the store returns.

**Mitigation:** The Monday watcher was repurposed into a one-page recovery check — if the offline notice is gone, it runs the full deal sweep and posts. One cheap navigation per week while waiting.

## Issue 13 — GSC "Request indexing" button missing

**Symptom:** No "Request indexing" option in URL Inspection.

**Cause:** Google retired/throttled the button for most properties. Not a bug.

**What works instead:** verification + inbound links (the repo description/homepage/README links) + sitemap submission. Check progress with a `site:putraindex.github.io` search.

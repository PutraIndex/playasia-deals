#!/usr/bin/env python3
"""Check every link on every page of the site. Usage: python3 check_links.py [base_url]
Note: outbound Playasia links return 403 to bots (Cloudflare) - that is NOT broken."""
import re, sys, urllib.request, urllib.error
base = sys.argv[1] if len(sys.argv) > 1 else "https://putraindex.github.io/playasia-deals/"
pages = ["index.html","psn-gift-cards.html","nintendo-eshop-cards.html","steam-wallet-codes.html",
         "xbox-gift-cards.html","japanese-import-games.html","rare-retro-games.html","anime-figures.html"]
bad = []
for p in pages:
    src = urllib.request.urlopen(base+p, timeout=15).read().decode()
    for h in sorted(set(re.findall(r'href="([^"#]+)"', src))):
        url = h if h.startswith("http") else base+h
        try:
            code = urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=15).status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            code = str(e)
        if code != 200:
            bad.append((p, h, code))
print("BROKEN:" if bad else "ALL LINKS OK")
for b in bad: print(" ", b)
sys.exit(1 if bad else 0)

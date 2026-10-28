#!/bin/bash
# Ping IndexNow (Bing/Yandex) for given URLs. Key file must be hosted on the site.
KEY="26fb718a0f04daf9cd7a0bc0c8c8e6b4"
HOST="putraindex.github.io"
[ $# -eq 0 ] && { echo "usage: $0 url [url...]"; exit 1; }
JSON=$(printf '%s\n' "$@" | python3 -c "import json,sys; print(json.dumps({'host':'$HOST','key':'$KEY','urlList':[l.strip() for l in sys.stdin]}))")
curl -s -X POST https://api.indexnow.org/IndexNow -H "Content-Type: application/json" -d "$JSON" -w "\nHTTP %{http_code}\n"

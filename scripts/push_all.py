#!/usr/bin/env python3
"""Deploy local files to the repo in a single commit via the GitHub Git Data API.
Usage: GITHUB_ACCESS_TOKEN=<token> python3 push_all.py file1 [file2 ...]
Pushes each file (relative to repo root) onto main. One commit, no git clone needed."""
import base64, json, os, sys, urllib.request

REPO = "PutraIndex/playasia-deals"   # change if forked/moved
API = f"https://api.github.com/repos/{REPO}"
TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]

def api(method, path, payload=None):
    req = urllib.request.Request(API + path, method=method,
        headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json"},
        data=json.dumps(payload).encode() if payload else None)
    return json.load(urllib.request.urlopen(req))

if len(sys.argv) < 2:
    sys.exit("usage: push_all.py file [file...]")

parent = api("GET", "/git/ref/heads/main")["object"]["sha"]
base_tree = api("GET", f"/git/commits/{parent}")["sha"]
items = []
for f in sys.argv[1:]:
    blob = api("POST", "/git/blobs", {"content": open(f, encoding="utf-8").read(), "encoding": "utf-8"})
    items.append({"path": f, "mode": "100644", "type": "blob", "sha": blob["sha"]})
tree = api("POST", "/git/trees", {"base_tree": base_tree, "tree": items})
commit = api("POST", "/git/commits", {"message": f"Update {', '.join(sys.argv[1:])}",
                                      "tree": tree["sha"], "parents": [parent]})
api("PATCH", "/git/refs/heads/main", {"sha": commit["sha"]})
print("committed:", commit["sha"][:10], "| files:", len(items), "| wait ~60s for Pages")

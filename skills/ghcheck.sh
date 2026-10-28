#!/bin/bash
curl -s https://api.github.com/user -H "Authorization: Bearer $GITHUB_ACCESS_TOKEN" | head -c 300
echo

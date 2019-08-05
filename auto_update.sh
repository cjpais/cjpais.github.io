#!/bin/bash

inotifywait -r -m ~/Dropbox/Notability/cjpais.com/ |
while read -r filename event; do
  sleep 5
  python process.py ~/Dropbox/Notability/cjpais.com/ res/svg commit
done

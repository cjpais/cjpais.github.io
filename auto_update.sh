#!/bin/bash

while true; do
  inotifywait -r ~/Dropbox/Notability/cjpais.com/
  python process.py ~/Dropbox/Notability/cjpais.com/ res/svg commit
  # hacky debounce
  sleep 5
done

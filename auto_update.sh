#!/bin/bash

while true; do
  inotifywait -r ~/Dropbox/Notability/cjpais.com/
  # hacky debounce + make sure new file is picked up
  sleep 5
  python process.py ~/Dropbox/Notability/cjpais.com/ res/svg commit
done

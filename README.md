# cjpais.github.io
Personal blog + scripts to make it work

## Automaded workflow from iPad -> Blog

1. Write something on Notability
2. Sync to Dropbox
3. After file updated on server execute process.py via auto_update.sh. This does the following
  4. Convert .pdf to SVG
  5. Process SVG
  6. From the processed guy generate HTML pages from SVG (index + page)
  7. Commit to git repo and see

## Dependencies
  * inkscape (for process.py)
  * inotify-tools (for running process.py automagically)
  * requirements.txt (Jinja2, static site generation) 
  
## Temp Notes on Pages:
There are no hyperlinks as of yet. This will be added in a later revision of process.py that inserts links into the SVG's themselves. CSS style will come with this. For now other pages can be found manually by going [here](https://github.com/cjpais/cjpais.github.io/tree/master/page), then navigating to cjpais.com/page/<page.html>

Needs directory structure in Notability. I will have to rearrange my Dropbox & process.py to support. This will be more natural but still not ideal. Needs a flag tagged (graph like) structure, not heirarchy. 

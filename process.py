import time
from datetime import datetime
import argparse
import subprocess
import sys
import glob
import os
from xml.dom import minidom
import re
from jinja2 import Template, Environment, PackageLoader, select_autoescape

epoch = datetime.utcfromtimestamp(0)
header_files = ['Title.svg', 'Posts.svg', 'About.svg']
env = Environment(
        loader = PackageLoader('process', 'src/templates'),
        autoescape = select_autoescape(['html'])
      )

# what defines a page.
class Page():
    pass

def gen_svg_from_pdf(pdf, svg):
    print("writing {} to {}".format(pdf, svg))

    # create the svg
    #subprocess.call(["pdf2svg", pdf, svg])
    subprocess.call(["inkscape", "--without-gui", "--file={}".format(pdf), "--export-plain-svg={}".format(svg)])

def optimize_svg(svg):
    # on the new svg optimize with svgo
    subprocess.call(["svgo", svg])

def remove_svg_height_width(svg):
    svg_xml = minidom.parse(svg)

    # remove height & width from svg + set viewbox from inkscape
    svg_xml.childNodes[0].removeAttribute("height")
    svg_xml.childNodes[0].removeAttribute("width")

    # write new xml
    with open(svg, 'w') as f:
        svg_xml.writexml(f)

def crop_svg(svg):
    # get output from inkscape
    is_out = subprocess.check_output(["inkscape", "--query-all", svg])
    
    # get the new vbox from the inkscape output. the first line has the vbox
    # that we want
    print (is_out)
    first_row = re.split(',|\n', is_out)
    print first_row

    width = first_row[3]
    height = first_row[4] 
    print(width, height)

    vbox = " ".join(first_row[1:5])
   
    # parse svg into xml
    svg_xml = minidom.parse(svg)

    # remove height & width from svg + set viewbox from inkscape
    svg_xml.childNodes[0].setAttribute("height", height)
    svg_xml.childNodes[0].setAttribute("width", width)
    svg_xml.childNodes[0].setAttribute("viewBox", vbox)

    # write new xml
    with open(svg, 'w') as f:
        svg_xml.writexml(f)

def get_last_update():
    try:
        with open('last_updated.txt', 'r') as update_f:
            # read in the file, strip newline and format into new datetime obj
            t = update_f.read().replace('\n', '')
            return datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')
    except (IOError, ValueError) as e:
        # if the file couldnt open then return the epoch time
        return epoch

def process(idir, odir):
    print("\nProcessing {}...".format(idir))
    files = []
    last_update = get_last_update()
    print("last update {}".format(last_update))

    # go through all pdf in input dir
    for file in os.listdir(idir):
        if file.endswith(".pdf"):
            # get the file names
            pdf_file = os.path.join(idir, file)
            svg_file = os.path.join(odir, file.split('.')[0] + ".svg")

            # only if new file update the svg
            last_modified_unix= os.path.getmtime(pdf_file)
            last_modified = datetime.fromtimestamp(last_modified_unix)

            # only do next steps if it's been updated since last time
            if last_modified > last_update:
                files.append(file)
                # pdf to svg
                gen_svg_from_pdf(pdf_file, svg_file)

                # optimize svg
                optimize_svg(svg_file)

                # remove height and width attributes to fix some things
                remove_svg_height_width(svg_file)

                # crop
                # crop_svg(svg_file)
            else:
                print("skipping {}. last modified @ {}".format(file, last_modified))


    # write out new file for when we last generated in curr dir
    if files != []:
        with open('last_updated.txt', 'w') as update_f:
            update_f.write(str(datetime.now()))

    # return the list of new/updated files for commit message
    return files

def gen_page(page, svg):
    print("gen page for {} {}".format(page, svg))

    page_temp = env.get_template('base.html')
    title = page.split('/')[-1].split(".")[0]

    page_data = page_temp.render(title=title, content_path=page)
    with open(page, 'w') as new_page:
        new_page.write(page_data)

"""
    Generate HTML from:
        SVG resources (res/svg)
        Jinja2 templates (src/templates)

    TODO this is very 0.1. Not very generic at all. Needs rework of dir
    structure. Able to define what should go in header etc. All programatic
"""
def gen_html():
    print("\nGenerating HTML...")
    svg_dir = 'res/svg'
    for file in os.listdir(svg_dir):
        # get the full path for SVG
        spath = os.path.join(svg_dir, file)
        hpath = ''

        # TODO remove hardcoding of index
        # get html path for this file
        if file == "TempIdx.svg":
            hpath = 'index.html'
        elif file not in header_files:
            hpath = 'page/' + file.split('.')[0] + '.html'

        # go ahead and gen the page now
        if hpath != '':
            gen_page(hpath, spath)

if __name__ == "__main__":
    updated_s = ""

    if len(sys.argv) >= 3:
	input_dir = sys.argv[1]
	output_dir = sys.argv[2]
    else:
	print("not enough arguments to do anything. exiting")
	quit()

    # generate svg from pdf, optimize, and crop
    updated_pages = process(input_dir, output_dir)
    updated_s = "updated pages from script: " + (",").join(updated_pages)

    # gen HTML (for all pages) 
    gen_html()

    # commit to git if enough args
    if len(sys.argv) >= 4 and updated_s != "":
        subprocess.call(["git", "add", "*"])
        subprocess.call(["git", "commit", "-m", updated_s])

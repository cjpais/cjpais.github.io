import subprocess
import sys
import glob
import os
from xml.dom import minidom
import re

def gen_svg_from_pdf(pdf, svg):
    print("writing {} to {}".format(pdf, svg))

    # create the svg
    subprocess.call(["pdf2svg", pdf, svg])

def optimize_svg(svg):
    # on the new svg optimize with svgo
    subprocess.call(["svgo", svg])

def crop_svg(svg):
    # get output from inkscape
    is_out = subprocess.check_output(["inkscape", "--query-all", svg])
    
    # get the new vbox from the inkscape output. the first line has the vbox
    # that we want
    vbox = " ".join(re.split(',|\n', is_out)[1:5])
   
    # parse svg into xml
    svg_xml = minidom.parse(svg)

    # remove height & width from svg + set viewbox from inkscape
    svg_xml.childNodes[0].removeAttribute("height")
    svg_xml.childNodes[0].removeAttribute("width")
    svg_xml.childNodes[0].setAttribute("viewBox", vbox)

    # write new xml
    with open(svg, 'w') as f:
        svg_xml.writexml(f)


def process(idir, odir):
    # go through all pdf in input dir
    for file in os.listdir(idir):
        if file.endswith(".pdf"):
            # get the file names
            pdf_file = os.path.join(idir, file)
            svg_file = os.path.join(odir, file.split('.')[0] + ".svg")

            # pdf to svg
            gen_svg_from_pdf(pdf_file, svg_file)

            # optimize svg
            optimize_svg(svg_file)

            # crop
            crop_svg(svg_file)


if __name__ == "__main__":
    if len(sys.argv) >= 3:
	input_dir = sys.argv[1]
	output_dir = sys.argv[2]
    else:
	print("not enough arguments to do anything. exiting")
	quit()

    # generate svg from pdf, optimize, and crop
    process(input_dir, output_dir)

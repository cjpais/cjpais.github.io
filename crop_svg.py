import subprocess
import sys
from xml.dom import minidom

if __name__ == "__main__":
    # get file name from arguments
    svg_file = sys.argv[1]

    new_file = svg_file.split('.')[0] + "_new.svg"

    # get output from inkscape
    is_out = subprocess.check_output(["inkscape", "--query-all", svg_file])
    
    # get the new vbox from the inkscape output. the first line has the vbox
    # that we want
    vbox = " ".join(is_out.split(",")[1:5])
    print (vbox)
   
    # parse svg into xml
    svg_xml = minidom.parse(svg_file)

    # remove height & width from svg + set viewbox from inkscape
    svg_xml.childNodes[0].removeAttribute("height")
    svg_xml.childNodes[0].removeAttribute("width")
    svg_xml.childNodes[0].setAttribute("viewBox", vbox)

    # write new xml
    with open(new_file, 'w') as f:
        svg_xml.writexml(f)

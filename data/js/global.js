document.addEventListener("DOMContentLoaded", function(event) {
  console.log("document loaded")
  obj_list = document.getElementsByTagName('object');
  for (obj = 0; obj < obj_list.length; obj++) {
    svg = obj_list[obj].getSVGDocument().getElementsByTagName('svg')[0]
    bbox = svg.getBBox()
    viewBox = [bbox.x, bbox.y, bbox.width, bbox.height].join(" ")
    svg.setAttribute("viewBox", viewBox)
    svg.setAttribute("height", bbox.height)
    svg.setAttribute("width", bbox.width)
  }
});

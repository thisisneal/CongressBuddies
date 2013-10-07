if (typeof String.prototype.startsWith != 'function') {
  // see below for better implementation!
  String.prototype.startsWith = function (str){
    return this.indexOf(str) == 0;
  };
}

var width = 960,
    height = 500;

var path = d3.geo.path();

var ignore_district = false;

var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height);

queue()
    .defer(d3.json, "/static/js/us.json")
    .defer(d3.json, "/static/js/us-congress-113.json")
    .await(ready);

function ready(error, us, congress) {
  console.log(map_color);
  svg.append("defs").append("path")
      .attr("id", "land")
      .datum(topojson.feature(us, us.objects.land))
      .attr("d", path);

  svg.append("clipPath")
      .attr("id", "clip-land")
    .append("use")
      .attr("xlink:href", "#land");

  svg.append("g")
      .attr("clip-path", "url(#clip-land)")
    .selectAll("path")
      .data(topojson.feature(congress, congress.objects.districts).features)
    .enter().append("path")
      .attr("d", path)
    .attr("class",(function(d) { 
       for(var loop = 0; loop < map_color["Republican"].length; loop++) {
        try {
           if(d.id == map_color["Republican"][loop]["code"]) {
           return "repub-districts";
           }
           else if((JSON.stringify(d.id)).startsWith(map_color["Republican"][loop]["code"])) {
             if(JSON.stringify(d.id).length == 3 && map_color["Republican"][loop]["code"].toString().length == 1)
              return "repub-districts";
            else if(JSON.stringify(d.id).length == 4 && map_color["Republican"][loop]["code"].toString().length == 2)
              return "repub-districts";
           }
         }
         catch(err) {
         }
       }
       for(var loop = 0; loop < map_color["Democrat"].length; loop++) {
         try {
           if(d.id == map_color["Democrat"][loop]["code"]) {
           return "dem-districts";
           }
           else if((JSON.stringify(d.id)).startsWith(map_color["Democrat"][loop]["code"])) {
             if(JSON.stringify(d.id).length == 3 && map_color["Democrat"][loop]["code"].toString().length == 1)
              return "repub-districts";
            else if(JSON.stringify(d.id).length == 4 && map_color["Democrat"][loop]["code"].toString().length == 2)
              return "repub-districts";
           }
         }
         catch(err) {
         }
       }
        return "districts";
      }))
    .append("title")
      .text(function(d) { 

       for(var loop = 0; loop < map_color["Republican"].length; loop++) {
        try {
           if(d.id == map_color["Republican"][loop]["code"]) {
             return_str = "";
             return_str = map_color["Republican"][loop]["name"]
             return_str += "\nDistrict: " + map_color["Republican"][loop]["district"];
             return return_str;
           }
           else if((JSON.stringify(d.id)).startsWith(map_color["Republican"][loop]["code"])) {

            return_str = "";
            if(JSON.stringify(d.id).length == 3 && map_color["Republican"][loop]["code"].toString().length == 1)
              return_str = map_color["Republican"][loop]["name"]
            else if(JSON.stringify(d.id).length == 4 && map_color["Republican"][loop]["code"].toString().length == 2)
              return_str = map_color["Republican"][loop]["name"]
            return return_str;
           }
         }
         catch(err) {
           return ""
         }
       }
       for(var loop = 0; loop < map_color["Democrat"].length; loop++) {
         try {
           if(d.id == map_color["Democrat"][loop]["code"]) {
             return_str = "";
             return_str = map_color["Democrat"][loop]["name"]
             return_str += "\nDistrict: " + map_color["Democrat"][loop]["district"];
             return return_str;
           }
           else if((JSON.stringify(d.id)).startsWith(map_color["Democrat"][loop]["code"])) {
             return_str = "";
            if(JSON.stringify(d.id).length == 3 && map_color["Democrat"][loop]["code"].toString().length == 1)
              return_str = map_color["Democrat"][loop]["name"]
            else if(JSON.stringify(d.id).length == 4 && map_color["Democrat"][loop]["code"].toString().length == 2)
              return_str = map_color["Democrat"][loop]["name"]
             return return_str;
           }
         }
         catch(err) {
           return ""
         }
       }


      });

  if(ignore_district) {
  svg.append("path")
      .attr("class", "district-boundaries")
      .attr("clip-path", "url(#clip-land)")
      .datum(topojson.mesh(congress, congress.objects.districts, function(a, b) { return (a.id / 1000 | 0) === (b.id / 1000 | 0); }))
      .attr("d", path);
  }

  svg.append("path")
      .attr("class", "state-boundaries")
      .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
      .attr("d", path);

  (elem=document.getElementById("loading")).parentNode.removeChild(elem);
  document.getElementById("top_search").focus()
  document.getElementById("footer").style.opacity = 1;
}

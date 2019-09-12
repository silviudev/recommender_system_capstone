$(function() {
  getRecs();

  function getRecs(){
    $.ajax({
        url: '/api/recs' + window.location.search,
        success: function(data){
          console.log("WORKED!")
          console.log(data)
          bubble_array = [];

          for (let i =0; i < 10; i++){
            currentDict = {}
            currentDict["Name"] = data["recData"][i][1]
            currentDict["Count"] = data["recData"][i][4]
            bubble_array.push(currentDict)
          }

          bubble_dataset = {
            "children": bubble_array
          }

          let diameter = 1100;
          let color = d3.scaleOrdinal(d3.schemeCategory20);

          let bubble = d3.pack(bubble_dataset)
              .size([diameter, diameter])
              .padding(1.5);

          let svg = d3.select("#bubble")
              .append("svg")
              .attr("width", diameter)
              .attr("height", diameter)
              .attr("class", "bubble");

          let nodes = d3.hierarchy(bubble_dataset)
              .sum(function(d) { return d.Count; });

          let node = svg.selectAll(".node")
              .data(bubble(nodes).descendants())
              .enter()
              .filter(function(d){
                  return  !d.children
              })
              .append("g")
              .attr("class", "node")
              .attr("transform", function(d) {
                  return "translate(" + d.x + "," + d.y + ")";
              });

          node.append("title")
              .text(function(d) {
                  return d.Name + ": " + d.Count;
              });

          node.append("circle")
              .attr("r", function(d) {
                  return d.r;
              })
              .style("fill", function(d,i) {
                  return color(i);
              });

          node.append("text")
              .attr("dy", ".2em")
              .style("text-anchor", "middle")
              .text(function(d) {
                  return d.data.Name.substring(0, d.r / 3);
              })
              .attr("font-family", "sans-serif")
              .attr("font-size", function(d){
                  return d.r/7;
              })
              .attr("fill", "white");

          node.append("text")
              .attr("dy", "1.3em")
              .style("text-anchor", "middle")
              .text(function(d) {
                  return d.data.Count;
              })
              .attr("font-family",  "Gill Sans", "Gill Sans MT")
              .attr("font-size", function(d){
                  return d.r/5;
              })
              .attr("fill", "white");

          d3.select(self.frameElement)
              .style("height", diameter + "px");

          }
        })
      }
});

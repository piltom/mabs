
function heatmap(x_limits,y_limits, data, size ,d3_node){
  console.log(d3_node)
  var margin = {top: 60, right: 60, bottom: 60, left: 60},
    width = size[1] - margin.left - margin.right,
    height = size[0] - margin.top - margin.bottom;
  let svg = d3_node.append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)

  console.log(svg);
  svg.append("g")
    .attr("transform","translate(" + margin.left + "," + margin.top + ")");

  let x = d3.scaleLinear()
    .range([ 0, width ])
    .domain(x_limits)
  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))
  var y = d3.scaleLinear()
      .range([ height, 0 ])
      .domain(y_limits)
  svg.append("g")
      .call(d3.axisLeft(y));
  console.log("Til the end")
}

function create_plot(plot_type, params, selector){
    heatmap([0,100],[0,400], null,[params.viewport.height,params.viewport.width], d3.select(selector));
}

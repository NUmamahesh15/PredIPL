
// function to display toss decision bat data
function getBatInfo(bat_data){

  var bat_data =bat_data;
// console.log(bat_data);

var rainbow = d3.scaleSequential(d3.interpolateRainbow).domain([0,13])

// setting the width and dimension for displaying the chart
var margin = {top: 20, right: 30, bottom: 50, left: 40},
    width = 500 - margin.left - margin.right,
    height = 450 - margin.top - margin.bottom;

// appending SVG object to display the chart
var svg = d3.select("#tossDecisionBat")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform","translate(" + margin.left + "," + margin.top + ")");

// Defining the x-axis
var x = d3.scaleBand()
    .range([ 0, width ])
    .domain(bat_data.map(function(d) { return d.season; }))
    .padding(0.2);
svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))
    .style("font-size", 12)
    .style("stroke",'#FFFF')

// Define y-axis
var y = d3.scaleLinear()
    .domain([0, 50])
    .range([ height, 0]);
svg.append("g")
    .call(d3.axisLeft(y))
    .style("font-size", 12)
    .style("stroke",'#FFFF')


  svg.selectAll("rect")
    .data(bat_data)
    .enter()
    .append("rect")
    .transition()
    .duration(1000)
      .attr("x", function(d) { return x(d.season); })
      .attr("y", function(d) { return y(d.value); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(d.value); })
      .attr("fill", function(d,i){return rainbow(i)})

}

// function to display toss decision field data
function getFieldInfo(field_data){

  var field_data =field_data;
  var rainbow = d3.scaleSequential(d3.interpolateRainbow).domain([0,13])

// margin and dimension
var margin = {top: 20, right: 30, bottom: 50, left: 40},
    width = 500 - margin.left - margin.right,
    height = 450 - margin.top - margin.bottom;
    // append the svg object to the body of the page
var svg = d3.select("#tossDecisionField")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform","translate(" + margin.left + "," + margin.top + ")");
// Defining the x-axis
var x = d3.scaleBand()
    .range([ 0, width ])
    .domain(field_data.map(function(d) { return d.season; }))
    .padding(0.2);
svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))
    .style("font-size", 12)
    .style("stroke",'#FFFF')

// Define y-axis
var y = d3.scaleLinear()
    .domain([0, 50])
    .range([ height, 0]);
svg.append("g")
    .call(d3.axisLeft(y))
    .style("font-size", 12)
    .style("stroke",'#FFFF');


  svg.selectAll("rect")
    .data(field_data)
    .enter()
    .append("rect")
    .transition()
    .duration(1000)
      .attr("x", function(d) { return x(d.season); })
      .attr("y", function(d) { return y(d.value); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(d.value); })
      .attr("fill", function(d,i){return rainbow(i)})

}

// function to display matches data
function getMatchInfo(matches){
  var rainbow = d3.scaleSequential(d3.interpolateRainbow).domain([0,13])
  var matches =matches;
console.log(matches);
// margin and dimension
var margin = {top: 20, right: 30, bottom: 50, left: 40},
    width = 500 - margin.left - margin.right,
    height = 450 - margin.top - margin.bottom;
    // append the svg object to the body of the page
var svg = d3.select("#matchesPlayed")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");
// Defining the x-axis
var x = d3.scaleBand()
  .range([ 0, width ])
  .domain(matches.map(function(d) { return d.team; }))
  .padding(0.2);
svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x))
  .style("font-size", 12)
  .style("stroke",'#0000');
// Define y-axis
// Add Y axis
var y = d3.scaleLinear()
  .domain([0, d3.max(matches, function(d) {
      return d.count;
    }) + 20])
  .range([ height, 0]);
svg.append("g")
  .call(d3.axisLeft(y))
  .style("font-size", 12)
  .style("stroke",'#0000');


  svg.selectAll("rect")
    .data(matches)
    .enter()
    .append("rect")
    // .merge(sections)
    .transition()
    .duration(1000)
      .attr("x", function(d) { return x(d.team); })
      .attr("y", function(d) { return y(d.count); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(d.count); })
      .attr("fill", function(d,i){return rainbow(i)})


}

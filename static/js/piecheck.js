function displayChart(data,tot) {

    var width = 400
    var height = 400
    var margin = 40

    // Defining the radius
    var radius = Math.min(width, height) / 2 - margin

    // append the svg object to the div called 'tossWinMatchWin'
    var svg = d3.select("#tossWinMatchWin")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    // Setting the color scale based on the values
    var color = d3.scaleOrdinal()
        .domain(data)
        .range(["#51318c", "#fac234"])

    // Compute the position of each group on the pie:
    var pie = d3.pie()
        .value(function(d) {return d.value; })
    // console.log(pie);
    // This generates the start angle and end angle for each category
    var data_ready = pie(d3.entries(data))
    console.log(data_ready)

    // Building the arc arcGenerator that gives the path
    var arcGenerator = d3.arc()
                          .innerRadius(0)
                          .outerRadius(radius)

    // Building the pie chart
    svg
    .selectAll('path')
    .data(data_ready)
    .enter()
    .append('path')
    .attr('d',arcGenerator)
    .attr('fill', function(d){ return(color(d.data.key)) })
    .attr("stroke", "black")
    .style("stroke-width", "2px")
    .style("opacity", 0.7)

  svg
    .selectAll('mySlices')
    .data(data_ready)
    .enter()
    .append('text')
    .text(function(d){ return  d.data.key + " " +Math.round((d.value/tot)*100)+'%'})
    .attr("transform", function(d) { return "translate(" + arcGenerator.centroid(d) + ")";  })
    .style("text-anchor", "middle")
    .style("font-size", 17)
    .style("stroke", "#FFFF")

}

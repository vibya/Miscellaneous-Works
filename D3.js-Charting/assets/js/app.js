var svgWidth = 1080;
var svgHeight = 540;

var margin = {
  top: 20,
  right: 40,
  bottom: 80,
  left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart,
// and shift the latter by left and top margins.
var svg = d3
  .select("#scatter")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

// Append an SVG group
var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Initial Params
var chosenXAxis = "poverty";
var chosenYAxis = "healthcare";

// function used for updating x-scale var upon click on axis label
function xScale(censusdata, chosenXAxis) {
  // create scales
  var xLinearScale = d3.scaleLinear()
    .domain([d3.min(censusdata, d => d[chosenXAxis]) * 0.8,
      d3.max(censusdata, d => d[chosenXAxis]) * 1.2
    ])
    .range([0, width]);

  return xLinearScale;
}

function yScale(censusdata, chosenYAxis) {
  // create scales
  var yLinearScale = d3.scaleLinear()
    .domain([0, d3.max(censusdata, d => d[chosenYAxis])])
    .range([height, 0]);

  return yLinearScale;

}
// function used for updating xAxis var upon click on axis label
function renderXAxes(newXScale, xAxis) {
  var bottomAxis = d3.axisBottom(newXScale);

  xAxis.transition()
    .duration(500)
    .call(bottomAxis);
  
  return xAxis;
}

function renderYAxes(newYscale, yAxis) {
  var leftAxis = d3.axisLeft(newYscale);

  yAxis.transition()
    .duration(500)
    .call(leftAxis);

  return yAxis;
}
// function used for updating circles group with a transition to
// new circles
function renderXCircles(circlesGroup, newXScale, chosenXaxis, circleslabels) {

  circlesGroup.transition()
    .duration(500)
    .attr("cx", d => newXScale(d[chosenXAxis]));

  circleslabels.transition()
    .duration(750)
    .attr("x",d => newXScale(d[chosenXAxis]));

  return circlesGroup,circleslabels;
}

function renderYCircles(circlesGroup, newYScale, chosenYaxis, circleslabels) {

  circlesGroup.transition()
    .duration(500)
    .attr("cy",0)
    .transition()
    .duration(500)
    .attr("cy", d => newYScale(d[chosenYAxis]));
  
  circleslabels.transition()
    .duration(500)
    .attr("y",0)
    .transition()
    .duration(750)
    .attr("y",d => newYScale(d[chosenYAxis])+3);

  return circlesGroup,circleslabels;
}

// function used for updating circles group with new tooltip
function updateToolTip(chosenXAxis, chosenYAxis, circlesGroup) {

  if (chosenXAxis === "poverty") {
    var xlabel = "Poverty:";
  }
  else if (chosenXAxis === "age") {
    var xlabel = "Age:";
  }
  else if (chosenXAxis === "income") {
    var xlabel = "Income: $";
  }

  if (chosenYAxis === "healthcare") {
    var ylabel = "Lacks Healthcare:";
  }
  else if (chosenYAxis === "smokes"){
    var ylabel = "Smokes:";
  }
  else if (chosenYAxis === "obesity"){
    var ylabel = "Obesity:"
  }

  var toolTip = d3.tip()
    .attr("class", "tooltip")
    .offset([80, -60])
    .html(function(d) {
      return (`${d.state}<br>${xlabel} ${d[chosenXAxis]}<br>${ylabel} ${d[chosenYAxis]}%`);
    });

  circlesGroup.call(toolTip);

  circlesGroup.on("mouseover", function(data) {
      d3.select(this)
      .transition()
      .duration(100);
      toolTip.show(data,this);
    })
    // onmouseout event
    .on("mouseout", function(data, index) {
      d3.select(this)
      .transition()
      .duration(100);
      toolTip.hide(data);
    });
  
  return circlesGroup;
}

// Retrieve data from the CSV file and execute everything below
var file = "https://raw.githubusercontent.com/the-Coding-Boot-Camp-at-UT/UTAUS201804DATA2-Class-Repository-DATA/master/16-D3/HOMEWORK/Instructions/data/data.csv?token=Ai1X4kfVG59iImK6CXQclTgK1lL3urFRks5bskKEwA%3D%3D"
d3.csv(file).then(successHandle, errorHandle);

function errorHandle(error){
  throw error;
}

function successHandle(censusdata) {

  // parse data
  censusdata.forEach(function(data) {
    data.poverty = +data.poverty;
    data.age = +data.age;
    data.healthcare = +data.healthcare;
    data.income = +data.income;
    data.smokes = +data.smokes;
    data.obesity = +data.obesity;
  });

  // xLinearScale function above csv import
  var xLinearScale = xScale(censusdata, chosenXAxis);

  // Create y scale function
  var yLinearScale = yScale(censusdata, chosenYAxis);
  
  // Create initial axis functions
  var bottomAxis = d3.axisBottom(xLinearScale);
  var leftAxis   = d3.axisLeft(yLinearScale);

  // append x axis
  var xAxis = chartGroup.append("g")
    .classed("x-axis", true)
    .attr("transform", `translate(0, ${height})`)
    .call(bottomAxis);

  // append y axis
  var yAxis = chartGroup.append("g")
    .classed("y-axis", true)
    .attr("transform", `translate(0)`)
    .call(leftAxis);

  // append initial circles
  var circlesGroup = chartGroup.selectAll("circle")
    .data(censusdata)
    .enter()
    .append("circle")
    .attr("cx", d => xLinearScale(d[chosenXAxis]))
    .attr("cy", d => yLinearScale(d[chosenYAxis]))
    .attr("r", 12)
    .attr("fill", "black")
    .attr("opacity", ".8");

  var circleslabels= chartGroup.append("text")
    .style("text-anchor", "middle")
    .style("font-size", "10px")
    .style("fill", "white")
    .style("stroke", "white")
    .selectAll("circle")
    .data(censusdata)
    .enter()
    .append("tspan")
        .attr("x", d => xLinearScale(d[chosenXAxis]))
        .attr("y", d => yLinearScale(d[chosenYAxis])+3)
        .text(d => d.abbr);

  // Create group for  multi x- axis labels
  var labelsGroup = chartGroup.append("g")
    .attr("transform", `translate(${width / 2}, ${height + 20})`);

  var povertyLabel = labelsGroup.append("text")
    .attr("x", 0)
    .attr("y", 20)
    .attr("value", "poverty") // value to grab for event listener
    .classed("active", true)
    .text("In Poverty (%)");

  var ageLabel = labelsGroup.append("text")
    .attr("x", 0)
    .attr("y", 40)
    .attr("value", "age") // value to grab for event listener
    .classed("inactive", true)
    .text("Age (Median)");

  var incomeLabel = labelsGroup.append("text")
    .attr("x", 0)
    .attr("y", 60)
    .attr("value", "income") // value to grab for event listener
    .classed("inactive", true)
    .text("Household Income (Median)");

  // Create group for  multi y- axis labels
  var healthcareLabel = labelsGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", (height / 2))
    .attr("y", 0 - (width / 2)-30)
    .attr("value", "healthcare")
    .classed("active", true)
    .text("Lacks Healthcare (%)");
  
  var smokeLabel = labelsGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", (height / 2))
    .attr("y", 0 -(width / 2)-50)
    .attr("value", "smokes")
    .classed("inactive", true)
    .text("Smokes (%)");

  var obeseLabel = labelsGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", (height / 2))
    .attr("y", 0 -(width / 2)-70)
    .attr("value", "obesity")
    .classed("inactive", true)
    .text("Obese (%)");

  // updateToolTip function above csv import
  var circlesGroup = updateToolTip(chosenXAxis, chosenYAxis, circlesGroup);

  xAxisLabels = ["age", "poverty", "income"];
  yAxisLabels = ["healthcare", "smokes", "obesity"];

  // x axis labels event listener
  labelsGroup.selectAll("text")
    .on("click", function() {
      // get value of selection
      var value = d3.select(this).attr("value");
      var isX = xAxisLabels.includes(value);
      var isY = yAxisLabels.includes(value);
      if (isX) {
        if (value !== chosenXAxis) {

          // replaces chosenXAxis with value
          chosenXAxis = value;

          // updates x scale for new data
          xLinearScale = xScale(censusdata, chosenXAxis);

          // updates x axis with transition
          xAxis = renderXAxes(xLinearScale, xAxis);

          // updates circles with new x values
          circlesGroup,circleslabels = renderXCircles(circlesGroup, xLinearScale, chosenXAxis, circleslabels);

          // updates tooltips with new info
          circlesGroup = updateToolTip(chosenXAxis, chosenYAxis, circlesGroup);

          // changes classes to change bold text
          if (chosenXAxis === "age") {
            ageLabel
              .classed("active", true)
              .classed("inactive", false);
            povertyLabel
              .classed("active", false)
              .classed("inactive", true);
            incomeLabel
              .classed("active", false)
              .classed("inactive", true);
            }
          else if (chosenXAxis === "income") {
            incomeLabel
              .classed("active", true)
              .classed("inactive", false);
            ageLabel
              .classed("active", false)
              .classed("inactive", true);
            povertyLabel
              .classed("active", false)
              .classed("inactive", true);
            }
          else {
            ageLabel
              .classed("active", false)
              .classed("inactive", true);
            povertyLabel
              .classed("active", true)
              .classed("inactive", false);
            incomeLabel
              .classed("active", false)
              .classed("inactive", true);
            }
          }
        }
      else if (isY) {
        if (value !== chosenYAxis) {

          chosenYAxis = value;
          yLinearScale = yScale(censusdata, chosenYAxis);
          yAxis = renderYAxes(yLinearScale, yAxis);
          circlesGroup,circleslabels = renderYCircles(circlesGroup, yLinearScale, chosenYAxis, circleslabels);
          circlesGroup = updateToolTip(chosenXAxis, chosenYAxis, circlesGroup);
          if (chosenYAxis === "healthcare") {
            healthcareLabel
              .classed("active", true)
              .classed("inactive", false);
            smokeLabel
              .classed("active", false)
              .classed("inactive", true);
            obeseLabel
              .classed("active", false)
              .classed("inactive", true);
            }
          else if (chosenYAxis === "smokes") {
            smokeLabel
              .classed("active", true)
              .classed("inactive", false);
            healthcareLabel
              .classed("active", false)
              .classed("inactive", true);
            obeseLabel
              .classed("active", false)
              .classed("inactive", true);
            }
          else {
            smokeLabel
              .classed("active", false)
              .classed("inactive", true);
            healthcareLabel
              .classed("active", false)
              .classed("inactive", true);
            obeseLabel
              .classed("active", true)
              .classed("inactive", false);  
            }
          } 
        }
    }
  );
};

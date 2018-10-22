// from data.js
var tableData = data;

// YOUR CODE HERE!
var submit = d3.select("#filter-btn");

submit.on("click", function() {

    // Prevent the page from refreshing
    d3.event.preventDefault();
  
    // Select the input element and get the raw HTML node
    var inputElement = d3.select("#datetime");
  
    // Get the value property of the input element
    var inputValue = inputElement.property("value");
  
    // console.log(inputValue);
    // console.log(tableData);
  
    var filteredData = tableData.filter(sighting => sighting.datetime === inputValue);
  
    // console.log(filteredData);
    // $("#ufo-table tbody tr").remove();
    var tbody = d3.select("tbody");
    $("#ufo-table tbody").empty();

    // console.log(tbody);
    // tbody.empty();
  
    filteredData.forEach((usighting) => {
        var row = tbody.append("tr");
        Object.entries(usighting).forEach(([key, value]) => {
            var cell = tbody.append("td");
            cell.text(value);
        });
    });
    
  });
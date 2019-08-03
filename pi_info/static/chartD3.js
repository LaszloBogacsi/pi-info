const queryParams = window.location.search;
const requestInit = {
    method: 'GET',
    mode: 'cors',
    redirect: 'follow',
    headers: new Headers({
        'Content-Type': 'application/json'
    })
};

// const url = "http://localhost:9080/sensor/data";
const url = "http://localhost:5000/sensor/data";
fetch(url + queryParams)
    .then(response => response.json())
    .catch(error => console.log(error))
    .then(data => loadDataset(data));

function loadDataset(data) {
    const dataset_temp = data.sensor_data.map(d => d.data.values.filter(v => v.type === "temperature")[0].value);
    const dataset_humidity = data.sensor_data.map(d => d.data.values.filter(v => v.type === "humidity")[0].value);
    const timeScale = data.sensor_data
        .map(d => d.published_at)
        .map(dateStr => d3.timeParse("%Y-%m-%dT%H:%M:%S")(dateStr));
    const dataXRange = d3.extent(timeScale);
// 2. Use the margin convention practice
    const margin = {top: 50, right: 50, bottom: 50, left: 50}
        , width = (window.innerWidth - margin.left - margin.right) * 0.9 // Use the window's width
        , height = (window.innerHeight - margin.top - margin.bottom) * 0.9; // Use the window's height

    const n = dataset_temp.length;

    const xScale = d3.scaleTime().domain(dataXRange).range([0, width]);
    const yScale = d3.scaleLinear().domain([-10, 40]).range([height, 0]);
    const yScale2 = d3.scaleLinear().domain([0, 100]).range([height, 0]);
    const line_temp = d3.line()
        .x((d, i) =>  xScale(timeScale[i])) // set the x values for the line generator
        .y(d => yScale(d)) // set the y values for the line generator
        .curve(d3.curveMonotoneX); // apply smoothing to the line
    const line_humid = d3.line()
        .x((d, i)  => xScale(timeScale[i])) // set the x values for the line generator
        .y(d => yScale2(d)) // set the y values for the line generator
        .curve(d3.curveMonotoneX); // apply smoothing to the line

// 1. Add the SVG to the page and employ #2
    const svg = d3.select("#chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// 3. Call the x axis in a group tag
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

// 4. Call the y axis in a group tag
    svg.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft
//  Call the right y axis in a group tag
    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + width + " ,0)")
        .call(d3.axisRight(yScale2)); // Create an axis component with d3.axisLeft

// 9. Append the path, bind the data, and call the line generator
    svg.append("path")
        .datum(dataset_temp) // 10. Binds data to the line
        .attr("class", "line") // Assign a class for styling
        .attr("d", line_temp); // 11. Calls the line generator
    // add another line for humidity
    svg.append("path")
        .datum(dataset_humidity) // 10. Binds data to the line
        .attr("class", "line2") // Assign a class for styling
        .attr("d", line_humid); // 11. Calls the line generator

// 12. Appends a circle for each datapoint
    svg.selectAll(".dot")
        .data(dataset_temp)
        .enter().append("circle") // Uses the enter().append() method
        .attr("class", "dot") // Assign a class for styling
        .attr("cx", function (d, i) {
            return xScale(timeScale[i])
        })
        .attr("cy", function (d) {
            return yScale(d)
        })
        .attr("r", 5)
        .on("mouseover", function (a, b, c) {
            console.log(a);
            this.setAttribute('class', 'focus')
        })
        .on("mouseout", function () {
            this.removeAttribute('class', 'focus');
            this.setAttribute('class', 'dot')

        });
//       .on("mousemove", mousemove);

//   var focus = svg.append("g")
//       .attr("class", "focus")
//       .style("display", "none");

//   focus.append("circle")
//       .attr("r", 4.5);

//   focus.append("text")
//       .attr("x", 9)
//       .attr("dy", ".35em");

//   svg.append("rect")
//       .attr("class", "overlay")
//       .attr("width", width)
//       .attr("height", height)
//       .on("mouseover", function() { focus.style("display", null); })
//       .on("mouseout", function() { focus.style("display", "none"); })
//       .on("mousemove", mousemove);

//   function mousemove() {
//     var x0 = x.invert(d3.mouse(this)[0]),
//         i = bisectDate(data, x0, 1),
//         d0 = data[i - 1],
//         d1 = data[i],
//         d = x0 - d0.date > d1.date - x0 ? d1 : d0;
//     focus.attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")");
//     focus.select("text").text(d);
//   }
}
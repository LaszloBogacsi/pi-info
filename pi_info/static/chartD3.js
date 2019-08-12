const queryParams = window.location.search;
const requestInit = {
    method: 'GET',
    mode: 'cors',
    redirect: 'follow',
    headers: new Headers({
        'Content-Type': 'application/json'
    })
};

const urlParams = new URLSearchParams(queryParams);
const timeRange = urlParams.get("timerange");
const TODAY = "today";

// const url = "http://localhost:9080/sensor/data";
const url = "http://192.168.1.205:5000/sensor/data";
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
    // const dataXRange = d3.extent(timeScale);
    const dataXRange = timeScale;
    const average_temperature = d3.mean(dataset_temp);
// 2. Use the margin convention practice
    const margin = {top: 50, right: 50, bottom: 50, left: 50}
        , width = (window.innerWidth - margin.left - margin.right) * 0.9 // Use the window's width
        , height = (window.innerHeight - margin.top - margin.bottom) * 0.9; // Use the window's height

    const n = dataset_temp.length;

    const xScale = d3.scaleBand().domain(dataXRange).rangeRound([0, width]).padding(0.1);

    const domainMin = -10;
    const domainMax = 40;
    const yScale = d3.scaleLinear().domain([domainMin, domainMax]).range([height, 0]);
    const yScale2 = d3.scaleLinear().domain([0, 100]).range([height, 0]);
    const chartWideHorizontalLine = (y) => [{x: 0, y}, {x: width, y}];
    const line_average_temperature = d3.line()
        .x(d => d.x)
        .y(d => yScale(d.y));
    const line_humid = d3.line()
        .x((d, i)  => xScale(timeScale[i])+xScale.bandwidth() /2) // set the x values for the line generator
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
        .call(d3.axisBottom(xScale)
            .tickFormat(d3.timeFormat(timeRange === TODAY ? "%H:%M" : "%Y-%m-%d"))
            .tickValues(xScale.domain())); // Create an axis component with d3.axisBottom

// 4. Call the y axis in a group tag
    svg.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft
//  Call the right y axis in a group tag
    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + width + " ,0)")
        .call(d3.axisRight(yScale2)); // Create an axis component with d3.axisLeft

    const barPadding = 8;
    const barWidth = width / n;
    const tooltip = d3.select("body").append("div").attr("class", "toolTip");

    const temperatureBars = svg.selectAll("rect")
        .data(dataset_temp)
        .enter()
        .append("rect")
        .attr("class","temp-bars")
        .attr("y", d => yScale(d))
        .attr("height", d => height - yScale(d + domainMin))
        .attr("width", barWidth - barPadding)
        .attr("transform", (d, i) => {
            const cx = xScale(timeScale[i]);
            return `translate(${cx})`
        })
        .on("mousemove", function(d){
            tooltip
                .style("left", d3.event.pageX - 50 + "px")
                .style("top", d3.event.pageY - 70 + "px")
                .style("display", "inline-block")
                .html(d);
        })
        .on("mouseout", function(d){ tooltip.style("display", "none");});;

    const valueLabels = svg.selectAll(".text")
        .data(dataset_temp)
        .enter()
        .append("text")
        .attr("class","label")
        .attr("x", (d, i) => xScale(timeScale[i]) + (xScale.bandwidth() - barPadding)/2)
        .attr("y", function(d) { return yScale(d) + 1; })
        .attr("dy", "1em")
        .text(d => d3.format(".0f")(d));



// 9. Append the path, bind the data, and call the line generator
    svg.append("path")
        .datum(chartWideHorizontalLine(average_temperature)) // 10. Binds data to the line
        .attr("class", "line") // Assign a class for styling
        .attr("d", line_average_temperature); // 11. Calls the line generator
    // add another line for humidity
    svg.append("path")
        .datum(dataset_humidity) // 10. Binds data to the line
        .attr("class", "line2") // Assign a class for styling
        .attr("d", line_humid); // 11. Calls the line generator

// 12. Appends a circle for each datapoint
//     svg.selectAll(".dot")
//         .data(dataset_temp)
//         .enter().append("circle") // Uses the enter().append() method
//         .attr("class", "dot") // Assign a class for styling
//         .attr("cx", function (d, i) {
//             return xScale(timeScale[i])
//         })
//         .attr("cy", function (d) {
//             return yScale(d)
//         })
//         .attr("r", 5)
//         .on("mouseover", function (a, b, c) {
//             console.log(a);
//             this.setAttribute('class', 'focus')
//         })
//         .on("mouseout", function () {
//             this.removeAttribute('class', 'focus');
//             this.setAttribute('class', 'dot')
//
//         });
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
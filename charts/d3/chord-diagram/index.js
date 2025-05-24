// index.js
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
import { WebModel } from "../dist/useeio.js"; // adjust the path if needed

async function drawChordChart() {
  // Load the model
  const model = new WebModel({ 
    modelId: "USEEIOv2.0" // Example model id (change to yours if needed)
  });

  // Fetch dynamic data
  const sectors = await model.sectors();
  const indicators = await model.indicators();

  console.log("Sectors:", sectors);
  console.log("Indicators:", indicators);

  // Example dummy matrix - you should replace this with real model data
  const matrix = [
    [11975, 5871, 8916, 2868],
    [1951, 10048, 2060, 6171],
    [8010, 16145, 8090, 8045],
    [1013, 990, 940, 6907]
  ];

  // You probably want to build the matrix from `sectors` and `indicators`
  // I'll show you how below

  const width = 700;
  const height = 700;
  const outerRadius = Math.min(width, height) * 0.5 - 40;
  const innerRadius = outerRadius - 30;

  const chord = d3.chord()
    .padAngle(0.05)
    .sortSubgroups(d3.descending);

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

  const ribbon = d3.ribbon()
    .radius(innerRadius);

  const color = d3.scaleOrdinal(d3.schemeCategory10);

  const svg = d3.select("#chartHolder")
    .append("svg")
      .attr("viewBox", [-width / 2, -height / 2, width, height])
      .attr("width", width)
      .attr("height", height);

  const chords = chord(matrix);

  const group = svg.append("g")
    .selectAll("g")
    .data(chords.groups)
    .join("g");

  group.append("path")
    .attr("fill", d => color(d.index))
    .attr("stroke", d => d3.rgb(color(d.index)).darker())
    .attr("d", arc);

  group.append("text")
    .each(d => { d.angle = (d.startAngle + d.endAngle) / 2; })
    .attr("dy", "0.35em")
    .attr("transform", d => `
      rotate(${(d.angle * 180 / Math.PI - 90)})
      translate(${outerRadius + 5})
      ${d.angle > Math.PI ? "rotate(180)" : ""}
    `)
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : "start")
    .text(d => sectors[d.index]?.name || `Group ${d.index + 1}`);

  svg.append("g")
    .attr("fill-opacity", 0.67)
    .selectAll("path")
    .data(chords)
    .join("path")
      .attr("fill", d => color(d.target.index))
      .attr("stroke", d => d3.rgb(color(d.target.index)).darker())
      .attr("d", ribbon);
}

// Call the draw function
drawChordChart();

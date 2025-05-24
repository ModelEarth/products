function _1(md){return(
  md`
  <h1>D Matrix Chord Diagram</h1>
  
  Relates impacts to sectors
  
  Name array was manually copied from the Excel file in Feb 2024 report.
  
  TO DO: Copy this folder. Name it "chord-diagram-sectors" and use the L Matrix for Sector to Sector.  
  TO DO: Build array of colors using a D3 loop that matches the number of names.  
  TO DO: Pull matrix data directly from [Github files](https://github.com/ModelEarth/profile/tree/main/impacts/2020/GAEEIOv1.0-s-20/matrix) via [D Matrix raw URL](https://raw.githubusercontent.com/ModelEarth/profile/main/impacts/2020/GAEEIOv1.0-s-20/matrix/D.json)  
  TO DO: Activate rollovers like [nivo.rocks/chord](https://nivo.rocks/chord/)
  
  Important: To avoid breaking Github Pages build, deleted "env" folder from original download.
  `
)}
  
function _d3(require){return(
require("d3@7")
)}

function _colorbrewer(require){return(
require("d3-scale-chromatic")
)}

function _sectors(){return(
[
  "493 - Warehouses",
  "325 - Agricultural, pharmaceutical, industrial",
  "315AL - Clothing and leather",
  "111CA - Oilseeds, grains, vegetables, fruits",
  "113FF - Raw forest products, wild-caught fish",
  "484 - Truck transport",
  "22 - Electricity, natural gas, drinking water",
  "211 - Unrefined oil and gas",
  "313TT - Textiles and textile-derived products",
  "331 - Primary and secondary ferrous and non-ferrous"
]
)}

function _metrics(){return(
["ACID", "CRHW", "EUTR", "ETOX", "WATR", "GHG", "HAPS", "HCAN", "HNCN", "HRSP"]
)}

function _matrix(sectors,metrics)
{
  // Create sector-to-metric connections with updated data including the new metrics
  const data = [
    [2.9279, 24.3675, 1.6938, 3.9541, 20.5908, 1.8173, 279.3497, 491.7182, 4.4575, 302.5696], // 493
    [25.3771, 1.6387, 1.3250, 354.9863, 826.1331, 313.1327, 2.4721, 4.1522, 142.9947, 5.8519], // 325
    [26.0514, 13.0543, 2.1608, 154.1701, 4.9000, 245.7903, 3.3080, 6.9144, 15.0362, 64.3718], // 315AL
    [438.7223, 3.8138, 27.7301, 76.3876, 3.9133, 341.0706, 4.3666, 4.8566, 327.3158, 10.7287], // 111CA
    [25.8767, 20.8041, 3.6649, 22.2308, 7.9823, 33.5033, 386.3942, 1.0869, 1.4296, 2.7018], // 113FF
    [45.1819, 679.8645, 77.0468, 22.2075, 7.5457, 138.2528, 426.7344, 2.7728, 317.5354, 1.7300], // 484
    [34.2637, 1.1684, 10.1879, 395.1648, 3.8880, 358.6471, 367.5525, 4.0886, 173.3957, 3.6207], // 22
    [12.5601, 560.7083, 603.4255, 30.5271, 7.0923, 4.2475, 1.4126, 3.6556, 16.4984, 2.7640], // 211
    [10.9040, 13.5706, 638.6000, 32.6075, 46.9141, 8.6628, 2.8434, 11.5467, 52.5390, 599.5237], // 313TT
    [4.8355, 128.5149, 154.4909, 200.2108, 284.9512, 6.3800, 1.9989, 2.1401, 70.2356, 3.6533], // 331
  ];
  
  const fullMatrix = [];
  
  // Add sector-to-metric connections
  sectors.forEach((_, i) => {
    const row = new Array(sectors.length + metrics.length).fill(0);
    
    // Add connections to metrics
    for (let j = 0; j < metrics.length; j++) {
      row[sectors.length + j] = data[i][j];
    }
    
    fullMatrix.push(row);
  });
  
  // Add metric-to-sector connections
  metrics.forEach((_, i) => {
    const row = new Array(sectors.length + metrics.length).fill(0);
    
    // Add connections from metrics back to sectors
    for (let j = 0; j < sectors.length; j++) {
      row[j] = fullMatrix[j][sectors.length + i];
    }
    
    fullMatrix.push(row);
  });
  
  return fullMatrix;
}


function _chart(d3,sectors,metrics,matrix)
{
  const width = 900;
  const height = 900;
  const innerRadius = Math.min(width, height) * 0.35;
  const outerRadius = innerRadius + 20;
  
  // Create an improved color scale using colorbrewer schemes for better contrast
  const color = d3.scaleOrdinal()
    .domain([...sectors, ...metrics])
    .range(d3.schemePaired.concat(d3.schemeSet2, d3.schemeSet3));
  
  // Create chord layout with increased padding
  const chord = d3.chord()
    .padAngle(0.08)
    .sortSubgroups(d3.descending)
    .sortChords(d3.descending);
  
  // Generate chord diagram data
  const chords = chord(matrix);
  
  // Create SVG with increased size
  const svg = d3.create("svg")
    .attr("viewBox", [-width / 2, -height / 2, width, height])
    .attr("width", width)
    .attr("height", height)
    .attr("style", "max-width: 100%; height: auto;");
  
  // Add a white background circle for better contrast
  svg.append("circle")
    .attr("r", outerRadius + 100)
    .attr("fill", "#fff");
  
  // Create group arcs
  const group = svg.append("g")
    .selectAll("g")
    .data(chords.groups)
    .join("g");
  
  // Add arcs with stronger stroke for better definition
  group.append("path")
    .attr("fill", d => color(d.index < sectors.length ? 
                           sectors[d.index] : 
                           metrics[d.index - sectors.length]))
    .attr("d", d3.arc().innerRadius(innerRadius).outerRadius(outerRadius))
    .attr("stroke", "#fff")
    .attr("stroke-width", 2);
  
  // Add labels with improved positioning and readability
  group.append("text")
    .each(d => {
      d.angle = (d.startAngle + d.endAngle) / 2;
      d.name = d.index < sectors.length ? 
        sectors[d.index].split(" - ")[0] : 
        metrics[d.index - sectors.length];
    })
    .attr("dy", "0.35em")
    .attr("transform", d => `
      rotate(${(d.angle * 180 / Math.PI - 90)})
      translate(${outerRadius + 20})
      ${d.angle > Math.PI ? "rotate(180)" : ""}
    `)
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
    .text(d => d.name)
    .attr("font-size", "14px")
    .attr("font-weight", "bold")
    .attr("font-family", "Arial, sans-serif")
    .attr("fill", "#000");
  
  // Add chords with lower default opacity for less visual clutter
  const ribbons = svg.append("g")
    .attr("fill-opacity", 0.6)
    .selectAll("path")
    .data(chords)
    .join("path")
    .attr("class", "chord")
    .attr("d", d3.ribbon().radius(innerRadius))
    .attr("fill", d => color(d.source.index < sectors.length ? 
                          sectors[d.source.index] : 
                          metrics[d.source.index - sectors.length]))
    .attr("stroke", "#fff")
    .attr("stroke-width", 0.5);
  
  // Add tooltips
  ribbons.append("title")
    .text(d => {
      const sourceName = d.source.index < sectors.length ? 
        sectors[d.source.index] : 
        metrics[d.source.index - sectors.length];
      const targetName = d.target.index < sectors.length ? 
        sectors[d.target.index] : 
        metrics[d.target.index - sectors.length];
      return `${sourceName} → ${targetName}: ${d.source.value.toFixed(2)}`;
    });
  
  // Enhanced interactivity - highlight connections on hover
  group.on("mouseover", function(event, d) {
    // Dim all ribbons
    svg.selectAll(".chord")
      .attr("opacity", 0.1);
    
    // Highlight connected ribbons
    svg.selectAll(".chord")
      .filter(c => c.source.index === d.index || c.target.index === d.index)
      .attr("opacity", 0.9)
      .attr("stroke-width", 1.5);
    
    // Highlight the current segment
    d3.select(this).select("path")
      .attr("stroke-width", 3)
      .attr("stroke", "#000");
      
    // Make this segment's label more prominent
    d3.select(this).select("text")
      .attr("font-size", "16px")
      .attr("font-weight", "bold")
      .attr("fill", "#000");
      
  }).on("mouseout", function() {
    // Restore original appearance
    svg.selectAll(".chord")
      .attr("opacity", 0.6)
      .attr("stroke-width", 0.5);
      
    group.selectAll("path")
      .attr("stroke-width", 2)
      .attr("stroke", "#fff");
      
    group.selectAll("text")
      .attr("font-size", "14px")
      .attr("font-weight", "bold")
      .attr("fill", "#000");
  });
  
  
  
  return svg.node();
}


export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("d3")).define("d3", ["require"], _d3);
  main.variable(observer("colorbrewer")).define("colorbrewer", ["require"], _colorbrewer);
  main.variable(observer("sectors")).define("sectors", _sectors);
  main.variable(observer("metrics")).define("metrics", _metrics);
  main.variable(observer("matrix")).define("matrix", ["sectors","metrics"], _matrix);
  main.variable(observer("chart")).define("chart", ["d3","sectors","metrics","matrix"], _chart);
  return main;
}

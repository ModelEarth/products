function _1(md) {
  return (
    md`
    <h1>D Matrix Chord Diagram</h1>
    Relates impacts to sectors
    
    Name array was manually copied from the Excel file in Feb 2024 report.
    
    TO DO: Copy this folder. Name it "chord-diagram-sectors" and use the L Matrix for Sector to Sector.  
    Completed : Build array of colors using a D3 loop that matches the number of names. - Trinadh Rayala
    TO DO: Pull matrix data directly from [Github files](https://github.com/ModelEarth/profile/tree/main/impacts/2020/GAEEIOv1.0-s-20/matrix) via [D Matrix raw URL](https://raw.githubusercontent.com/ModelEarth/profile/main/impacts/2020/GAEEIOv1.0-s-20/matrix/D.json)  
    Completed : Activate rollovers like [nivo.rocks/chord](https://nivo.rocks/chord/) - Trinadh Rayala
    
    Important: To avoid breaking Github Pages build, deleted "env" folder from original download.
    `
  );
}

function _groupTicks(d3) {
  return (
    function groupTicks(d, step) {
      const k = (d.endAngle - d.startAngle) / d.value;
      return d3.range(0, d.value, step).map(value => {
        return { value: value, angle: value * k + d.startAngle };
      });
    }
  );
}

function _chart(data, d3, groupTicks) {
  const width = 800;
  const height = width + 100;
  const { names, colors } = data;
  const outerRadius = Math.min(width, height) * 0.5 - 60;
  const innerRadius = outerRadius - 10;
  const tickStep = d3.tickStep(0, d3.sum(data.flat()), 100);
  const formatValue = d3.format(".1~%");

  const chord = d3.chord()
    .padAngle(10 / innerRadius)
    .sortSubgroups(d3.descending)
    .sortChords(d3.descending);

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

  const ribbon = d3.ribbon()
    .radius(innerRadius - 1)
    .padAngle(1 / innerRadius);

  const color = d3.scaleOrdinal(names, colors);

  const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [-width / 2, -height / 2, width, height])
    .attr("style", "width: 100%; height: auto; font: 10px sans-serif;");

  //  Tooltip div 
  const tooltip = d3.select("body")
    .append("div")
    .attr("class", "tooltip")
    .style("position", "absolute")
    .style("visibility", "hidden")
    .style("background", "#fff")
    .style("border", "1px solid #ccc")
    .style("padding", "8px")
    .style("border-radius", "4px")
    .style("font", "12px sans-serif")
    .style("pointer-events", "none")
    .style("z-index", "10");

  const chords = chord(data);

  //  Group Arcs
  const group = svg.append("g")
    .selectAll("g")
    .data(chords.groups)
    .join("g");

  group.append("path")
    .attr("fill", d => color(names[d.index]))
    .attr("d", arc)
    .on("mouseover", (event, d) => {
      tooltip
        .html(`<strong>${names[d.index]}</strong><br/>Total: ${formatValue(d.value)}`)
        .style("visibility", "visible");
    })
    .on("mousemove", event => {
      tooltip
        .style("top", (event.pageY + 10) + "px")
        .style("left", (event.pageX + 10) + "px");
    })
    .on("mouseout", () => tooltip.style("visibility", "hidden"));

  const groupTick = group.append("g")
    .selectAll("g")
    .data(d => groupTicks(d, tickStep))
    .join("g")
    .attr("transform", d => `rotate(${d.angle * 180 / Math.PI - 90}) translate(${outerRadius},0)`);

  groupTick.append("line")
    .attr("stroke", "currentColor")
    .attr("x2", 6);

  groupTick.append("text")
    .attr("x", 8)
    .attr("dy", "0.35em")
    .attr("transform", d => d.angle > Math.PI ? "rotate(180) translate(-16)" : null)
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
    .text(d => formatValue(d.value));

  group.append("text")
    .attr("dy", "-1em")
    .attr("text-anchor", "middle")
    .attr("transform", d => {
      const angle = (d.startAngle + d.endAngle) / 2;
      const rotate = angle * 180 / Math.PI - 90;
      const x = Math.cos(angle) * (outerRadius + 10);
      const y = Math.sin(angle) * (outerRadius + 10);
      return `translate(${x},${y}) rotate(${rotate})`;
    })
    .text(d => names[d.index]);

  //  Ribbons
  svg.append("g")
    .attr("fill-opacity", 0.8)
    .selectAll("path")
    .data(chords)
    .join("path")
    .style("mix-blend-mode", "multiply")
    .attr("fill", d => color(names[d.source.index]))
    .attr("d", ribbon)
    .on("mouseover", (event, d) => {
      tooltip
        .html(
          `<strong>${names[d.source.index]}</strong> → <strong>${names[d.target.index]}</strong><br/>
          Value: ${formatValue(d.source.value)}`
        )
        .style("visibility", "visible");
    })
    .on("mousemove", event => {
      tooltip
        .style("top", (event.pageY + 10) + "px")
        .style("left", (event.pageX + 10) + "px");
    })
    .on("mouseout", () => tooltip.style("visibility", "hidden"));

  return svg.node();
}

async function _data() {
  const matrixURL = "https://raw.githubusercontent.com/ModelEarth/profile/main/impacts/2020/GAEEIOv1.0-s-20/matrix/D.json";
  const metaURL = "https://raw.githubusercontent.com/ModelEarth/profile/main/impacts/2020/GAEEIOv1.0-s-20/sectors.json";

  const [matrix, meta] = await Promise.all([
    fetch(matrixURL).then(res => res.json()),
    fetch(metaURL).then(res => res.json())
  ]);

  const names = meta.map(d => d.id);

  // const colors = d3.scaleOrdinal()
  //   .domain(names)
  //   .range(d3.schemeCategory10); // Use D3's color scale (Category10 for example)

   // Generate an array of colors, cycling through D3 schemes if needed

   const colorScheme = d3.schemeCategory10;
   const colors = names.map((_, i) => colorScheme[i % colorScheme.length]);

  return Object.assign(matrix, {
    names: names,
    colors: colors
  });
}

export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("chart")).define("chart", ["data", "d3", "groupTicks"], _chart);
  main.variable(observer("groupTicks")).define("groupTicks", ["d3"], _groupTicks);
  main.variable(observer("data")).define("data", _data);
  return main;
}

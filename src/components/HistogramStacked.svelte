<script>
	import { onMount } from 'svelte';
	import {
    select as d3Select,
    scaleLinear,
    max,
    scaleBand,
    axisBottom,
    axisLeft,
    stack as d3Stack,
    stackOrderNone,
    stackOffsetNone
  } from 'd3';
  import { send } from '../query.util'

  export let documentId

  const height = 450;
  const margin = {
    top: 5,
    right: 0,
    bottom: 25,
    left: 125
  }
  const width = Math.max(Math.min(window.innerWidth, 750), 300) - margin.left - margin.right - 10

  const legendCellSize = width > 500 ? 20 : 15

  $: drawGraph(documentId)

  async function drawGraph(id) {
    let data = await send('/api/projectAuteurSort', {documentId: id})
    
    const keys = [
      "Irrecevable 40",
      "A discuter",
      "Rejeté",
      "En traitement",
      "En recevabilité",
      "Retiré",
      "Irrecevable",
      "Adopté",
      "Non soutenu",
      "Tombé"
    ]

    const heightContent = data.length * 14
    // let data = [
    //   { auteur: "A", d: 3, e: 4, f: 5 },
    //   { auteur: "B", d: 3, e: 14, f: 5 },
    //   { auteur: "C", d: 3, e: 24, f: 5 },
    // ]
    // const keys = ["d", "e", "f"]

    const colors = ["#f7fcf0", "#e0f3db", "#ccebc5", "#a8ddb5", "#7bccc4", "#4eb3d3", "#2b8cbe", "#0868ac", "#084081", "#002000"]


    var stack = d3Stack()
        .keys(keys)
        .order(stackOrderNone)
        .offset(stackOffsetNone);

    var series = stack(data);

    const x = scaleLinear()
			.domain([0, max(series[series.length - 1], d => d[1] || d[0])])
			.range([0, width - 10])

		const y = scaleBand()
      .domain(data.map(d => d.auteur))
			.range([0, heightContent])
      .padding(0.15)

    // chart
    const svg = d3Select("#chart").html("")
			.attr("style", `width: ${width + margin.left}px;`)
      .append('div')
			.attr("style", `height: ${height}px;` +
                     `width: ${width + margin.left}px;` +
                     `overflow-y: auto;` +
                     `overflow-x: hidden;`)
    .append("svg")
      .attr("id", "svg")
      .attr("width", width + margin.left)
      .attr("height", heightContent + margin.top)
      .append("g")
    	.attr("transform", `translate(${margin.left}, ${margin.top})`);

    let groups = svg
    .selectAll("g")
      .data(series)
      .enter()
        .append("g")
        .style("fill", (d, i) => colors[i]);

    // bar
    let rect = groups.selectAll("rect")
      .data(d => d)
      .enter()
        .append("rect")
        .attr("x", d => x(d[0]))
        .attr("width", d => x(d[1] - d[0]))
        .attr("y", d => y(d.data.auteur))
        .attr("height", d => y.bandwidth());

    // axis left
    svg.append("g")
      .call(axisLeft(y).tickSize(0))
      .selectAll("text")	
      .attr('class', 'axis')
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", ".15em")

      // axis bottom
    d3Select("#chart")
      .append('div')
      .append('svg')
			.attr("width", width + margin.left)
      .attr("height", margin.bottom)
      .attr("font-family", "sans-serif")
      .attr("font-size", "14")
      .attr("text-anchor", "end")
      .append("g")
      .attr("transform", "translate(" + margin.left + ", 0)")
      .call(axisBottom(x).ticks(6));

    let reverseColors = colors.reverse(); // Pour présenter les catégories dans le même sens qu'elles sont utilisées
    let reverseKeys = keys.reverse();

    const legendHeight = colors.length * legendCellSize

    let legend = d3Select('#chart')
      .append('svg')
      .attr('style', `position: absolute;` +
                      `bottom: 40px;` +
                      `right: 10px;` +
                      `height: ${legendHeight}px;` +
                      `width: 125px;`)
        
    legend.selectAll()
        .data(reverseColors)
        .enter().append('rect')
            .attr('height', legendCellSize + 'px')
            .attr('width', legendCellSize + 'px')
            .attr('x', 0)
            .attr('y', (d,i) => i * legendCellSize)
            .style("fill", d => d);
    
    legend.selectAll()
        .data(reverseKeys)
        .enter().append('text')
            .attr('class', 'legend')
            .attr("transform", (d,i) => "translate(" + (legendCellSize + 5) + ", " + (i * legendCellSize) + ")")
            .attr("dy", legendCellSize / 1.6) // Pour centrer le texte par rapport aux carrés
            .style("font-size", "13px")
            .style("fill", "grey")
            .text(d => d);
  }
</script>

<style>
  #chart {
    position: relative;
  }
  :global(.legend), :global(.axis) {
    fill: #333;
    font-variant: small-caps;
  }
</style>

<h2>Nombre d'amendements par député</h2>
<div id="chart"></div>
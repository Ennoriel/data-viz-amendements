<script>
	import { onMount } from 'svelte';
  import * as pkg from 'd3';
  const {
    scaleLinear,
    max,
    scaleBand,
    axisBottom,
    axisLeft,
    stackOrderNone,
    stackOffsetNone
  } = pkg;
  const d3Select = pkg.select
  const d3Stack = pkg.stack

  export let data
  export let getXVal

  let height;
  let margin = {
    top: 5,
    right: 0,
    bottom: 25,
    left: 150
  }
  const width = Math.max(Math.min(window.innerWidth, 750), 300) - margin.left - margin.right - 10
  const randomNumber = Math.floor(Math.random() * 100000000)

  const legendCellSize = width > 500 ? 20 : 15

  onMount(drawGraph)

  async function drawGraph() {

    const keys = [
      ...new Set(data.reduce((acc, val) => [...acc, ...Object.keys(val).filter(key => !getXVal({[key]: 42}) && key !== 'count')], []))
    ].sort()

    margin.left = 6 * data.reduce((acc, val) => Math.max(acc, getXVal(val).length), 0)

    const heightContent = data.length * 14
    height = Math.min(400, heightContent + 10)

    let colors
    
    if(keys.length === 3) {
      colors = ["#ccebc5", "#4eb3d3", "#084081"]
    } else {
      colors = distributedCopy([
      "#f7fcf0",
      "#e0f3db",
      "#ccebc5",
      "#a8ddb5",
      "#7bccc4",
      "#4eb3d3",
      "#2b8cbe",
      "#0868ac",
      "#084081",
      "#002000"
    ], keys.length)
    }


    var stack = d3Stack()
        .keys(keys)
        .order(stackOrderNone)
        .offset(stackOffsetNone);

    var series = stack(data);

    const x = scaleLinear()
			.domain([0, max(series[series.length - 1], d => d[1] || d[0])])
			.range([0, width - 10])

		const y = scaleBand()
      .domain(data.map(getXVal))
			.range([0, heightContent])
      .padding(0.15)

    // chart
    const svg = d3Select(`#chart-${randomNumber}`).html("")
			.attr("style", `width: ${width + margin.left}px;` +
                      `position: relative;`)
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
        .attr("y", d => y(getXVal(d.data)))
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
    d3Select(`#chart-${randomNumber}`)
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

    let reverseColors = colors.reverse();
    let reverseKeys = keys.reverse();

    const legendHeight = colors.length * legendCellSize

    let legend = d3Select(`#chart-${randomNumber}`)
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

  /**
   * Retrieve a fixed number of elements from an array, evenly distributed but
   * always including the first and last elements.
   *
   * @param   {Array} items - The array to operate on.
   * @param   {number} n - The number of elements to extract.
   * @returns {Array}
   */
  function distributedCopy(items, n) {
      var elements = [items[0]];
      var totalItems = items.length - 2;
      var interval = Math.floor(totalItems/(n - 2));
      for (var i = 1; i < n - 1; i++) {
          elements.push(items[i * interval]);
      }
      elements.push(items[items.length - 1]);
      return elements;
  }
</script>

<style>
  /* #chart {
    position: relative;
  } */
  :global(.legend), :global(.axis) {
    fill: #333;
    font-variant: small-caps;
  }
</style>

<div id={`chart-${randomNumber}`}></div>
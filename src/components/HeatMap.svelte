<script>
	import { onMount } from 'svelte';
	import {
    select as d3Select,
    range,
    sum,
    scaleLinear,
    scaleLog,
    max,
    axisBottom,
  } from 'd3';
  import { send } from '../query.util'

  export let documentId
  export let acteurId

  const margin = {
    top: 50,
    right: 0,
    bottom: 10,
    left: 75
  }

  const months = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre']
  const days = range(31).map(v => v + 1)

  const width = Math.max(Math.min(window.innerWidth, 750), 300) - margin.left - margin.right - 10
  const gridSize = {
    x: Math.floor(width / days.length),
    y: Math.max(15, Math.floor(width / days.length))
  }

  let data = []

  let monthsToDraw
  let minMonth
  let maxMonth
  let height

  let numStops = 3;
  
  let colorScale
  let countScale
  let countPoint

  $: drawGraph(documentId, acteurId)

  async function drawGraph(documentId, acteurId) {
    data = await send('/api/projectDayMonth', { year: 2020, documentId, acteurId })

    data = data.filter(val => !!val._id)
              .map(val => ({year: val._id, data: val.data}))
              .sort((val1, val2) => val1.year - val2.year)

    d3Select('#heat-map').html("").attr('style', `width: ${width + margin.left + margin.right}px;`)

    if (data.length) {
      initColorScale(data.reduce((acc, val) => [...acc, ...val.data], []))
      data.forEach(v => drawYear(v.year, v.data))
      drawColorScale(data.reduce((acc, val) => [...acc, ...val.data], []))
    }
  }

  function formatNumber(number) {
    return number.toString()
                  .split('').reverse().join('') // reverse number
                  .match(/\d{1,3}/g).join(' ')  // add spaces every 3 digits
                  .split('').reverse().join('') // reverse number
  }

  function initColorScale(values) {
    colorScale = scaleLog()
      .domain([1, max(values, d => d.count) / 2, max(values, d => d.count)])
      .range(["#f7fbff", "#6baed6", "#08306b"]);
      
    countScale = scaleLinear()
      .domain([0, max(values, d => d.count)])
      .range([0, width])

    countPoint = [0, max(values, d => d.count) / 2, max(values, d => d.count)];
  }

  function drawYear(year, values) {

    minMonth = values.reduce((acc, v) => Math.min(acc, v.month), 12)
    maxMonth = values.reduce((acc, v) => Math.max(acc, v.month), 0)
    monthsToDraw = months.slice(minMonth - 1, maxMonth)
    height = gridSize.y * monthsToDraw.length

    let chart = drawSvgWrapper()
    drawSubtitle(chart, year, values)

    drawMonthGraph(chart, values)
    drawMonthAxis(chart)
  }

  function drawSvgWrapper() {
    return d3Select('#heat-map')
      .append("svg")
      .attr("class", "svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  }

  function drawSubtitle(chart, year, values) {
    chart.append("text")
      .attr("class", "subtitle")
      .attr("x", width / 2)
      .attr("y", -25)
      .style("text-anchor", "middle")
      .text(` - ${year} - ${formatNumber(sum(values, d => d.count))} amendements - `);
  }

  function drawMonthGraph(chart, values) {

    chart.selectAll(".hour")
      .data(values)
      .enter().append("rect")
        .attr("x", d => ( d.day - 1 ) * gridSize.x)
        .attr("y", d => ( d.month - minMonth ) * gridSize.y)
        .attr("width", gridSize.x)
        .attr("height", gridSize.y)
        .style("stroke", "white")
        .style("stroke-opacity", 0.6)
        .style("fill", function(d) { return colorScale(d.count); });
  }

  function drawMonthAxis(chart) {
    chart.selectAll(".month-label")
      .data(monthsToDraw)
      .enter().append("text")
        .text(function (d) { return d; })
        .attr("x", 0)
        .attr("y", (d, i) => i * gridSize.y)
        .attr("transform", "translate(-6, 12)")
        .attr("class", "month-label")
        .style("text-anchor", "end");

    let daysAxis = width > 450 ? days : days.map((d, i) => i % 2 ? '' : d)
    chart.selectAll(".day-label")
      .data(daysAxis)
      .enter().append("text")
        .text(d => d)
        .attr("x", (d, i) => i * gridSize.x)
        .attr("y", 0)
        .attr("transform", "translate(" + gridSize.x / 2 + ", -6)")
        .attr("class", "day-label")
        .style("text-anchor", "middle");
  }

  function drawColorScale(values) {
    let chart = d3Select('#heat-map')
      .append("svg")
      .attr("class", "svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", 100)
      .append("g")
        .attr("transform", "translate(" + (margin.left - margin.right) / 2 + ", 50)");

    chart.append("defs")
    .append("linearGradient")
    .attr("id", "legend-traffic")
    .attr("x1", "0%").attr("y1", "0%")
    .attr("x2", "100%").attr("y2", "0%")
    .selectAll("stop") 
    .data(range(numStops))                
    .enter().append("stop") 
      .attr("offset", function(d,i) { 
          return countScale(countPoint[i]) / width;
      })   
      .attr("stop-color", function(d,i) { 
          return colorScale(countPoint[i]); 
      });

    let legendWidth = Math.min(width * 0.8, 400);
    
    // groupe principal
    let legendsvg = chart.append("g") 
      .attr("class", "legendWrapper")
      .attr("transform", "translate(" + (width/2) + ", 0)");

    // rectangle avec gradient
    legendsvg.append("rect")
      .attr("class", "legendRect")
      .attr("x", -legendWidth/2)
      .attr("y", 0)
      .attr("width", legendWidth)
      .attr("height", 10)
      .style("fill", "url(#legend-traffic)");
          
    // légende
    legendsvg.append("text") 
      .attr("class", "legendTitle")
      .attr("x", 0)
      .attr("y", -10)
      .style("text-anchor", "middle")
      .text("Nombre d'Amendements");

    // scale pour x-axis
    let xScale = scaleLog()
      .range([-legendWidth / 2, legendWidth / 2])
      .domain([ 1, max(values, d => d.count)] );  

    // x axis
    legendsvg.append("g") 
      .attr("transform", "translate(0, 10)")
      .call(axisBottom(xScale).ticks(4, "d"));
  }
</script>

<style>
  :global(.subtitle), :global(.month-label), :global(.day-label) {
    fill: #333;
    font-size: .8em;
    font-variant: small-caps;
  }
  :global(.subtitle) {
    fill: #777
  }
</style>

<h2>Nombre d'amendements par jour</h2>

{#if data.length}
  <div id="heat-map"></div>
{:else}
  <p>Pas d'amendement</p>
{/if}
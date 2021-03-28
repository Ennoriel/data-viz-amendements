<script>
	import {
    scaleTime,
    scaleLinear,
    line as d3Line,
    select as d3Select,
    extent as d3extent,
    axisBottom,
    axisLeft,
    timeYear,
    max,
    utcMonth as d3UtcMonth
  } from 'd3';
  import { send } from '../query.util'

  const ref = {
    sorts: [
      'A discuter',
      'Adopté',
      'En recevabilité',
      'En traitement',
      'Irrecevable 40',
      'Irrecevable',
      'Non soutenu',
      'Rejeté',
      'Retiré',
      'Tombé'
    ]
  }

  let sort = 'Irrecevable'

  const margin = {
    top: 10,
    right: 0,
    bottom: 20,
    left: 50
  }

  const width = 350
  const innerWidth = width - margin.left - margin.right - 10
  const height = 140
  const innerHeight = height - margin.top - margin.bottom - 10

  const x = scaleTime()
    .range([0, innerWidth]);

  const y = scaleLinear()
    .range([innerHeight, 0]);

  const line = d3Line()
    .x(d => x(d.date))
    .y(d => y(d.pourcentage));

  let data
  let gridData
  let flatData

  $: loadCharts(sort)

  function loadCharts() {
    send('/api/projectNewSortDate', {sort}).then(res => {

      data = res.groupRecords.map(groupRecord => ({
                groupe: groupRecord.groupe,
                records: groupRecord.records.map(record => ({...record, date: new Date(record.date) }))
            }))
      flatData = data.reduce((acc, record) => [...acc, ...record.records], [])
      data.sort((val1, val2) => val1.groupe.localeCompare(val2.groupe))
      gridData = data.reduce((acc, val, index) => {
        let pos = Math.floor(index / 3)
        if (pos === acc.length - 1) {
          acc[pos].push({...val, index})
        } else {
          acc.push([{...val, index}])
        }
        return acc
      }, [])
      
      drawCharts()
    })
  }

  function drawCharts() {
    x.domain(d3extent(flatData, d => d.date));
    y.domain([0, max(flatData, d => d.pourcentage)]);

    const svg = d3Select("#svg-linear").html("")
      .attr("width", width * 3)
      .attr("height", height * 4)
  
    // row = 3 graphs
    svg.selectAll('.row')
      .data(gridData)
      .join('g')
      .attr('class', 'row')
      .attr("transform", (d, i) => "translate(0," + height * i + ")")

      // graph container
      .selectAll('.graph')
        .data(d => d)
        .join('g')
        .attr('class', 'graph')
        .attr("transform", (d, i) => `translate(${ width * i }, 0)`)

      // groupe name
      .append("text")
        .attr('class', 'legend-groupe')
        .attr('x', margin.left + 5)
        .attr('y', margin.top + 5)
        .text(d => d.groupe)
        .select(function() {return this.parentNode})
      
      // container with margins
      .append("g")
        .attr('class', d => `series-${d.index}`)
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

      // x axis (primary and secondary)
      .append("g")
        .attr("class", "axis-secondary")
        .attr("transform", "translate(0," + innerHeight + ")")
        .call(axisBottom(x).ticks(d3UtcMonth.every(1), ""))
        .select(function() {return this.parentNode})
      .append("g")
        .attr("transform", "translate(0," + innerHeight + ")")
        .call(axisBottom(x).ticks(timeYear))
        .select(function() {return this.parentNode})

      // y axis
      .append("g")
        .call(axisLeft(y).ticks(5, ".0%"))
        .select(function() {return this.parentNode})

      // series
      .selectAll('.series') 
      .data(d => {
        return data.map((v, i) => ({...v, highlight: i === d.index}))
      })
      .join('path')
        .attr("class", d => d.highlight ? "series series-highlight" : "series")
        .style("mix-blend-mode", "multiply")
        .attr("d", d => line(d.records))

    // const svg = drawContainer()
    // drawXAxis(svg)
    // drawYAxis(svg)
    // drawSeries(svg)
  }

  function drawContainer() {
    return d3Select("#svg-linear").html("")
      .attr("width", innerWidth + margin.left + margin.right)
      .attr("height", innerHeight + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  }

  function drawXAxis(svg) {
    svg.append("g")
        .attr("class", "axis-secondary")
        .attr("transform", "translate(0," + innerHeight + ")")
        .call(axisBottom(x).ticks(d3UtcMonth.every(1), ""));

    svg.append("g")
        .attr("transform", "translate(0," + innerHeight + ")")
        .call(axisBottom(x).ticks(timeYear));
  }

  function drawYAxis(svg) {
    svg.append("g")
        .call(axisLeft(y).ticks(5, ".0%"))
  }

  function drawSeries(svg) {
    svg.selectAll(".series")
      .data(data)
      .join("path")
        .attr("class", "series")
        .style("mix-blend-mode", "multiply")
        .attr("d", d => line(d.records));
  }
</script>

<style>
  :global(.series) {
    fill: none;
    stroke: #ccc;
    stroke-width: 0.5px;
  }

  :global(.series-highlight) {
    stroke: red;
    stroke-width: 1.5px;
  }

  :global(.horizontalGrid) {
    fill: none;
    shape-rendering: crispEdges;
    stroke: lightgrey;
    stroke-width: 1px;
  }

  :global(.axis-secondary) {
    color: #BBB
  }

  :global(.legend-groupe) {
    font-size: 10px;
    font-family: sans-serif;
  }
</style>

<h3>Filtrer par sort</h3>
<!-- svelte-ignore a11y-no-onchange -->
<select bind:value={sort}>
  {#each ref.sorts as refSort}
    <option value={refSort}>{refSort}</option>
  {/each}
</select>

<div>
  <svg id="svg-linear"/>
</div>
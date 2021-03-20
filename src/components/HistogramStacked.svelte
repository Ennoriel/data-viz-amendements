<script>
	import { onMount } from 'svelte';
	import {
    select as d3Select,
    range,
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

  const width = 500;
  const height = 500;
  const padding = {
    top: 25,
    right: 25,
    bottom: 25,
    left: 100
  }
  const legendCellSize = 20
  const tooltipWidth = 210;

  let documentId
  let ref = {}

	onMount(() => {
    drawGraph()
    loadDocuments()
  })

  async function loadDocuments() {
    ref.documents = await send('http://localhost:3456/api/documents')
  }

  async function drawGraph(documentId) {
    let data = await send('http://localhost:3456/api/projectAuteurSort', documentId)
    // const keys = [...new Set(data.reduce((acc, d) => [...acc, ...Object.keys(d)], []))];
    // keys.splice(keys.findIndex(k => k === 'auteur'), 1).sort()
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

    const heightContent = data.length * 10
    // let data = [
    //   { auteur: "A", d: 3, e: 4, f: 5 },
    //   { auteur: "B", d: 3, e: 14, f: 5 },
    //   { auteur: "C", d: 3, e: 24, f: 5 },
    // ]
    // const keys = ["d", "e", "f"]

    // console.log('keys')
    // console.log(keys)
    // console.log('data')
    // console.log(data)
    const colors = ["#f7fcf0", "#e0f3db", "#ccebc5", "#a8ddb5", "#7bccc4", "#4eb3d3", "#2b8cbe", "#0868ac", "#084081", "#002000"]


    var stack = d3Stack()
        .keys(keys)
        .order(stackOrderNone)
        .offset(stackOffsetNone);

    var series = stack(data);
    // console.log('series')
    // console.log(series)
    
    // console.log('max')
    // console.log(max(series[series.length - 1], d => d[1] || d[0]))

    const x = scaleLinear()
			.domain([0, max(series[series.length - 1], d => d[1] || d[0])])
			.range([0, width])

		const y = scaleBand()
      .domain(data.map(d => d.auteur))
			.range([0, heightContent])
      .padding(0.1)

    // chart
    const svg = d3Select("#chart")
    .append('div')
			.attr("style", `height: ${height}px;` +
                     `overflow-y: auto;`)
    .append("svg")
      .attr("id", "svg")
      .attr("width", width+ padding.left)
      .attr("height", heightContent)
      .append("g")
    	.attr("transform", "translate(" + padding.left + ", 0)");

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
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", ".15em")

      // axis bottom
    d3Select("#chart")
      .append('div')
      .append('svg')
			.attr("width", width + padding.left)
      .attr("height", padding.bottom)
      .attr("font-family", "sans-serif")
      .attr("font-size", "14")
      .attr("text-anchor", "end")
      .append("g")
      .attr("transform", "translate(" + padding.left + ", 0)")
      .call(axisBottom(x).ticks(6));

      addLegend(keys, colors)
  }

  function addLegend(keys, colors) {
    let reverseColors = colors.reverse(); // Pour présenter les catégories dans le même sens qu'elles sont utilisées
    let reverseKeys = keys.reverse();

    const legendHeight = colors.length * legendCellSize

    let legend = d3Select('#chart')
      .append('svg')
      .attr('style', `position: absolute;` +
                      `top: ${height - legendHeight}px;` +
                      `left: ${width - 50}px;` +
                      `height: ${legendHeight}px`)
      .append('g')
        // .attr('transform', 'translate(10, 20)'); // Représente le point précis en haut à gauche du premier carré de couleur
        
    // Pour chaque couleur, on ajoute un carré toujours positionné au même endroit sur l'axe X et décalé en fonction de la 
    // taille du carré et de l'indice de la couleur traitée sur l'axe Y
    legend.selectAll()
        .data(reverseColors)
        .enter().append('rect')
            .attr('height', legendCellSize + 'px')
            .attr('width', legendCellSize + 'px')
            .attr('x', 5)
            .attr('y', (d,i) => i * legendCellSize)
            .style("fill", d => d);
    
    // On procéde de la même façon sur les libellés avec un positionement sur l'axe X de la taille des carrés 
    // à laquelle on rajoute 10 px de marge
    legend.selectAll()
        .data(reverseKeys)
        .enter().append('text')
            .attr("transform", (d,i) => "translate(" + (legendCellSize + 10) + ", " + (i * legendCellSize) + ")")
            .attr("dy", legendCellSize / 1.6) // Pour centrer le texte par rapport aux carrés
            .style("font-size", "13px")
            .style("fill", "grey")
            .text(d => d);
  }

  function onDocumentChange() {
    d3Select("#chart").html("")
    drawGraph({documentId})
  }
</script>

<!-- svelte-ignore a11y-no-onchange -->
<select
  bind:value={documentId}
  on:change={onDocumentChange}
>
  <option value={''} />
  {#if ref.documents}
    {#each ref.documents as refDocument}
      <option value={refDocument.uid}>{refDocument.titre}</option>
    {/each}
  {/if}
</select>
<div id="chart"></div>
<script>
  import Spinner from '$lib/Spinner.svelte'
	import { onMount } from 'svelte';
	import { ref } from '$lib/stores/ref.js';
  import { send } from '$lib/query.util'
  import * as pkg from 'd3';
  const d3Select = pkg.select;
  
  import * as pkgSankey from 'd3-sankey';
  const d3Sankey = pkgSankey.sankey;
  const d3SankeyLinkHorizontal = pkgSankey.sankeyLinkHorizontal;

  // const inputOrder = "justify" // center, right, left
  const padding = 10
  let width
  const height = 400
  const color = "#EEEEEEEE"

  let documentIds = ['PRJLANR5L15B2623', 'PRJLANR5L15B3360']
  let acteurIds = ["PA605036", "PA721474"]

  let rawData = {}
  let sankeyData = {}
  let working

  onMount(loadGraph)
  
  async function loadGraph() {
    working = true

    width = Math.max(Math.min(window.innerWidth, 750), 300) - 10

    const svg = d3Select('#svg-sankey').html("")

    rawData.links = await send(fetch, '/api/graph/sankey', {documentIds, acteurIds})
    rawData.nodes = rawData.links.reduce((acc, link) => {
      acc.push(link.source)
      acc.push(link.target)
      return acc
    }, [])
    rawData.nodes = [...new Set(rawData.nodes)].sort().map(v => ({name: v}))

    let sankey = d3Sankey()
      .nodeId(d => d.name)
      // .nodeAlign(d3[`sankey${align[0].toUpperCase()}${align.slice(1)}`])
      .nodeSort(null)
      .nodeWidth(15)
      .nodePadding(padding)
      .extent([[0, 5], [width, height - 5]])

    sankeyData = sankey({
      nodes: rawData.nodes.map(d => Object.assign({}, d)),
      links: rawData.links.map(d => Object.assign({}, d))
    });

    svg.style("background", "#fff")
      .attr("width", width)
      .attr("height", height);

    svg.append("g")
      .selectAll("rect")
      .data(sankeyData.nodes)
      .join("rect")
        .attr("x", d => d.x0 + 1)
        .attr("y", d => d.y0)
        .attr("height", d => d.y1 - d.y0)
        .attr("width", d => d.x1 - d.x0 - 2)
        .attr("fill", 'black')
      .append("title")
        .text(d => `${d.name}\n${d.value.toLocaleString()}`);

    const link = svg.append("g")
        .attr("fill", "none")
      .selectAll("g")
      .data(sankeyData.links)
      .join("g")
        .attr("stroke", color)
        .style("mix-blend-mode", "multiply");

    link.append("path")
        .attr("d", d3SankeyLinkHorizontal())
        .attr("stroke-width", d => Math.max(1, d.width));

    link.append("title")
        .text(d => `${d.source.name} → ${d.target.name}\nnombre d'amandements : ${d.value.toLocaleString()}`);

    svg.append("g")
        .style("font", "10px sans-serif")
      .selectAll("text")
      .data(sankeyData.nodes)
      .join("text")
        .attr("x", d => d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6)
        .attr("y", d => (d.y1 + d.y0) / 2)
        .attr("dy", "0.35em")
        .attr("text-anchor", d => d.x0 < width / 2 ? "start" : "end")
        .text(d => d.name)
      .append("tspan")
        .attr("fill-opacity", 0.7)
        .text(d => ` - ${d.value.toLocaleString()}`);

    working = false
  }

</script>

<style>
  select {
    padding-bottom: 10em;
  }
</style>

<h3>Filtrer par projet de loi (multiselection)</h3>
<!-- svelte-ignore a11y-no-onchange -->
<select bind:value={documentIds} multiple>
  {#if $ref.documents}
    {#each $ref.documents as refDocument}
      <option value={refDocument.uid}>{`${refDocument.count} - ${refDocument.titre}`}</option>
    {/each}
  {/if}
</select>

<h3>Filtrer par député (multiselection)</h3>
<!-- svelte-ignore a11y-no-onchange -->
<select bind:value={acteurIds} multiple>
  {#if $ref.acteurs}
    {#each $ref.acteurs as refActeurs}
      <option value={refActeurs.uid}>{`${refActeurs.prenom} ${refActeurs.nom} (${refActeurs.groupe})`}</option>
    {/each}
  {/if}
</select>

<button on:click={loadGraph}>Charger</button>
{#if working}
  <Spinner/>
{/if}
<div>
  <svg id="svg-sankey"/>
</div>
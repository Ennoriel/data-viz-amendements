<script>
	import { onMount } from 'svelte';
	import { select, scaleLinear, max, scaleBand, range, axisBottom, axisLeft } from 'd3';
  import { send } from '../query.util'

  const width = 500;
  const height = 500;
  const padding = 25;
  const paddingLeft = 75;

	onMount(async () => {
    let data = await send('http://localhost:3456/api/agg')

    const x = scaleLinear()
			.domain([0, max(data.map(d => d.count))])
			.range([0, width])

		const y = scaleBand()
      .domain(data.map(d => d._id))
			.range([0, height])

    const svg = select("div")
      .append('svg')
			.attr("width", width + padding + paddingLeft)
      .attr("height", y.range()[1] + 2 * padding)
      .attr("font-family", "sans-serif")
      .attr("font-size", "14")
      .attr("text-anchor", "end")
			.append('g')
    	.attr("transform", "translate(" + paddingLeft + "," + padding + ")");

    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(axisBottom(x).ticks(6));

    svg.selectAll('rect').data(data)
      .join("rect")
      .attr("fill", "steelblue")
      .attr("width", d => x(d.count))
      .attr("y", d => y(d._id))
      .attr("height", y.bandwidth() - 1);

    svg.append("g")
      .call(axisLeft(y).tickSize(0))
      .selectAll("text")	
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", ".15em")
  })
</script>

<div class="test"></div>
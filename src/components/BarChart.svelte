<script>
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	const data = [3, 6, 8, 5, 9];
	const width = 200

	onMount(() => {
		const x = d3.scaleLinear()
			.domain([0, d3.max(data)])
			.range([0, width])

		const y = d3.scaleBand()
			.domain(d3.range(data.length))
			.range([0, 20 * data.length])

		const svg = d3.selectAll("svg")
			.attr("width", width)
      .attr("height", y.range()[1])
      .attr("font-family", "sans-serif")
      .attr("font-size", "10")
      .attr("text-anchor", "end");

			const bar = svg.selectAll('g')
				.data(data)
				.join("g")
					.attr("transform", (d, i) => `translate(0,${y(i)})`);

			bar.append("rect")
				.attr("fill", "steelblue")
				.attr("width", x)
				.attr("height", y.bandwidth() - 1);

			bar.append("text")
				.attr("fill", "white")
				.attr("x", d => x(d) - 3)
				.attr("y", (y.bandwidth() - 1) / 2)
				.attr("dy", "0.35em")
				.text(d => d);
	});
</script>

<svg></svg>
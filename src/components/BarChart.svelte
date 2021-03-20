<script>
	import { onMount } from 'svelte';
	import { scaleLinear, max, scaleBand, range, select, axisBottom} from 'd3';
	const data = [3, 6, 8, 5, 9];
	const width = 200
	const height = 200
	const padding = 30

	onMount(() => {
		const x = scaleLinear()
			.domain([0, max(data)])
			.range([0, width])

		const y = scaleBand()
			.domain(range(data.length))
			.range([0, height])

		const svg = select("svg")
			.attr("width", width + 2 * padding)
      .attr("height", y.range()[1] + 2 * padding)
      .attr("font-family", "sans-serif")
      .attr("font-size", "14")
      .attr("text-anchor", "end")
			.append('g')
			
    	.attr("transform", "translate(" + padding + "," + padding + ")");

			const bar = svg.selectAll('g')
				.data(data)
				.join("g")
					.attr("transform", (d, i) => `translate(0,${y(i)})`);

			svg.append("g")
				.attr("transform", "translate(0," + height + ")")
        .call(axisBottom(x).ticks(6));

			bar.append("rect")
				.attr("fill", "steelblue")
				.attr("width", x)
				.attr("height", y.bandwidth() - 1);

				bar.append("text")
				.attr("fill", "white")
				.attr("x", d => x(d) - 5)
				.attr("y", (y.bandwidth() - 1) / 2)
				.attr("dy", "0.35em")
				.attr("cursor", "default")
				.text(d => d);
	});
</script>

<svg></svg>
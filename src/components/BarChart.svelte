<script>
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	var data = [3, 6, 8, 5, 9];

	onMount(() => {
		 const div = d3.selectAll("div")
      .style("font", "10px sans-serif")
      .style("text-align", "right")
      .style("color", "white");

		div.selectAll("div")
			.data(data)
			.join("div")
				.style("background", "steelblue")
				.style("padding", "3px")
				.style("margin", "1px")
				.style("width", d => `${d * 10}px`)
				.text(d => d);
	});
</script>

<div></div>
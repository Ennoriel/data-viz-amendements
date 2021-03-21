<script>
	import Select from './components/Select.svelte'
	import BarChart from './components/BarChart.svelte'
	import Histogram from './components/Histogram.svelte';
	import HistogramStacked from './components/HistogramStacked.svelte';
	import Test from './components/Test.svelte';
	import HeatMap from './components/HeatMap.svelte'

	let documentId

	function onDocumentChange(value) {
		documentId = value
	}
</script>

<Select {onDocumentChange}/>

<!-- <Test/> -->
<!-- <BarChart/> -->
<!-- <Histogram/> -->
<HistogramStacked {documentId}/>
<HeatMap {documentId}/>
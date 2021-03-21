<script>
	import Select from './components/Select.svelte'
	import HistogramStacked from './components/HistogramStacked.svelte';
	import HeatMap from './components/HeatMap.svelte'

	let documentId

	function onDocumentChange(value) {
		documentId = value
	}
</script>

<h1>Graphiques relatifs aux amendements déposés sous la XVème législature</h1>
<p>
	Les données sont issues des <a href="https://data.assemblee-nationale.fr" target="_blank">Open data de l'Assemblée Nationale</a>.
	Le code source est disponible sur ce <a href="{process.env.GITHUB_REPO}" target="_blank">repository Github</a>.
</p>
<p>
	La base de données est composée de 500 000 amendements et 6500 projets/propositions de loi au 18 mars 2021.
</p>
<Select {onDocumentChange}/>

<HistogramStacked {documentId}/>
<HeatMap {documentId}/>
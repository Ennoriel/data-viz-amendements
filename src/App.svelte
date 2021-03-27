<script>
	import { onMount } from 'svelte';
  import { send } from './query.util'
	
	import Divider from './components/Divider.svelte'
	import DeputeeSortHS from './components/StackedHistogram/DeputeeSortHS.svelte'
	import GroupeNewSortHS from './components/StackedHistogram/GroupeNewSortHS.svelte'
	import Select from './components/Select.svelte'
	import HeatMap from './components/HeatMap.svelte'
	import SankeyDiagram from './components/SankeyDiagram.svelte'
	import LinearChart from './components/LinearChart.svelte'

	let ref = {}

	let documentId
	let acteurId

	onMount(loadDocuments)

	async function loadDocuments() {
		send('/api/documents').then(res => ref.documents = res)
		send('/api/acteurs').then(res => ref.acteurs = res)
	}
</script>

<style>
	header {
		padding: 10px;
	}
</style>

<header>
	<h1>Graphiques relatifs aux amendements déposés sous la XVème législature</h1>
	<p>
		Les données sont issues des <a href="https://data.assemblee-nationale.fr" target="_blank">Open data de l'Assemblée Nationale</a>.
		Le code source est disponible sur ce <a href="{process.env.GITHUB_REPO}" target="_blank">repository Github</a>.
	</p>
	<p>
		La base de données est composée de 500 000 amendements et 6500 projets/propositions de loi au 18 mars 2021.
	</p>
</header>

<Divider/>
<Select {ref} bind:documentId bind:acteurId/>
<Divider/>
<HeatMap {documentId} {acteurId}/>
<Divider/>
<DeputeeSortHS {documentId} />
<Divider/>
<GroupeNewSortHS {documentId} />
<Divider/>
<SankeyDiagram {ref}/>
<Divider/>
<LinearChart/>
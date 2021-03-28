<script>
	import { onMount } from 'svelte';
  import { send } from './query.util'
	
	import Nav from './components/Nav.svelte'
	import Home from './components/Home.svelte'
	import DeputeeSortHS from './components/StackedHistogram/DeputeeSortHS.svelte'
	import GroupeNewSortHS from './components/StackedHistogram/GroupeNewSortHS.svelte'
	import HeatMap from './components/HeatMap.svelte'
	import SankeyDiagram from './components/SankeyDiagram.svelte'
	import LinearChart from './components/LinearChart.svelte'

	let selectedRoute

	let ref = {}

	onMount(loadData)

	async function loadData() {
		send('/api/documents').then(res => ref.documents = res)
		send('/api/acteurs').then(res => ref.acteurs = res)
	}

	const routes = [
		{
			menu: 'Accueil',
			title: "Accueil",
			component: Home
		},
		{
			menu: 'par Jour',
			title: "Nombre d'amendements par jour",
			component: HeatMap
		},
		{
			menu: 'par député',
			title: "Nombre d'amendements par député",
			component: DeputeeSortHS
		},
		{
			menu: 'par député 2',
			title: "Nombre d'amendements par député",
			component: SankeyDiagram
		},
		{
			menu: 'par groupe',
			title: "Nombre d'amendements par groupe",
			component: GroupeNewSortHS
		},
		{
			menu: 'dans le temps',
			title: "Nombre d'amendements dans le temps",
			component: LinearChart
		}
	]
</script>

<style>
	:global(html) {
		--nav-height: 60px;
		--color-main: rgb(255,62,0);
	}
	main {
		height: calc(100vh - var(--nav-height));
		box-sizing: border-box;
		
		overflow-y: auto;

		padding: 1em;
		display: flex;
		flex-direction: column;
		align-items: center;
	}
</style>

<Nav {routes} bind:selectedRoute/>

<main>
	{#if selectedRoute}
		<svelte:component this={selectedRoute.component} {ref} />
	{/if}
</main>
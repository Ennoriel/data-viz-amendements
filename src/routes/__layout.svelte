<script>
	import { onMount } from 'svelte';
	import Nav from '$lib/Nav.svelte'

	import { ref } from '$lib/stores/ref.js';
  import { send } from '$lib/query.util'

	import '../app.css';
	
	onMount(() => {
		loadData()
	})

	async function loadData() {
		Promise.all([
			send(fetch, '/api/ref/documents'),
			send(fetch, '/api/ref/acteurs')
		]).then(res => {
			$ref = {
				documents: res[0],
				acteurs: res[1]
			}
		})
	}
</script>

<Nav />
<main>
	<slot />
</main>

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
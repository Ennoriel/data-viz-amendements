<script>
  import Select from '$lib/Select.svelte'
  import Spinner from '$lib/Spinner.svelte'
  import HistogramStacked from '$lib/HistogramStacked.svelte';
  import { send } from '$lib/query.util'

  export let ref

  let working = false
  let documentId
  let data

  $: {
    working = true
    send(fetch, '/api/graph/stackedbar/group', { documentId }).then(res => {
      data = res
      working = false
    })
  }
</script>

<Select {ref} bind:documentId isActeur={false} />
{#if working}
  <Spinner/>
{:else}
  <HistogramStacked {data} getXVal={v => v.groupe}/>
{/if}
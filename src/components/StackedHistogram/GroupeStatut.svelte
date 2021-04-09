<script>
  import Select from './../Select.svelte'
  import Spinner from './../Spinner.svelte'
  import HistogramStacked from './HistogramStacked.svelte';
  import { send } from '../../query.util'

  export let ref

  let working = false
  let documentId
  let data

  $: {
    working = true
    send('/api/projectGroupStatut', { documentId }).then(res => {
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
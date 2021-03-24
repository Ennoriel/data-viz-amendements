<script>
  import HistogramStacked from './HistogramStacked.svelte';
  import { send } from '../../query.util'

  export let documentId
  let data

  $: {
    send('/api/projectAuteurSort', { documentId }).then(res => {
      data = res
    })
  }
</script>

<HistogramStacked {data} getXVal={v => v.auteur} title="Nombre d'amendements par député"/>
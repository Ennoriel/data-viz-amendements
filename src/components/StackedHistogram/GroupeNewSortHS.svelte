<script>
  import HistogramStacked from './HistogramStacked.svelte';
  import { send } from '../../query.util'

  export let documentId
  let data

  $: {
    send('/api/projectGroupNewSort', { documentId }).then(res => {
      data = res
      // console.log(data)
    })
  }
</script>

<HistogramStacked {data} getXVal={v => v.groupe} title="Nombre d'amendements par groupe politique"/>
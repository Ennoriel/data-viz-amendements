<script>
	import { onMount } from 'svelte';
  import { send } from '../query.util'

  export let onDocumentChange
  let ref = {}
  let documentId

  onMount(loadDocuments)

  async function loadDocuments() {
    ref.documents = await send('http://localhost:3456/api/documents')
  }
</script>

<style>
  select {
    width: 100%;
  }
</style>

<h1>Filtrer par projet de loi</h1>
<!-- svelte-ignore a11y-no-onchange -->
<select
  bind:value={documentId}
  on:change={() => onDocumentChange(documentId)}
>
  <option value={''} />
  {#if ref.documents}
    {#each ref.documents as refDocument}
      <option value={refDocument.uid}>{`${refDocument.count} - ${refDocument.titre}`}</option>
    {/each}
  {/if}
</select>
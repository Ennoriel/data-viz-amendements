<script>
	import { onMount } from 'svelte';
  import { send } from '../query.util'

  export let documentId
  export let acteurId

  let ref = {}

  onMount(loadDocuments)

  async function loadDocuments() {
    ref.documents = await send('/api/documents')
    ref.acteurs = await send('/api/acteurs')
  }
</script>

<style>
  select {
    width: 100%;
  }
</style>

<h2>Filtrer par projet de loi</h2>
<!-- svelte-ignore a11y-no-onchange -->
<select bind:value={documentId}>
  <option value={''} />
  {#if ref.documents}
    {#each ref.documents as refDocument}
      <option value={refDocument.uid}>{`${refDocument.count} - ${refDocument.titre}`}</option>
    {/each}
  {/if}
</select>

<h2>Filtrer par député (uniquement le deuxième grpahique)</h2>
<!-- svelte-ignore a11y-no-onchange -->
<select bind:value={acteurId}>
  <option value={''} />
  {#if ref.acteurs}
    {#each ref.acteurs as refActeurs}
      <option value={refActeurs.uid}>{`${refActeurs.prenom} ${refActeurs.nom} (${refActeurs.groupe})`}</option>
    {/each}
  {/if}
</select>
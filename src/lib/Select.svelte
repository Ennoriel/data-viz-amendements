<script>
	import { ref } from '$lib/stores/ref.js';
  export let isDocument = true
  export let isActeur = true

  export let documentId
  export let acteurId
</script>

{#if isDocument}
  <h3>Filtrer par projet de loi</h3>
  <!-- svelte-ignore a11y-no-onchange -->
  <select bind:value={documentId}>
    <option value={undefined} />
    {#if $ref.documents}
      {#each $ref.documents as refDocument}
        <option value={refDocument.uid}>{`${refDocument.count} - ${refDocument.titre.substring(0, 130)}${refDocument.titre.length > 130 ? '...' : ''}`}</option>
      {/each}
    {/if}
  </select>
{/if}

{#if isActeur}
  <h3>Filtrer par député</h3>
  <!-- svelte-ignore a11y-no-onchange -->
  <select bind:value={acteurId}>
    <option value={undefined} />
    {#if $ref.acteurs}
      {#each $ref.acteurs as refActeurs}
        <option value={refActeurs.uid}>{`${refActeurs.prenom} ${refActeurs.nom} (${refActeurs.groupe})`}</option>
      {/each}
    {/if}
  </select>
{/if}
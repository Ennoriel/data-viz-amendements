import { writable } from 'svelte/store';

export const ref = writable({
  documents: [],
  acteurs: []
});
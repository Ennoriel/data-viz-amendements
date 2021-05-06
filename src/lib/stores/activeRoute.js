import { writable } from 'svelte/store';

export const activeRoute = writable({
  menu: 'Accueil',
  title: "Accueil",
  src: '/'
});
<script context="module">
	export const prerender = true;
</script>

<script>
	import POSTS from '$lib/posts.js'
	import { activeRoute } from '$lib/stores/activeRoute.js';
</script>

<style>
  h2 {
    font-size: 1.8em;
    text-align: center;
  }
	ul {
		margin: 0 0 1em 0;
		line-height: 1.5;
    list-style-type: '-   '
	}
  a {
    text-decoration: none;
    text-decoration: none;
    cursor: pointer;
  }
</style>

<h2>Liste des articles</h2>
<ul>
  {#each POSTS as post}
    <li>
      <a
        href="blog/{post.href}"
        on:click={() => $activeRoute = post}
      >
        {post.title}
      </a>
    </li>
  {/each}
</ul>

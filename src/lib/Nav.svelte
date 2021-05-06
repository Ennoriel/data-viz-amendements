<script context="module">

	export async function load() {
		console.log("nav module load")
	}

</script>

<script>
	import { browser } from '$app/env';
	import { activeRoute } from '$lib/stores/activeRoute.js';
	import ROUTES from '$lib/routes.js'
	import POSTS from '$lib/posts.js'
	import { page } from '$app/stores';

	// only executed on first nav rendering (app load)
	if (browser) {
		if (!$page.path.includes('/blog/')) {
			$activeRoute = ROUTES.find(route => route.href === $page.path)
		} else {
			$activeRoute = POSTS.find(post => $page.path.endsWith(post.href))
		}
	}
</script>

<style>
	nav {
		border-bottom: 1px solid rgba(255,62,0,0.1);
		font-weight: 300;
		height: var(--nav-height);
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		
		box-sizing: border-box;
	}

	h1 {
		font-size: 1.5em;
		margin: -2px 0 0 1em;
		height: var(--nav-height);
		line-height: var(--nav-height);
	}

	ul {
		margin: 0 1em 0 0;
		padding: 0;
	}

	li {
		height: 100%;
		display: inline-block;
	}

	[aria-current] {
		position: relative;
		display: inline-block;
	}

	[aria-current]::after {
		position: absolute;
		content: '';
		width: calc(100% - 1em);
		height: 4px;
		background-color: var(--color-main);
		display: block;
		bottom: -2px;
		left: 0.5em;
	}

	a {
		color: #333;
		text-decoration: none;
		height: 100%;
		line-height: var(--nav-height);
		text-decoration: none;
		padding: 0 .75em;
		display: block;
		
		transition: color 0.2s;
	}
		
	a:not([aria-current]):hover {
		color: var(--color-main);
	}

	@media (max-width: 1050px) {
		ul {
			width: 10em;
			max-height: calc(var(--nav-height) - 1px);
			overflow-y: hidden;
			background-color: white;
			z-index: 1;
		}
		ul:hover {
			max-height: calc(7 * var(--nav-height) + 3px)
		}
		ul:not(:hover):before {
			content: "Accueil ⯆";
			display: block;
			height: var(--nav-height);
			line-height: var(--nav-height);
			text-align: right;
			margin-right: 1em;
		}
		ul:not(:hover) li:first-of-type a:after {
			content: '⯈';
			margin-left: 1em;
			display: inline-block;
			transform: rotate(90deg);
		}
		li {
			display: block;
		}
		a:hover {
			color: var(--color-main);
			margin-left: 0.5em;
		}
		a:hover:before {
			content: '⯈';
			margin-right: 0.5em;
		}
		ul:hover li {
			border-bottom: 1px solid var(--color-main);
		}
		[aria-current]::after {
			opacity: 0;
		}
	}

	@media (max-width: 600px) {
		h1 {
			font-size: 1em;
			margin: 0 0 0 1em;
		}
	}

	@media (max-width: 450px) {
		h1 {
			overflow: hidden;
		}
	}
</style>

<nav>
	{#if $activeRoute}
		<h1>{$activeRoute.title}</h1>
	{/if}

	<ul>
		{#each ROUTES as route}
			<li>
				<a
					href={route.href}
					aria-current={route.menu === $activeRoute.menu ? 'page' : undefined}
					on:click={() => $activeRoute = route}
				>
					{route.menu}
				</a>
			</li>
		{/each}
	</ul>
</nav>

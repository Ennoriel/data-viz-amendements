<script>
	export let routes;
	export let selectedRoute = routes[0];
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

	span {
		height: 100%;
		line-height: var(--nav-height);
		text-decoration: none;
		padding: 0 .75em;
		display: block;
		
		transition: color 0.2s;
	}
		
	span:not([aria-current]):hover {
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
			max-height: calc(6 * var(--nav-height) + 3px)
		}
		ul:not(:hover):before {
			content: "Accueil ⯆";
			display: block;
			height: var(--nav-height);
			line-height: var(--nav-height);
			text-align: right;
			margin-right: 1em;
		}
		ul:not(:hover) li:first-of-type span:after {
			content: '⯈';
			margin-left: 1em;
			display: inline-block;
			transform: rotate(90deg);
		}
		li {
			display: block;
		}
		span:hover {
			color: var(--color-main);
			margin-left: 0.5em;
		}
		span:hover:before {
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
	<h1>{selectedRoute.title}</h1>
	<ul>
		{#each routes as route}
			<li>
				<span
					aria-current="{route.menu === selectedRoute.menu ? 'page' : undefined}"
					on:click={() => selectedRoute = route}
				>
					{route.menu}
				</span>
			</li>
		{/each}
	</ul>
</nav>

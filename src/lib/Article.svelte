<style>
  :global(article) {
    width: 100%;
    margin-right: auto;
    margin-left: auto;
    text-align: justify;
  }
  @media (min-width: 700px) {
    :global(article) {
      width: calc(52% + 336px);
      max-width: 960px;
    }
  }

  :global(h2), :global(#subtitle), :global(h3), :global(h4) {
    font-weight: bolder;
  }
  :global(header) {
    width: 100%;
    display: flex;
    flex-direction: column;
  }
  :global(h2) {
    font-size: 1.8em;
    text-align: center;
  }
  :global(#subtitle) {
    font-size: 1.2em;
    color: #666;
    margin-top: 0;
    text-align: center;
    font-style: italic;
  }
  :global(h3) {
    font-size: 1.5em;
    margin-top: 2em;
  }
  :global(h4) {
    font-size: 1.2em;
  }
  :global(h3), :global(h4) {
    width: 100%;
    text-align: center;
  }
  @media (min-width: 700px) {
    :global(h3), :global(h4) {
      text-align: left;
    }
    :global(h3) {
      margin-left: 2em;
    }
    :global(h4) {
      margin-left: 4em;
    }
  }
  :global(ul) {
    list-style-type: '-   '
  }
  :global(table) {
    margin: 3em auto;
    width: 100%;
    border-collapse: collapse;
  }
  :global(table), :global(td), :global(th) {
    border: 1px solid black;
    text-align: center;
  }
  :global(td), :global(th) {
    padding: .5em;
  }
  :global(th) {
    font-weight: 700;
  }
  :global(.table-fixed) {
    width: 80%;
    table-layout: fixed;
  }
  :global(img) {
    display: block;
    max-width: 65%;
    margin: 3em auto;
  }
  :global(a:visited) {
    text-decoration: none;
  }
  :global(a) {
    color: var(--color-main)
  }

  nav {
    padding: 1em 0 3em;
  }
  a {
    background-color: var(--color-main);
    text-decoration: none;
    cursor: pointer;
    padding: 0.5em 2em;
    border-radius: 0.3em;
    color: white;
  }
</style>

<slot/>
<nav>
  <a href="/blog">Retour à la liste des articles</a>
</nav>
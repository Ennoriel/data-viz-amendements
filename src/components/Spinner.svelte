<style>
  #loading {
    flex-shrink: 0;
    display: inline-block;
    width: 50px;
    height: 50px;
    border: 3px solid #ddd;
    border-radius: 50%;
    border-top-color: var(--color-main);
    animation: spin 1s ease-in-out infinite;
    -webkit-animation: spin 1s ease-in-out infinite;
  }

  @keyframes spin {
    to { -webkit-transform: rotate(360deg); }
  }
  @-webkit-keyframes spin {
    to { -webkit-transform: rotate(360deg); }
  }
</style>

<p>Récupération des données...</p>
<div id="loading"></div>
<style>
  a {
      color: rgb(0, 100, 200);
      text-decoration: none;
  }

  a:hover {
      text-decoration: underline;
  }

  strong {
    font-weight: bolder;
    font-size: 1.2em;
  }
</style>

<h2>Graphiques relatifs aux amendements déposés sous la XVème législature</h2>
<p>
  Les données sont issues des <a href="https://data.assemblee-nationale.fr" target="_blank">Open data de l'Assemblée Nationale</a>.
  Le code source est disponible sur ce <a href="{process.env.GITHUB_REPO}" target="_blank">repository Github</a>.
</p>
<p>
  La base de données est composée de 500 000 amendements et 6500 projets/propositions de loi au 18 mars 2021.
</p>
<p>
  La récupération des données n'a pas encore été optimisé sur tous les graphiques. Le chargement peut prendre plusieurs secondes.
</p>
<p>
  <strong>
    Attention, les données importées ne sont pas correctes. En particulier :
  </strong>
</p>
<ul>
  <li><strong>Les amendements sont en double, il faut donc diviser les chiffres par deux (exceptés les pourcentages)</strong></li>
  <li><strong>Les sorts correspondant à un état non clos ne sont pas toujours corrects (du fait de l'export de l'AN...)</strong></li>
</ul>
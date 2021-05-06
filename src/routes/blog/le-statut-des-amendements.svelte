<script context="module">
	export const prerender = true;
</script>

<script>
  import Article from '$lib/Article.svelte'
</script>

<Article>
  <article>
    <header>
      <h2>Le statut des amendements</h2>
      <p id="subtitle">Reverse engineering du système d'informations de l'Etat</p>
    </header>

    <h3>1. Introduction</h3> 

    <h4>a. Qu’est-ce qu’un amendement ?</h4>

    <p>Un amendement est une modification d’un projet ou d’une proposition de loi au sein d’une assemblée délibérante telle que l’Assemblée nationale (voir <a target="blank_" href="https://www.vie-publique.fr/questions-reponses/273399-huit-questions-sur-le-droit-damendement">ici</a> pour plus de détail).</p>
    <p>Les amendements suivent un processus entre le moment de leur dépôt et de leur décision finale. Quel est ce processus ? Il n'est pas défini dans un document unique mais réparti entre plusieurs textes (Constitution, lois, règlement de l’AN).</p>

    <h4>b. Traitement des amendements dans un système d’information</h4>

    <p>Toutefois, il est possible de retracer le processus de traitement des amendements à partir du système de traitement automatisé de l’information mis en place par l’Assemblée nationale.</p>
    <p>L’ensemble des règles mises en place dans le cadre du système d’information (SI) de la chambre basse s’appuie sur plusieurs états, sous-états et sort permettant de reconstituer le trajet d’un amendement (voir <a target="blank_" href="https://www2.assemblee-nationale.fr/decouvrir-l-assemblee/role-et-pouvoirs-de-l-assemblee-nationale/l-administration-de-l-assemblee-nationale/l-informatique-a-l-assemblee-nationale">ici</a> pour plus de détails).</p>
    <p>L’extraction de ces informations pour reconstituer le processus de traitement se base sur la pratique du Reverse Engineering (rétro-ingénierie). Cette pratique vise, à partir d’un résultat final, à reconstituer l’ensemble des étapes ayant conduit à ce résultat (voir <a target="blank_" href="https://fr.wikipedia.org/wiki/R%C3%A9tro-ing%C3%A9nierie#D%C3%A9finition_formelle">ici</a> pour plus de détails).</p>
     
    <h3>2. Rétro-ingénierie du processus d’adoption d’un amendement</h3>

    <h4>a. Extraction des informations</h4>

    <p>Il existe plusieurs moyen de récupérer le contenu d'un amendement :</p>
    <ul>
      <li>En recherchant via le <a target="blank_" href="https://www.assemblee-nationale.fr/dyn/15/amendements">site public de l'AN</a></li>
      <li>En temps réel des discussion via le site <a target="blank_" href="https://eliasse.assemblee-nationale.fr/eliasse/index.html">Eliasse</a></li>
      <li>Via les données ouvertes :
        <ul>
          <li>sur chaque détail d'amendement, il est possible de télécharger une version au format json (<a target="blank_" href="https://www.assemblee-nationale.fr/dyn/opendata/AMANR5L15PO717460BTC1094P0D1N000023.json">exemple</a>)</li>
          <li>sur le site des données ouvertes, il est possible de télécharger l'ensemble des amendements d'une législature (<a target="blank_" href="https://data.assemblee-nationale.fr/">site</a>)</li>
        </ul>
      </li>
    </ul>

    <h4>b. Critères de classification : sort, état et sous état</h4>

    <p>En parcourant plusieurs fichiers json, il est possible de se rendre compte qu’un amendement ne dispose pas d'un statut unique définissant l'emplacement dans le processus de traitement mais un triptyque définissant son statut.</p>

    <p>Ces éléments sont :</p>
    <ul>
      <li>le sort qui constitue le stade final de l’amendement, </li>
      <li>l'état qui constitue son placement dans le processus de traitement</li>
      <li>le sous-état qui vient préciser l’état</li>
    </ul>

    <p>Lorsque que l’on s’intéresse aux éléments constituant le statut de l’amendement, il apparaît que ceux-ci rassemblent plusieurs valeurs.</p>

    <h4>c. Constitution des éléments : définition des valeurs</h4>

    <p>En extrayant les 250 000 amendements de la XVe législature au 18 mars 2021, on observe les valeurs suivantes pour chaque élément de statut :</p>

    <table class="table-fixed">
      <thead>
        <tr>
          <th>Sort - 5 valeurs</th>
          <th>Etat - 6 valeurs</th>
          <th>Sous-état - 29 valeurs</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            Adopté<br/>
            Non soutenu<br/>
            Rejeté<br/>
            Retiré<br/>
            Tombé<br/>
            (+ 1 valeur nulle)
          </td>
          <td>
            En traitement<br/>
            En recevabilité<br/>
            Irrecevable<br/>
            Irrecevable 40<br/>
            A discuter<br/>
            Discuté<br/>
            Retiré<br/>
          </td>
          <td>
            dont 21 valeurs relatives aux états Irrecevable et Irrecevable 40<br/>
            (+ 1 valeur nulle)
          </td>
        </tr>
      </tbody>
    </table>

    <p>Si l'on assemble le sort, l'état et le sous état, il existe 16 duos sort-état et 41 triptyques.</p>
    <p>Pour réaliser le processus de traitement des statuts, on peut se baser sur les duos sort-état qui semblent représenter le statut général de l’amendement, le sous-état apportant un détail à ce dernier.</p>

    <h4>d. Les duos "bâtards"</h4>

    <p>En additionnant le nombre d’amendement sur le duo sort-état, on se rend compte que 5 des 16 duos sont en très faible nombre et représentent des statuts de premier abord incohérent :</p>

    <table class="table-fixed">
      <thead>
        <tr>
          <th colspan="3">Tryptiques « bâtards »</th>
        </tr>
        <tr>
          <th>Sort</th>
          <th>Etat</th>
          <th>Nombre</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Non soutenu</td>
          <td>Irrecevable</td>
          <td>35</td>
        </tr>
        <tr>
          <td>Rejeté</td>
          <td>A discuter</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Rejeté</td>
          <td>Irrecevable</td>
          <td>7</td>
        </tr>
        <tr>
          <td>Retiré</td>
          <td>Irrecevable</td>
          <td>10</td>
        </tr>
        <tr>
          <td>Tombé</td>
          <td>Irrecevable</td>
          <td>2</td>
        </tr>
      </tbody>
    </table>

    <p>On peut supposer que ces valeurs sont des anomalies dues à des modifications simultanées de deux personnes au sein du système d’information. Ces données ont été écartées dans la reconstitution finale du processus.</p>

    <h4>e. Proposition de modélisation</h4>

    <p>Le schéma ci-dessous représente le processus de traitement supposé d’un amendement :</p>

    <img src="/WF_amendement_status.PNG" alt="Schéma représentant le workflow des statuts (sort et état) d'un amendement"/>

    <p>Pour réaliser ce schéma, nous avons agrégé le nombre d’amendements par duo sort-état et avons supposé, sur les principes logiques les possibles changements d’état. Certains changements sont peut-être possibles en plus de ce qui est représenté aussi bien que certains changements ne sont peut-être pas possibles alors que représenté.</p>
    <p>Le duo “Aucun” “En irrecevabilité” est en très faible nombre, celui-ci semble être un état transitoire minoritaire utilisé pour les amendements dont les services de l’Assemblée nationale ont un doute sur la recevabilité de l’amendement.</p>
    <p>Pour vérifier le processus de manière plus fiable, il serait nécessaire de scruter en temps réel le triptyque au fil du temps pour chaque amendement. Bien que cela soit théoriquement possible, cela nécessiterait d'interroger à une fréquence élevée et pour un grand nombre d’amendements le site de l’assemblée nationale ce qui n’est pas forcément l’enjeu.</p>
    <p>Si nous devions résumer les états des amendements, nous pourrions donc en extraire 11 :</p>

    <table class="table table-bordered table-hover table-condensed">
      <thead>
        <tr>
          <th title="Field #1">Statut</th>
          <th title="Field #2">Sort</th>
          <th title="Field #3">Etat</th>
          <th title="Field #4">Description</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>En traitement</td>
          <td>Aucun</td>
          <td>En traitement</td>
          <td>l’amendement vient d’être déposé</td>
        </tr>
        <tr>
          <td>En irrecevabilité</td>
          <td>Aucun</td>
          <td>En irrecevabilité</td>
          <td>l’amendement a été positionné en état intermédiaire, en attente d’une décision sur sa recevabilité</td>
        </tr>
        <tr>
          <td>A discuter</td>
          <td>Aucun</td>
          <td>A discuter</td>
          <td>l’amendement a été jugé recevable par les services de l’AN. Il est en attente d’être discuté en commission</td>
        </tr>
        <tr>
          <td>Irrecevable</td>
          <td>Aucun</td>
          <td>Irrecevable</td>
          <td>l’amendement est irrecevable (68% cavalier législatif, 24% doublon, entonnoir ou sous-amendement, etc.)</td>
        </tr>
        <tr>
          <td>Irrecevable 40</td>
          <td>Aucun</td>
          <td>Irrecevable 40</td>
          <td>l’amendement est irrecevable aux yeux de l’article 40 de la constitution (charge financière)</td>
        </tr>
        <tr>
          <td>Retiré avant discussion</td>
          <td>Aucun</td>
          <td>Retiré</td>
          <td>l’amendement a été retiré par le député avant d’avoir été soutenu et voté</td>
        </tr>
        <tr>
          <td>Adopté</td>
          <td>Adopté</td>
          <td>Discuté</td>
          <td>l’amendement a été soutenu, voté et adopté</td>
        </tr>
        <tr>
          <td>Non soutenu</td>
          <td>Non soutenu</td>
          <td>Discuté</td>
          <td>l’amendement a été présenté à l’Assemblée mais n’a pas été soutenu</td>
        </tr>
        <tr>
          <td>Rejeté</td>
          <td>Rejeté</td>
          <td>Discuté</td>
          <td>l’amendement a été soutenu, voté et rejeté</td>
        </tr>
        <tr>
          <td>Tombé</td>
          <td>Tombé</td>
          <td>Discuté</td>
          <td>l’amendement est rendu nul par l’adoption d’un autre amendement</td>
        </tr>
        <tr>
          <td>Retiré après discussion</td>
          <td>Retiré</td>
          <td>Discuté</td>
          <td>l’amendement a été soutenu mais retiré avant le vote</td>
        </tr>
      </tbody>
    </table>

    <p>Pour la praticité d’usage, nous regrouperons certains statuts ensemble pour l’exploitabilité des données :</p>

    <ul>
      <li>En traitement, En irrecevabilité, A discuté</li>
      <li>Retiré avant discussion, retiré après discussion, non soutenu, rejeté, tombé</li>
      <li>Adopté</li>
      <li>Irrecevable</li>
      <li>Irrecevable 40</li>
    </ul>
  </article>
</Article>
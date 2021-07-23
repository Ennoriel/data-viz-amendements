from os import environ
from utils import download_file, get_node_text
from lxml import html
from re import search, compile
from functools import reduce
from lxml.etree import tostring
from pymongo import MongoClient


# titles of the law
LAW_TITLES = {
	"assnat1TomeNum"          : "tome_no",
	"assnat2PartieNum"        : "partie_no",
	"assnat3LivreNum0"        : "livre_no",
	"assnat4TitreNum"         : "titre_no",
	"assnat5ChapitreNum0"     : "chapitre_no",
	"assnat6SectionNum"       : "section_no",
	"assnat7Sous-sectionNum0" : "sous-section_no",
	"assnat8ParagrapheNum0"   : "paragprahe_no",

	"assnat1TomeIntit": "tome",
	"assnat2PartieIntit": "partie",
	"assnat3LivreIntit": "livre",
	"assnat4TitreIntit": "titre",
	"assnat5ChapitreIntit": "chapitre",
	"assnat6SectionIntit": "section",
	"sectionIntit": "sous-section",
	"assnat8ParagrapheIntit0": "paragprahe"
}


ALL_TITLE_CLASSES = [
	'assnat1TomeIntit0',
	'assnat1TomeNum0',
	'assnat2PartieIntit0',
	'assnat2PartieNum0',
	'assnat3LivreIntit0',
	'assnat3LivreNum',
	'assnat4TitreIntit0',
	'assnat4TitreNum0',
	'assnat5ChapitreIntit0',
	'assnat5ChapitreNum',
	'assnat6SectionIntit0',
	'assnat6SectionNum0',
	'assnat7Sous-sectionIntit0',
	'assnat7Sous-sectionNum',
	'assnat8ParagrapheIntit',
	'assnat8ParagrapheNum',

	'assnat1TomeIntit',
	'assnat1TomeNum',
	'assnat2PartieIntit',
	'assnat2PartieNum',
	'assnat3LivreIntit',
	'assnat3LivreNum0',
	'assnat4TitreIntit',
	'assnat4TitreNum',
	'assnat4titreintit1',
	'assnat5ChapitreIntit',
	'assnat5ChapitreNum0',
	'assnat6SectionIntit',
	'assnat6SectionNum',
	'assnat7Sous-sectionIntit',
	'assnat7Sous-sectionNum0',
	'assnat8ParagrapheIntit0',
	'assnat8ParagrapheNum0',
]


# section INSIDE an article of the law (ex: the article is adding a chapter to an existing book)
TITLES_IN_ARTICLES = {
	# "assnat1TomeIntit"          : "tome",
	"assnat1TomeIntit0"         : "tome",
	# "assnat1TomeNum"            : "tome_no",
	"assnat1TomeNum0"           : "tome_no",
	# "assnat2PartieIntit"        : "partie",
	"assnat2PartieIntit0"       : "partie",
	# "assnat2PartieNum"          : "partie_no",
	"assnat2PartieNumO"          : "partie_no",
	# "assnat3LivreIntit"         : "livre",
	"assnat3LivreIntit0"         : "livre",
	"assnat3LivreNum"           : "livre_no",
	# "assnat3LivreNum0"          : "livre_no",
	# "assnat4TitreIntit"         : "titre",
	"assnat4TitreIntit0"        : "titre",
	# "assnat4TitreNum"           : "titre_no",
	"assnat4TitreNum0"          : "titre_no",
	# "assnat5ChapitreIntit"      : "chapitre",
	"assnat5ChapitreIntit0"     : "chapitre",
	"assnat5ChapitreNum"        : "chapitre_no",
	# "assnat5ChapitreNum0"       : "chapitre_no",
	# "assnat6SectionIntit"       : "section",
	"assnat6SectionIntit0"      : "section",
	# "assnat6SectionNum"         : "section_no",
	"assnat6SectionNum0"        : "section_no",
	# "assnat7Sous-sectionIntit"  : "sous_section",
	"assnat7Sous-sectionIntit0" : "sous_section",
	"assnat7Sous-sectionNum"    : "sous_section_no",
	# "assnat7Sous-sectionNum0"   : "sous_section_no",
	"assnat8ParagrapheIntit"    : "paragraphe",
	# "assnat8ParagrapheIntit0"   : "paragraphe",
	"assnat8ParagrapheNum"      : "paragraphe_no",
	# "assnat8ParagrapheNum0"     : "paragraphe_no",
	"assnat9ArticleNum"         : "article",
	"assnat9ArticleNum0"        : "article",
}


mongo_db = environ['MONGO_DB']
mongo_url = environ['MONGO_URL']
client = MongoClient(mongo_url, retryWrites=False, w=1)[mongo_db]['y-textes']


def get_node_type(node, lvl=0):
	"""

	:param node:
	:param lvl:
	:return: one value in :
		- ('KO', "node is of wrong type")
		- ('KO', "node is not a <p> or <table> element")
		- ('KO', "node is empty")
		- ('KO', 'signature')
		- ('OK', 'alinea-table')
		- ('OK', 'article-no')
		- ('OK', 'alinea-text')
		- ('OK', 'structure-title')
        - ('OK', 'title-in-article')
	"""
	if type(node) is not html.HtmlElement:
		return 'KO', "node is of wrong type"
	if node.tag not in ['p', 'table']:
		return 'KO', "node is not a <p> or <table> element"
	if node.text_content().isspace() or compile(r'X').sub('', node.text_content()).isspace():
		return 'KO', "node is empty"
	if node.tag == 'table':
		# a table in a law article is considered as an alinea
		return 'OK', 'alinea-table'
	node_class = node.get('class')
	if node_class == 'assnatACorpsdetexte':
		return 'KO', 'signature'
	if node_class == 'assnat9ArticleNum':
		# an article no (ex: Article 1er, Article 2...) has a 'assnat9ArticleNum' class.
		# It is not considered as an alinea. Alineas starts at 1 after each article no
		# (if there is only one alinea, the alinea number is omitted)
		return 'OK', 'article-no'
	if node_class == 'assnatLoiTexte':
		# a paragraph is a law article has a 'assnatLoiTexte' class. It is considered as an alinea
		return 'OK', 'alinea-text'
	if node_class and node_class in ALL_TITLE_CLASSES:
		# The laws seem to use different classes if a title is the structure of the law or part of an article
		# but the norm is not very consistent, thus enforcing rules
		if node_class in LAW_TITLES and not node.xpath('.//img'):
			return 'OK', 'structure-title'
		elif node_class in TITLES_IN_ARTICLES and node.xpath('.//img'):
			return 'OK', 'title-in-article'
	print('Unknown node:')
	print(node_class)
	print(node.text_content())
	return 'KO', 'unknow node'


def count_by_element_type(acc, element):
	# if element.tag == "table":
	# 	print(element.text_content())
	if element.tag in acc:
		acc[element.tag] = acc[element.tag] + 1
	else:
		acc[element.tag] = 1
	return acc


def get_canonical_dom(text_id, html):
	"""
	Gets a list of first level dom elements part of the law project (titre, chapitre, articles)
	by removing unwanted parts (exposé des motifs, décret)
	(laws are usually made of few div containing lots of p elements)
	:param text_id:
	:param dom_elements:
	:return:
	"""

	if 'Projet de loi de finances' in html.text_content()[0:1000]:
		# Projet de loi finance (ex: PRJLANR5L15B2272)
		return None

	# law parts are in div with class assnatSection but not all of them are meaningful
	dom_elements = html.xpath("/html/body/div[starts-with(@class,'assnatSection')]")

	if dom_elements:
		dom_element = dom_elements[-1]
		if search(r'Annexe \w', dom_element.getchildren()[1].text_content()):
			# If there is one or more annexe (with title formatted as Annexe X), each one is in
			# a different div. Thus, more than one div should be aggregated to make the final draft
			# ex: PRJLANR5L15B2296, PRJLANR5L15B2416
			# Also, this should be in addition to an empty div (next case).
			# This part of the method should probably be recursive...
			children = []
			pass
		elif 'PRJ' in text_id and len(dom_element.text_content()) < 10:
			# if div content is less thant 10 char, going for previous block
			children = dom_elements[-2]
		elif 'PRJ' in text_id and 'RAPPORT ANNEXÉ' in dom_element.text_content():
			# if there is one "rapport annexé", taking both the previous div and this one
			children = dom_elements[-2].getchildren()
			children.extend(dom_elements[-1].getchildren())
		else:
			# otherwise, take all tags of the last div
			children = dom_element.getchildren()

		if not len(children):
			return None

		count_tags = reduce(count_by_element_type, children, {})
		# max_tag = (None, 0)
		# for count_tag in count_tags.items():
		# 	if count_tag[1] > max_tag[1]:
		# 		max_tag = count_tag
		max_tag = reduce(lambda acc, x: x if x[1] < acc[1] else acc, count_tags.items(), (None, 0))
		if max_tag[0] == 'div':
			# some law are made of div containg lots of div (not the same format) => PRJLANR5L15BTC3995
			return None

		# print(count_tags)
		count_class = reduce(lambda acc, x: (acc + 1) if x.get('class') else acc, children, 0)
		# print(count_class)
		if count_class < 0.1 * len(children):
			# less than 10% of tags have a class, considered unparsable (projet de loi finance / budget)
			return None
		text_content = dom_element.text_content()
		res = []
		if 'PION' in text_id:
			# print('EXPOSÉ DES MOTIFS') if 'EXPOSÉ DES MOTIFS' in text_content else print('...')
			# print('PROPOSITION DE LOI') if 'proposition de loi' in text_content else print('...')
			if 'EXPOSÉ DES MOTIFS' in text_content and 'PROPOSITION DE LOI' in text_content:
				# in some law text, there is a first section, not meaningful that needs to be removed
				for index in range(len(children)):
					if 'PROPOSITION DE LOI' in children[index].text_content():
						res = children[index + 1:]
						break
				else:
					# FIXME weird case
					res = []
			else:
				res = children
		elif 'PRJ' in text_id:
			if 'table' not in count_tags:
				# if there is a table, it might be for: a signed pre-text or a table inside the law
				# but if there isn't, all the tags can be taken
				res = children
			else:
				for index in range(len(children)):
					if 'Articleliminaire' in compile(r'\s+').sub('', children[index].text_content()):
						res = children[index:]
						break
					if 'Article unique' in children[index].text_content():
						res = children[index:]
						break
					if 'Article 1' in children[index].text_content():
						# if article 1 is found, going backwards to search for chapter and part titles
						for jndex in range(index, 0, -1):
							if children[jndex].get('class') and 'assnatLoiTexte' in children[jndex].get('class'):
								# print(jndex)
								res = children[jndex + 1:]
								break
						else:
							# if not found, we suspect that there is nothing before hence,
							# ever children are taken
							res = children
						break
		return res


def get_alinea_content(alinea, alinea_type, alinea_no):
	if alinea_type == 'alinea-table':
		return {
			"type": 'table',
			"alinea_no": alinea_no + 1,
			"content": tostring(alinea).decode('ascii')
		}
	elif alinea_type == 'article-no':
		return {
			"type": 'article_no',
			"content": alinea.text_content()
		}
	elif alinea_type == 'alinea-text':
		return {
			"type": 'alinea-text',
			"alinea_no": alinea_no + 1,
			"content": alinea.text_content()
		}
	elif alinea_type == 'structure-title':
		return {
			"type": 'structure-title',
			"title-type": LAW_TITLES[alinea.get('class')],
			"content": alinea.text_content()
		}
	elif alinea_type == 'title-in-article':
		return {
			"type": 'structure-title',
			"title-type": TITLES_IN_ARTICLES[alinea.get('class')],
			"alinea_no": alinea_no + 1,
			"content": alinea.text_content()
		}


def get_text(text_id):
	html_content = download_file(environ['AN_URL'] + "/dyn/opendata/{}.html".format(text_id))
	html_lxml = html.fromstring(html_content)

	# la proposition de loi est contenu dans le dernier div ayant la classe assnatSectionX
	# Il peut en effet y avoir des div supplémentaires pour les notes de bas de page (PIONANR5L15B0586)

	canonical_dom = get_canonical_dom(text_id, html_lxml)
	print('OK' if len(canonical_dom) else 'KO')
	alinea_list = []
	if canonical_dom:
		alinea_no = 0
		for alinea in canonical_dom:
			alinea_type = get_node_type(alinea)
			if alinea_type[0] == 'OK':
				converted_alinea = get_alinea_content(alinea, alinea_type[1], alinea_no)
				alinea_list.append(converted_alinea)
				alinea_no = converted_alinea["alinea_no"] if "alinea_no" in converted_alinea else 0
				# print(alinea.text_content())
				# print(alinea_type)
	# print(alinea_list)
	print(alinea_list)
	client.insert_one({
		"text_id": text_id,
		"content": alinea_list,
		"raw_html": html_content
	})


	# pour les propositions de loi (PIONxxx), s'il y a un exposé des motifs, il y a deux titres : exposé des motifs et proposition de loi
	# dans le cas contraire, il n'y a que la proposition de loi

	# projet de loi finance : contient 1 balise p => pas du tout le même format (PRJLANR5L15B2272)
	# l'exposé des motifs est en dehors du div
	# print ('EXPOSÉ DES MOTIFS') if 'EXPOSÉ DES MOTIFS' in text_content else print ('...')
	# print ('PROPOSITION DE LOI') if 'proposition de loi' in text_content else print ('...')


# get_text("PRJLANR5L15BTC3995")
texts_pion = [
	'PIONANR5L15B0086', 'PIONANR5L15B0101', 'PIONANR5L15B0150', 'PIONANR5L15B0228',
	'PIONANR5L15B0232', 'PIONANR5L15B0248', 'PIONANR5L15B0303', 'PIONANR5L15B0307',
	'PIONANR5L15B0310', 'PIONANR5L15B0329', 'PIONANR5L15B0331', 'PIONANR5L15B0346',
	'PIONANR5L15B0422', 'PIONANR5L15B0475', 'PIONANR5L15B0476', 'PIONANR5L15B0477',
	'PIONANR5L15B0498', 'PIONANR5L15B0516', 'PIONANR5L15B0517', 'PIONANR5L15B0520',
	'PIONANR5L15B0536', 'PIONANR5L15B0559', 'PIONANR5L15B0584', 'PIONANR5L15B0585',
	'PIONANR5L15B0586', 'PIONANR5L15B0587', 'PIONANR5L15B0589', 'PIONANR5L15B0601',
	'PIONANR5L15B0630', 'PIONANR5L15B0631', 'PIONANR5L15B0652', 'PIONANR5L15B0675',
	'PIONANR5L15B0687', 'PIONANR5L15B0702', 'PIONANR5L15B0706', 'PIONANR5L15B0717',
	'PIONANR5L15B0759', 'PIONANR5L15B0772', 'PIONANR5L15B0779', 'PIONANR5L15B0788',
	'PIONANR5L15B0799', 'PIONANR5L15B0805', 'PIONANR5L15B0833', 'PIONANR5L15B0840',
	'PIONANR5L15B0847', 'PIONANR5L15B0848', 'PIONANR5L15B0849', 'PIONANR5L15B0882',
	'PIONANR5L15B0936', 'PIONANR5L15B0940'
]
texts_prj = [
	# 'PRJLANR5L15B1516' , 'PRJLANR5L15B1673', 'PRJLANR5L15B1681', 'PRJLANR5L15B1695',
	# 'PRJLANR5L15B1696', 'PRJLANR5L15B1737', 'PRJLANR5L15B1802',
	# 'PRJLANR5L15B1831',
	# 'PRJLANR5L15B1844',
	# 'PRJLANR5L15B1880',
	# 'PRJLANR5L15B1881', 'PRJLANR5L15B1908',
	# 'PRJLANR5L15B1947', 'PRJLANR5L15B1978', 'PRJLANR5L15B1980', 'PRJLANR5L15B2070',
	# 'PRJLANR5L15B2106', 'PRJLANR5L15B2107', 'PRJLANR5L15B2135',
	'PRJLANR5L15B2137',
	# 'PRJLANR5L15B2187', 'PRJLANR5L15B2272', 'PRJLANR5L15B2274',
	# 'PRJLANR5L15B2296',
	# 'PRJLANR5L15B2357', 'PRJLANR5L15B2367', 'PRJLANR5L15B2400', 'PRJLANR5L15B2416',
	# 'PRJLANR5L15B2488', 'PRJLANR5L15B2489', 'PRJLANR5L15B2493', 'PRJLANR5L15B2535',
	# 'PRJLANR5L15B2536', 'PRJLANR5L15B2622', 'PRJLANR5L15B2623', 'PRJLANR5L15B2658',
	# 'PRJLANR5L15B2731', 'PRJLANR5L15B2750', "PRJLANR5L15B3875", 'PRJLANR5L15BTC3995'
]

for text in texts_prj:
	get_text(text)

# PRJLANR5L15B2820 chelou - projet de loi rectificative - pas sous le même format, pas d'articles
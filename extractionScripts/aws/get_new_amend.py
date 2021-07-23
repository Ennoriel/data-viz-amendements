import os
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from requests import get
from pandas import DataFrame, merge
from lxml import html, etree
from re import search, compile
from datetime import date, datetime, timedelta
from json import loads
from logger import LogDecorator


is_dev = os.environ['ENV'] == 'dev'

mongo_db = os.environ['MONGO_DB']
mongo_url = os.environ['MONGO_URL']
db = MongoClient(mongo_url, retryWrites=False, w=1)[mongo_db]
client = db['x-amendements']
client_config = db['x-config']


my_rule = {
	'url': 'https://www.assemblee-nationale.fr/dyn/15/amendements?date_depot={}&page={}',
	'item_start': 1,
	'item_end': 20,
	'web_uri': {
		'xpath': '//*[@id="tbody-amendements-list"]/tr[{}]',
		'type': 'attr',
		'attr': 'data-href',
		'xpath_param': '{}',
		'regex': r'.*'
	},
	'data': [
		{
			'value': 'amendement_no',
			'xpath': '//*[@id="tbody-amendements-list"]/tr[{}]/td[2]',
			'xpath_param': '{}',
			'regex': r'.*'
		},
		{
			'value': 'sort_initial',
			'xpath': '//*[@id="tbody-amendements-list"]/tr[{}]/td[6]',
			'xpath_param': '{}',
			'regex': r'.*'
		},
		{
			'value': 'texte_no',
			'xpath': '//*[@id="tbody-amendements-list"]/tr[{}]/td[10]',
			'xpath_param': '{}',
			'regex': r'\d+'
		}
	]
}


@LogDecorator()
def download_file(url):
	local_file_name = 'html_pages/{}.html'.format(url.replace('/', '-').replace('?', '-').replace(':', '-'))

	if is_dev and os.path.isfile(local_file_name + '.err'):
		return None

	if is_dev and os.path.isfile(local_file_name):
		with open(local_file_name, "r") as f:
			return f.read()

	else:
		page = get(url)

		if is_dev and page.status_code == 200:
			try:
				with open(local_file_name, 'w') as f:
					f.write(page.content.decode('cp1252', 'ignore'))
			except IOError:
				print('    problem while writing file {}', local_file_name)
		if page.status_code != 200:
			print('  Unexpected error: HTTP code {} at url {}'.format(page.status_code, url))
			print(page.content.decode(encoding='cp1252', errors='ignore'))
			return None

	print(page.content.decode(encoding='UTF-8'))
	return page.content.decode(encoding='UTF-8')


def get_data(html_lxml, rule):

	df = DataFrame()
	columns = ['web_uri', ] + [e['value'] for e in rule['data']]

	for item_nb in range(rule['item_start'], rule['item_end']):
		# try:
		dom_elements = html_lxml.xpath(rule['web_uri']['xpath'].format(
			eval(rule['web_uri']['xpath_param'].format(item_nb))))#[0]
		if dom_elements and len(dom_elements):
			dom_element = dom_elements[0]
		else:
			print('data not found in page')
			continue
		id_element = dom_element.text_content().strip() \
			if rule['web_uri']['type'] == 're' \
			else dom_element.get(rule['web_uri']['attr'])

		index = search(rule['web_uri']['regex'], id_element)[0]

		row = [index]
		for attribute_nb in range(0, len(rule['data'])):

			dom_element = html_lxml.xpath(rule['data'][attribute_nb]['xpath'].format(
				eval(rule['data'][attribute_nb]['xpath_param'].format(item_nb))))[0]
			if 'attribute' in rule['data'][attribute_nb]:
				dom_element = dom_element.get(rule['data'][attribute_nb]['attribute'])
			else:
				dom_element = dom_element.text_content().strip()

			value = search(rule['data'][attribute_nb]['regex'], dom_element)[0]
			value = compile(r'\s+').sub(' ', value)
			row.append(value)

		df = df.append(DataFrame([row], columns=columns))
		# except TypeError as err:
		# 	pass
		# 	print('regex pb with item {}'.format(item_nb))
		# 	print(err)
		# except Exception as err:
		# 	pass
		# 	print('xpath or regex pb with item {}'.format(item_nb))
		# 	print(err)

	if df.empty:
		# no data on page => went to far
		raise ValueError()

	web_uris = df["web_uri"].to_list()

	records = client.find({"web_uri": {"$in": web_uris}}, {"_id": 0, "web_uri": 1})
	records = list(records)
	print('{} records found in DB'.format(len(records)))
	records = [record["web_uri"] for record in records]

	df_mask = df["web_uri"].apply(lambda x: x not in records)
	df = df[df_mask]

	if df.empty:
		# all data are stored in db
		raise KeyError()

	df = df.__deepcopy__()
	df["api_uri"] = df["web_uri"].apply(search_api_uri)

	s_from_json = df["api_uri"].apply(get_df_from_json)
	s_from_json.index = list(range(s_from_json.size))

	columns = [
		"api_uri",
		"uid",
		"texteLegislatifRef",
		"cardinaliteAmdtMultiples",
		"amendementParentRef",
		"typeAuteur",
		"acteurRef",
		"groupePolitiqueRef",
		"article",
		"aaa",
		"alinea",
		"dispositif",
		"exposeSommaire"
	]

	df_from_json = DataFrame.from_dict(dict(zip(s_from_json.index, s_from_json.values))).T
	df_from_json.columns = columns

	res = merge(df, df_from_json, left_on='api_uri', right_on='api_uri')

	return res


@LogDecorator()
def get_df_from_json(api_uri):
	raw_content = download_file(os.environ['AN_URL'] + api_uri)
	json_content = loads(raw_content)
	
	return [
		api_uri,
		get_json_val(json_content, ["uid"]),
		get_json_val(json_content, ["texteLegislatifRef"]),
		get_json_val(json_content, ["cardinaliteAmdtMultiples"]),
		get_json_val(json_content, ["amendementParentRef"]),
		get_json_val(json_content, ["signataires", "auteur", "typeAuteur"]),
		get_json_val(json_content, ["signataires", "auteur", "acteurRef"]),
		get_json_val(json_content, ["signataires", "auteur", "groupePolitiqueRef"]),
		get_json_val(json_content, ["pointeurFragmentTexte", "division", "titre"]),
		get_json_val(json_content, ["pointeurFragmentTexte", "division", "avant_A_Apres"]),
		get_json_val(json_content, ["amendementStandard", "alinea", "alineaDesignation"]),
		remove_unwanted_html_markup(get_json_val(json_content, ["corps", "contenuAuteur", "dispositif"])),
		remove_unwanted_html_markup(get_json_val(json_content, ["corps", "contenuAuteur", "exposeSommaire"]))
	]


def remove_unwanted_html_markup(text):
	if not text:
		return None
	tmp = text
	tmp = compile(r'<p>&#160;</p>').sub('', tmp)
	tmp = compile(r'<p style=\"text-align: justify;\">&#160;</p>').sub('', tmp)
	return tmp


# @LogDecorator()
def get_json_val(json, keys, is_str=True):
	val = json

	for key in keys:
		if key in val:
			val = val[key]
		else:
			print('key {} not found in {}'.format(str(keys), json))
			return None

	if isinstance(val, str):
		return val if is_str else datetime.strptime(val[0:10], '%Y-%m-%d')

	return None


def search_api_uri(web_uri):
	html_content = download_file(os.environ['AN_URL'] + web_uri)
	html_lxml = html.fromstring(html_content)
	documents_html = html_lxml.xpath("//*[@id=\"amendementCard\"]/div[1]/div[2]/ul")[0]
	documents_text = etree.tostring(documents_html)
	return search(r'/dyn/\S*\.json', str(documents_text))[0]


def check_nb_amendements(html_lxml, date_search):
	config = client_config.find_one({})
	print(config)
	if 'nb_amendements' not in config or config['date_dernier_releve'] != date_search:
		config['date_dernier_releve'] = date_search
		config['nb_amendements'] = 0

	nb_amendements = html_lxml.xpath('//*[@id="amendementListFrame"]/div/div[1]/div[1]/div/div/div[2]')
	if nb_amendements:
		nb_amendements = search(r'\d+', nb_amendements[0].text_content())[0]
	print(nb_amendements)

	if config['nb_amendements'] != nb_amendements:
		print('!!')
		config['nb_amendements'] = nb_amendements
		client_config.replace_one({}, config)
		return nb_amendements
	else:
		return 0


def lambda_handler(event, context):

	date_search = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")
	page = 1
	nb_data_imported = 0

	while True:
		url = my_rule['url'].format(date_search, page)

		html_content = download_file(url)
		if not html_content:
			break

		html_lxml = html.fromstring(html_content)

		if page == 1:
			nb_ame = check_nb_amendements(html_lxml, date_search)
			if nb_ame == 0:
				break

		try:
			df = get_data(html_lxml, my_rule)
			nb_data_imported = nb_data_imported + df.shape[0]
		except ValueError:
			print("no more page to load")
			break
		except KeyError:
			print("no data to save on this page")
			page = page + 1
			continue

		records = df.to_dict(orient='records')
		try:
			client.insert_many(records, ordered=False)
		except BulkWriteError as err:
			print(err)

		page = page + 1

	print("{} amendements importés".format(nb_data_imported))

	return 0

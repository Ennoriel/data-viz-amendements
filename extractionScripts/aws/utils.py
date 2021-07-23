from logger import LogDecorator
from os import path, environ
from requests import get
from re import compile
from lxml import html

is_dev = environ['ENV'] == 'dev'


@LogDecorator()
def download_file(url):
	local_file_name = 'html_pages/{}.html'.format(url.replace('/', '-').replace('?', '-').replace(':', '-'))

	if is_dev and path.isfile(local_file_name + '.err'):
		return None

	page_content = None
	if is_dev and path.isfile(local_file_name):
		with open(local_file_name, "r", encoding='UTF-8') as f:
			return f.read()

	else:
		page = get(url)

		if is_dev and page.status_code == 200:
			try:
				page_content = page.content.decode(encoding='UTF-8')
				page_content = compile(r'\s+').sub(' ', page_content)
				page_content = compile(r'> ').sub('>', page_content)
				page_content = compile(r' <').sub('<', page_content)
				page_content = compile(r'<style.*</style>').sub('', page_content)
				# page_content = compile(r' style="[^"]*"').sub('', page_content)
				page_content = compile(r'<img[^>]*>').sub('', page_content)
				page_content = compile(r'<span>&#xa0;</span>').sub('', page_content)
				with open(local_file_name, 'w', encoding='UTF-8') as f:
					f.write(page_content)
			except IOError:
				print('    problem while writing file {}', local_file_name)
		if page.status_code != 200:
			print('  Unexpected error: HTTP code {} at url {}'.format(page.status_code, url))
			print(page.content.decode(encoding='cp1252', errors='ignore'))
			return None

	return page_content


def get_node_text(node):
	if isinstance(node, html.HtmlElement):
		res = node.text_content()
		return compile(r'\s+').sub(' ', res).strip()
	elif len(node):
		res = node[0].text_content()
		return compile(r'\s+').sub(' ', res).strip()

from urllib.request import urlopen
from bs4 import BeautifulSoup
import os.path

class SweetSpeak:
	sitemap_url = "https://sweetspeak.ru/sitemap.html"
	last_article_url = ""
	last_article_url_file = ""

	def __init__(self, last_article_url_file):
		self.last_article_url_file = last_article_url_file

		if(os.path.exists(last_article_url_file)):
			self.last_article_url = open(last_article_url_file, 'r').read()
		else:
			f = open(last_article_url_file, 'w')
			self.last_article_url = self.get_last_article_url()
			f.write(self.last_article_url)
			f.close()

	def get_last_article_url(self):
		sitemap_url_l2 = self.get_first_url_on_page(self.sitemap_url, 'post')
		last_article_url = self.get_first_url_on_page(sitemap_url_l2, 'http')
		return last_article_url

	def get_first_url_on_page(self, url, filter):
		sitemap_url = urlopen(url).read().decode('utf-8')
		soup = BeautifulSoup(str(sitemap_url), 'lxml')

		hrefs = []
		for a in soup.find_all('a', href=True):
			if a.string.find(filter) != -1:
				hrefs.append(a['href'])

		return hrefs[0]

	def update_last_article_url(self):
		self.last_article_url = self.get_last_article_url()

	def is_new_article(self):
		new_article_url = self.get_last_article_url()
		return new_article_url if new_article_url != self.last_article_url else None

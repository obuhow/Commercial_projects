import os.path

from urllib.request import urlopen
from bs4 import BeautifulSoup


class SweetSpeak:
	sitemap_url = "https://sweetspeak.ru/sitemap.html"
	last_article_url = ""
	last_article_url_file = ""

	def get_url_list(self):
		sitemaps = self.get_urls_by_filter(self.sitemap_url, 'post')
		new_articles_urls = []
		for sitemap in sitemaps:
			new_articles_urls.extend(self.get_urls_by_filter(sitemap, 'http'))
		return new_articles_urls

	def get_urls_by_filter(self, url, search_filter):
		html = urlopen(url).read().decode('utf-8')
		soup = BeautifulSoup(str(html), 'lxml')
		hrefs = []
		for a in soup.find_all('a', href=True):
			if a.string.find(search_filter) != -1:
				hrefs.append(a['href'])
		return hrefs[0]

	def update_last_article_url(self):
		self.last_article_url = self.get_last_article_url()

	def is_new_article(self):
		new_article_url = self.get_last_article_url()
		return True if new_article_url != self.last_article_url else None

	def make_a_post_from_the_article(self):
		# parse the article
		html = urlopen(self.last_article_url).read().decode('utf-8')
		soup = BeautifulSoup(str(html), 'lxml')
		# get the first paragraph of the article
		paragraph = ''
		soup.span.unwrap()
		# the article starts with third <p> tag
		p = 0
		for s in soup.select('p'):
			if p == 3:
				paragraph = s.get_text()
				# the article can start with an image or table of contents
				# if we don't find the text or text is shorter the 100 char,
				# step back and repeat
				if paragraph == '' or len(paragraph) < 100:
					p -= 1
			p += 1
		# add a link to the article
		post = paragraph + '\n' + self.last_article_url
		return post

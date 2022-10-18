from urllib.request import urlopen
from bs4 import BeautifulSoup
from sweetspeak.bot.models import Bot, PublishedPosts


class SweetSpeakParser:
	sitemap_url = "https://sweetspeak.ru/sitemap.html"
	last_post_url = ""

	def __init__(self):
		self.last_post_url = PublishedPosts.objects.all.reverse[0].url

	def get_url_list(self):
		sitemaps = self.get_urls_by_filter(self.sitemap_url, 'post')
		all_articles_urls = []
		for sitemap in sitemaps:
			all_articles_urls.extend(self.get_urls_by_filter(sitemap, 'http'))
		return all_articles_urls

	def get_urls_by_filter(self, url, search_filter):
		html = urlopen(url).read().decode('utf-8')
		soup = BeautifulSoup(str(html), 'lxml')
		hrefs = []
		for a in soup.find_all('a', href=True):
			if a.string.find(search_filter) != -1:
				hrefs.append(a['href'])
		return hrefs

	def make_new_posts(self):
		last_post_sending_time = Bot.objects.all.reverse[0].sending_datetime

		urls = self.get_url_list()
		for link in urls:
			post = self.make_a_post_from_the_article(link)
			Bot.objects.create(sending_datetime='%Y-%m-%d %H:%M:%S',
							   url=link,
							   post=post,)

	def make_a_post_from_the_article(self, url):
		# parse the article
		html = urlopen(url.read().decode('utf-8')
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
		post = paragraph + '\n' + url
		return post

from datetime import datetime, timedelta

from urllib.request import urlopen
from bs4 import BeautifulSoup

from bot.models import ScheduledPosts, PublishedPosts


class SweetSpeakParser:
    sitemap_url = "https://sweetspeak.ru/sitemap.html"
    last_post_url = ""

    def __init__(self):
        db = PublishedPosts.objects.all()
        db_reverse = db.reverse()
        self.last_post_url = db_reverse[0].url

    # The site map consists of the home page and internal pages
    def get_url_list(self):
        sitemaps = self.get_urls_by_filter(self.sitemap_url, 'post')
        all_articles_urls = []
        for sitemap in sitemaps:
            all_articles_urls.extend(self.get_urls_by_filter(sitemap, 'http'))
        return all_articles_urls

    # Filter the links, leaving only the necessary links
    def get_urls_by_filter(self, url, search_filter):
        html = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(str(html), 'lxml')
        hrefs = []
        for a in soup.find_all('a', href=True):
            if a.string.find(search_filter) != -1:
                hrefs.append(a['href'])
        return hrefs

    # From the general list we leave the links that go before the last post link
    def new_articles_urls(self):
        urls = self.get_url_list()
        new_articles_links = []
        for link in urls:
            if link == self.last_post_url:
                break
            new_articles_links.append(link)
        return new_articles_links

    # Making posts from articles and writing them into the database
    def make_new_posts(self):
        last_post_sending_time_string = ScheduledPosts.objects.all.reverse[0].sending_datetime
        last_post_sending_time = datetime.strptime(last_post_sending_time_string, '%Y-%m-%d %H:%M:%S')
        new_post_datetime = last_post_sending_time + timedelta(days=1)
        urls = self.new_articles_urls()
        for link in urls.reverse():
            post1 = self.make_a_post_from_the_article(link)
            ScheduledPosts.objects.create(sending_datetime=new_post_datetime,
                                          url=link,
                                          post=post1, )
            new_post_datetime = new_post_datetime + timedelta(1)

    def make_a_post_from_the_article(self, url):
        # parse the article
        html = urlopen(url).read().decode('utf-8')
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

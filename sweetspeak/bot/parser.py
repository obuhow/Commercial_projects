from datetime import date, time, datetime, timedelta

from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml

from .models import ScheduledPosts, PublishedPosts
from .config import SEND_HOUR, SEND_MINUTE

class SweetSpeakParser:
    sitemap_url = "https://sweetspeak.ru/sitemap.html"
    last_post_url = ""

    def __init__(self):
        print("Initialize Parser")
        if ScheduledPosts.objects.last():
            db_last = ScheduledPosts.objects.last()
            self.last_post_url = db_last.url
        elif PublishedPosts.objects.last():
            db_last = PublishedPosts.objects.last()
            self.last_post_url = db_last.url_p
        else:
            urls = self.get_url_list()
            self.last_post_url = urls[1]
    
    def get_url_list(self):
        # The site map consists of the home page and internal pages
        sitemaps = self.get_urls_by_filter(self.sitemap_url, 'post')
        all_articles_urls = []
        for sitemap in sitemaps:
            all_articles_urls.extend(self.get_urls_by_filter(sitemap, 'http'))
        return all_articles_urls

    def get_urls_by_filter(self, url, search_filter):
        # Filter the links, leaving only the necessary links
        html = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(str(html), 'lxml')
        hrefs = []
        for a in soup.find_all('a', href=True):
            if a.string.find(search_filter) != -1:
                hrefs.append(a['href'])
        return hrefs

    def new_articles_urls(self):
        # From the general list we leave the links that go before the last post link
        urls = self.get_url_list()
        new_articles_links = []
        for link in urls:
            if link == self.last_post_url:
                break
            new_articles_links.append(link)
        new_articles_links.reverse()
        return new_articles_links

    def make_new_posts(self):
        print("Make new posts")
        # Making posts from articles and writing them into the database
        now = datetime.now()
        if ScheduledPosts.objects.last():
            last_post_sending_time_string = db_last.sending_datetime
            last_post_sending_time = datetime.strptime(last_post_sending_time_string, '%Y-%m-%d %H:%M:%S')
        if ScheduledPosts.objects.last() and last_post_sending_time.time() > now.time():
            new_post_datetime = last_post_sending_time + timedelta(days=1)
        else:
            send_date = now.date() if now.time() < time(SEND_HOUR - 1, (SEND_MINUTE + 59) % 60, 0) else now.date() + timedelta(days=1)
            send_time = time(SEND_HOUR, SEND_MINUTE)
            new_post_datetime = datetime.combine(send_date, send_time)
        urls = self.new_articles_urls()
        for link in urls:
            post1 = self.make_a_post_from_the_article(link)
            ScheduledPosts.objects.create(sending_datetime=new_post_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                                          url=link,
                                          post=post1, )
            new_post_datetime = new_post_datetime + timedelta(days=1)

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

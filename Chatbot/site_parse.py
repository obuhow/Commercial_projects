from urllib.request import urlopen
from bs4 import BeautifulSoup

def parse_main_sitemap(url, mark='http'):
    html = urlopen(url).read().decode('utf-8')
    s = str(html)
    soup = BeautifulSoup(s, 'html.parser')

    hrefs = []
    for a in soup.find_all('a', href=True):
        check_url = a.string.find(mark)
        if check_url != -1:
            hrefs.append(a.string)

    articles = []
    for a in hrefs:
        check_url = a.find('sitemap')
        if check_url == -1:
            articles.append(a)
        else:
            new_map_articles = parse_main_sitemap(a, 'http')
            articles.extend(new_map_articles)

    return articles

def parse_article(url):
    html = urlopen(url).read().decode('utf-8')
    s = str(html)
    soup = BeautifulSoup(s, 'html.parser')

    text_particles = []
    for s in soup.find_all('span', attrs={'style': 'font-weight: 400;'}):
        text_particles.append(s.string)

    while text_particles.count(None) != 0:
        text_particles.remove(None)

    text = ' '.join(text_particles)

    return text

def make_dict_of_quotes(hrefs):
    quotes_dict = {}
    for a in hrefs:
        article = parse_article(a)
        sentences = article.split('.')
        if len(sentences) > 1:
            quotes_dict[a] = sentences
    return quotes_dict

url = "https://sweetspeak.ru/sitemap.html"
hrefs = parse_main_sitemap(url, 'post')
quotes_dict = make_dict_of_quotes(hrefs)

for href, quotes in quotes_dict.items():
    print(href, quotes, sep=':')
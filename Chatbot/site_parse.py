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


url = "https://sweetspeak.ru/sitemap.html"
hrefs = parse_main_sitemap(url, 'post')
print(hrefs)




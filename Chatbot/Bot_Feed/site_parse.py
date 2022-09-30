from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
from mysql.connector import connect, Error
import config

def insert_article(article_url, article_text):
    try:
        with connect(
            host='localhost',
            user=config.user_bd,
            password=config.pass_bd,
            database='article',
        ) as connection:
            with connection.cursor() as cursor:
                request = """
                    INSERT INTO article (url, text) 
                    VALUES (%s, %s);"""
                cursor.execute(request, (article_url, article_text))
                connection.commit()
    except Error as e:
        print(e)

def parse_main_sitemap(url, mark='http'):
    html = urlopen(url).read().decode('utf-8')
    s = str(html)
    soup = BeautifulSoup(s, 'lxml')

    hrefs = []
    for a in soup.find_all('a', href=True):
        check_url = a.string.find(mark)
        if check_url != -1:
            hrefs.append(a['href'])

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
    soup = BeautifulSoup(s, 'lxml')
    text_particles = [soup.h1.string, '\n']
    soup.span.unwrap()
    p = 0
    while p < 4:
        for s in soup.select('p'):
            if 2 < p < 4:
                paragraph = s.get_text()
                if paragraph != '':
                    text_particles.append(paragraph)
                    text_particles.append('\n')
                else:
                    p -= 1
            p += 1
    text_particles.append(url)
    text = ' '.join(text_particles)
    return text

def make_base_of_quotes(hrefs):
    for url in hrefs:
        article = parse_article(url)
        insert_article(url, article)

def main():
    url = "https://sweetspeak.ru/sitemap.html"
    hrefs = parse_main_sitemap(url, 'post')
    make_base_of_quotes(hrefs)

main()
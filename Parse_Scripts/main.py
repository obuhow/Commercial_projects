from urllib.request import urlopen
from bs4 import BeautifulSoup
import xlwt

def parse_html_obj(url, cols):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet("Price")

    html = urlopen(url).read().decode('utf-8')
    s = str(html)
    soup = BeautifulSoup(s, 'html.parser')

    counter = 0
    for row in soup.find_all('div', attrs={'class': 'tab th'}):
            worksheet.write(0, counter, row.string)
            counter += 1

    counter = 0
    for row in soup.find_all('div', attrs={'class': 'tab divhref'}):
            worksheet.write(counter // cols + 1, counter % cols, row.string)
            counter += 1

    workbook.save("Price.xls")


if __name__ == '__main__':
    url = "https://astra-rvd.ru/1sn-ultimate"
    cols = 4
    parse_html_obj(url, cols)





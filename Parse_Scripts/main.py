from urllib.request import urlopen
from bs4 import BeautifulSoup
import xlwt

def parse_html_obj():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet("List 1")

    html = urlopen("https://www.krpms.ru/catalog/rvd/gidravlicheskie-rukava-rvd/rvd1sn/").read().decode('utf-8')
    s = str(html)
    soup = BeautifulSoup(s, 'html.parser')

    counter = 0
    for row in soup.find_all('div', attrs={'class': 'tab th'}):
            worksheet.write(0, counter, row.string)
            counter += 1

    counter = 0
    for row in soup.find_all('div', attrs={'class': 'tab divhref'}):
            worksheet.write(counter // 9 + 1, counter % 9, row.string)
            counter += 1

    workbook.save("table.xls")


if __name__ == '__main__':
    parse_html_obj()





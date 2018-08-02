import os
import json
from scrapy import Request, Spider
from bs4 import BeautifulSoup

save_json = os.path.abspath(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..{sep}..{sep}feixiaohao.json".format(sep=os.sep))))


class FeixiaohaoInitSpider(Spider):
    name = 'feixiaohao_update'
    allow_domain = ['www.feixiaohao.com', ]
    start_urls = ['https://www.feixiaohao.com/', ]

    def __init__(self):
        self.items = list()

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        item_boxes = soup.find('table', {'class': 'new-table new-coin-list'}).find(
            'tbody').find_all('tr')
        for item_box in item_boxes:
            href = item_box.find('a')['href']
            name = item_box.find('a').text.strip()
            self.items.append({'name': name,
                               'url': 'https://www.feixiaohao.com{href}'.format(href=href)})

        next_page = soup.find('div', {'class': 'new-page-list'}).find(
            'a', {'class': 'btn btn-white active'}).find_next('a')['href']
        if next_page != '#':
            yield Request(response.urljoin(next_page), callback=self.parse)
        else:
            json.dump(self.items, open(save_json, 'w'), indent=4)

import os
import json
from scrapy import Request, Spider
from bs4 import BeautifulSoup


class FeixiaohaoInitSpider(Spider):
    name = 'feixiaohao'
    allow_domain = ['www.feixiaohao.com', ]
    start_urls = ['https://www.feixiaohao.com/', ]

    def parse(self, response):
        items = list()
        soup = BeautifulSoup(response.text, 'lxml')
        item_boxes = soup.find('table', {'class': 'new-table new-coin-list'}).find(
            'tbody').find_all('tr')
        for item_box in item_boxes:
            href = item_box.find('a')['href']
            items.append(
                'https://www.feixiaohao.com{href}/#native'.format(href=href))

        next_page = soup.find('div', {'class': 'new-page-list'}).find(
            'a', {'class': 'btn btn-white active'}).find_next('a')['href']
        if next_page != '#':
            yield Request(response.urljoin(next_page), callback=self.parse)
        for item in items:
            yield Request(response.urljoin(item), callback=self.parse_coin)

    def parse_coin(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        items_boxes = soup.find('table', {'id': 'markets'}).find(
            'tbody').find_all('tr')[1:]
        for item_boxes in items_boxes:
            item_boxes = item_boxes.find_all('td')
            platform = item_boxes[1].find('a').find('img')['alt'].strip()
            pair = item_boxes[2].text.strip()
            price = item_boxes[3].text.strip()
            volume = item_boxes[4].text.strip()
            turn_volume = item_boxes[5].text.strip()
            proportion = item_boxes[6].text.strip()

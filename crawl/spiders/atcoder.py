import logging
from datetime import datetime

import json
from scrapy import Spider, Request
from urllib.parse import unquote

from crawl.items import ContestItem, AtcoderRatingItem


class LuoguSpider(Spider):
    name = "atcoder"
    allowed_domains = ["atcoder.jp"]
    custom_settings = {
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
        'ITEM_PIPLINES': {
            'crawl.pipelines.ContestsPipeline': 300,
        },
    }

    def start_requests(self):
        opt = getattr(self, 'opt', None)
        user_name = getattr(self, 'user_name', None)
        match opt:
            case 'contests':
                url = "https://atcoder.jp/contests/"
                yield Request(url=url, callback=self.parse_contests)
            case 'rating':
                if user_name is None:
                    logging.warning(f'未指定用户名称，无法爬取 {self.name} 用户信息')
                else:
                    url = "https://atcoder.jp/users/" + user_name
                    yield Request(url=url, callback=self.parse_rating)
            case _:
                logging.warning(f'未找到蜘蛛 {self.name} 的爬取内容可选项 {opt}')

    def parse_contests(self, response):
        contests_list = response.xpath('//*[@id="contest-table-upcoming"]/div/div/table/tbody')
        contests_list = contests_list.xpath('.//tr')
        for contest in contests_list:
            cid = contest.xpath('.//td[2]/a/@href').get()[10:]
            title = contest.xpath('.//td[2]/a/text()').get()
            duration_list = contest.xpath('.//td[3]/text()').get().split(':')
            duration = int(duration_list[0]) * 60 + int(duration_list[1])
            given_format = '%Y-%m-%d %H:%M:%S%z'
            given_time = contest.xpath('.//td[1]/a/time/text()').get()
            start_time = datetime.timestamp(datetime.strptime(given_time, given_format))
            yield ContestItem(
                cid=cid,
                title=title,
                type='ICPC',
                start_time=int(start_time * 1000),
                duration=duration * 60 * 1000,
                oj='Atcoder',
                url='https://atcoder.jp/contests/' + cid
            )

    def parse_rating(self, response):
        user_info = response.xpath('//*[@id="main-container"]/div[1]/div[3]/table')
        user_name = getattr(self, 'user_name', None)
        rating = user_info.xpath('.//tr[2]/td/span[1]/text()').get()
        max_rating = user_info.xpath('.//tr[3]/td/span[1]/text()').get()
        yield AtcoderRatingItem(
            user_name=user_name,
            rating=rating,
            max_rating=max_rating
        )

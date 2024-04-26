import logging

import json
from scrapy import Spider, Request
from urllib.parse import unquote

from crawl.items import ContestItem

LUOGU_CONTEST_TYPE = ['', 'OI', 'ICPC', '乐多', 'IOI']


class LuoguSpider(Spider):
    name = "luogu"
    allowed_domains = ["luogu.com.cn"]
    custom_settings = {
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
        'ITEM_PIPLINES': {
            'crawl.pipelines.ContestsPipeline': 300,
        },
    }

    def start_requests(self):
        opt = getattr(self, 'opt', None)
        match opt:
            case 'contests':
                url = "https://www.luogu.com.cn/contest/list"
                yield Request(url=url, callback=self.parse_contests)
            case 'rating':
                pass
            case _:
                logging.warning(f'未找到蜘蛛 {self.name} 的爬取内容可选项 {opt}')

    def parse_contests(self, response):
        encoded_data = response.xpath('/html/head').re_first(r'JSON\.parse\(decodeURIComponent\(\"([^"]+)\"\)\)')
        decoded_data = json.loads(unquote(encoded_data))
        contests_list = decoded_data['currentData']['contests']['result']
        current_time = decoded_data['currentTime'] * 1000
        for contest in contests_list:
            start_time = contest['startTime'] * 1000
            end_time = contest['endTime'] * 1000
            if end_time <= current_time:
                continue
            cid = str(str(contest['id']))
            yield ContestItem(
                cid='lg' + cid,
                title=contest['name'],
                type=LUOGU_CONTEST_TYPE[contest['ruleType']],
                start_time=start_time,
                duration=end_time - start_time,
                oj='Luogu',
                url='https://www.luogu.com.cn/contest/' + cid
            )

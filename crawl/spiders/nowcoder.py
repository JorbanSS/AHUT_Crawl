import json
import logging

from scrapy import Spider, Request

from crawl.items import ContestItem

NOWCODER_CONTEST_TYPE = ['ICPC', '', 'OI', 'IOI']


class NowcoderSpider(Spider):
    name = "nowcoder"
    allowed_domains = ["nowcoder.com"]
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
                url = "https://ac.nowcoder.com/acm/contest/vip-index"
                yield Request(url=url, callback=self.parse_contests)
            case 'rating':
                pass
            case _:
                logging.warning(f'未找到蜘蛛 {self.name} 的爬取内容可选项 {opt}')

    def parse_contests(self, response):
        contests_list = response.xpath('/html/body/div[1]/div[3]/div[1]/div[2]')
        contests_list = contests_list.css('div.platform-item.js-item')
        for contest in contests_list:
            encoded_data = contest.attrib['data-json']
            decoded_data = encoded_data.replace('&quot;', '"')
            contest = json.loads(decoded_data)
            cid = str(str(contest['contestId']))
            contest_item = ContestItem(
                cid='nc' + cid,
                title=contest['contestName'],
                type=NOWCODER_CONTEST_TYPE[contest['type']],
                start_time=contest['contestStartTime'],
                duration=contest['contestDuration'],
                oj='Nowcoder',
                url='https://ac.nowcoder.com/acm/contest/' + cid
            )
            yield contest_item

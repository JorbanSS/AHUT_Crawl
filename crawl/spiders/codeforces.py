from scrapy import Spider, Request
import logging

from crawl.items import ContestItem


class CodeforcesSpider(Spider):
    name = "codeforces"
    allowed_domains = ["codeforces.com"]
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
                url = "https://codeforces.com/api/contest.list"
                yield Request(url=url, callback=self.parse_contests)
            case 'rating':
                pass
            case _:
                logging.warning(f'未找到蜘蛛 {self.name} 的爬取内容可选项 {opt}')

    def parse_contests(self, response):
        contests = response.json()['result']
        for contest in contests:
            print(contest)
            if contest['phase'] != 'FINISHED':
                contest_item = ContestItem(
                    rcid='cf' + str(contest['id']),
                    title=contest['name'],
                    type=contest['type'],
                    duration=contest['durationSeconds'],
                    start_time=contest['startTimeSeconds'],
                    oj='Codeforces',
                )
                yield contest_item
            else:
                break

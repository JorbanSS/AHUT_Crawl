from scrapy import Spider, Request, FormRequest
import logging
from urllib.parse import urlencode

from crawl.items import ContestItem, CodeforcesRatingItem
from dao import crud


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
                url = "https://codeforces.com/api/user.info"
                uid_list = getattr(self, 'uid_list', None)
                query_params = {
                    'handles': uid_list,
                    'checkHistoricHandles': 'false'
                }
                yield FormRequest(url=url, formdata=query_params, method='GET', callback=self.parse_rating)
            case _:
                logging.warning(f'未找到蜘蛛 {self.name} 的爬取内容可选项 {opt}')

    def parse_contests(self, response):
        contests = response.json()
        if contests['status'] == 'OK':
            for contest in contests['result']:
                if contest['phase'] != 'FINISHED':
                    cid = str(contest['id'])
                    contest_item = ContestItem(
                        cid='cf' + cid,
                        title=contest['name'],
                        type=contest['type'],
                        duration=contest['durationSeconds'] * 1000,
                        start_time=contest['startTimeSeconds'] * 1000,
                        oj='Codeforces',
                        url='https://codeforces.com/contest/' + cid
                    )
                    yield contest_item
                else:
                    break
        else:
            logging.error(f'{self.name} 爬取内容 近期比赛 失败')


    def parse_rating(self, response):
        user_rating_list = response.json()
        if user_rating_list['status'] == 'OK':
            for user_rating in user_rating_list['result']:
                user_rating_item = CodeforcesRatingItem(
                    uid=user_rating['handle'],
                    rating=user_rating['rating'],
                    max_rating=user_rating['maxRating'],
                )
                print(user_rating_item)
                yield user_rating_item
        else:
            logging.error(f'{self.name} 爬取内容 {self.opt} 失败')
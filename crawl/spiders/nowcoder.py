import json
import logging
from datetime import datetime

from scrapy import Spider, Request, FormRequest

from crawl.items import ContestItem, NowcoderRatingItem, NowcoderUserItem

NOWCODER_CONTEST_TYPE = ['ICPC', '', 'OI', 'IOI']


class NowcoderSpider(Spider):
    name = "nowcoder"
    allowed_domains = ["nowcoder.com"]
    custom_settings = {
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
        'ITEM_PIPLINES': {
            'crawl.pipelines.ContestsPipeline': 300,
            'crawl.pipelines.RatingPipeline': 301,
        },
    }

    def start_requests(self):
        opt = getattr(self, 'opt', '')
        match opt:
            case 'contests':
                url = "https://ac.nowcoder.com/acm/contest/vip-index"
                yield Request(url=url, callback=self.parse_contests)
            case 'rating':
                uid = getattr(self, 'uid', '')
                url = "https://ac.nowcoder.com/acm/contest/rating-history"
                query_params = {
                    'uid': uid,
                }
                yield FormRequest(
                    url=url,
                    method='GET',
                    formdata=query_params,
                    callback=self.parse_rating
                )
            case 'uid':
                user_name = getattr(self, 'user_name', '')
                url = "https://gw-c.nowcoder.com/api/sparta/pc/search"
                body_json = {
                    'query': user_name,
                    'type': 'user',
                }
                yield FormRequest(
                    url=url,
                    method='POST',
                    body=json.dumps(body_json),
                    callback=self.parse_uid,
                    headers={'Content-Type': 'application/json'},
                )
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
            yield ContestItem(
                cid='nc' + cid,
                title=contest['contestName'],
                type=NOWCODER_CONTEST_TYPE[contest['type']],
                start_time=contest['contestStartTime'],
                duration=contest['contestDuration'],
                oj='Nowcoder',
                url='https://ac.nowcoder.com/acm/contest/' + cid
            )

    def parse_rating(self, response):
        rating_history = response.json()
        uid = getattr(self, 'uid', '')
        if rating_history['code'] != 0 or len(rating_history['data']) == 0:
            logging.warning(f'Nowcoder 用户 {uid} 不存在，未找到历史数据')
            return
        rating = rating_history['data'][0]['rating']
        max_rating = rating
        rating_list = [item['rating'] for item in rating_history['data']]
        for rating in rating_list:
            if rating > max_rating:
                max_rating = rating
        yield NowcoderRatingItem(
            uid=uid,
            rating=rating,
            max_rating=max_rating,
        )

    def parse_uid(self, response):
        user_name = getattr(self, 'user_name', '')
        user_list = response.json()['data']['records']
        for user in user_list:
            if user['nickname'] == user_name:
                yield NowcoderUserItem(
                    uid=user['userId'],
                    user_name=user_name,
                )
        logging.warning(f'Nowcoder 用户 {user_name} 不存在')

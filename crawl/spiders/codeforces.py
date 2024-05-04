from scrapy import Spider, Request, FormRequest
import logging

from crawl.items import ContestItem, CodeforcesRatingItem, CodeforcesUserSubmissionItem


class CodeforcesSpider(Spider):
    name = "codeforces"
    allowed_domains = ["codeforces.com"]
    custom_settings = {
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
        'ITEM_PIPLINES': {
            'crawl.pipelines.ContestsPipeline': 300,
            'crawl.pipelines.RatingPipeline': 310,
            'crawl.pipelines.CodeforcesStatisticsPipeline': 330,
        },
    }

    def start_requests(self):
        opt = getattr(self, 'opt', None)
        base_url = 'https://codeforces.com/api'
        match opt:
            case 'contests':
                url = base_url + '/contest.list'
                yield Request(url=url, callback=self.parse_contests)
            case 'rating':
                url = base_url + '/user.info'
                user_name_list = getattr(self, 'user_name_list', '')
                query_params = {
                    'handles': user_name_list,
                    'checkHistoricHandles': 'false'
                }
                if user_name_list != '':
                    yield FormRequest(url=url, formdata=query_params, method='GET', callback=self.parse_rating)
            case 'submissions':
                url = base_url + '/user.status'
                user_name = getattr(self, 'user_name', '')
                query_params = {
                    'handle': user_name
                }
                if user_name != '':
                    yield FormRequest(url=url, formdata=query_params, method='GET', callback=self.parse_submissions)
            case _:
                logging.warning(f'未找到蜘蛛 {self.name} 的爬取内容可选项 {opt}')

    def parse_contests(self, response):
        contests = response.json()
        if contests['status'] != 'OK':
            logging.error(f'{self.name} 爬取内容 recent contests 失败')
            return
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

    def parse_rating(self, response):
        user_rating_list = response.json()
        if user_rating_list['status'] != 'OK':
            logging.error(f'{self.name} 爬取内容 rating 失败')
            return
        for user_rating in user_rating_list['result']:
            yield CodeforcesRatingItem(
                user_name=user_rating['handle'],
                rating=user_rating['rating'],
                max_rating=user_rating['maxRating'],
            )

    def parse_submissions(self, response):
        user_name = getattr(self, 'user_name', '')
        submissions = response.json()
        if submissions['status'] != 'OK':
            logging.error(f'{self.name} 爬取内容 submissions 失败')
            return
        verdict_dict: dict[str, int] = {}
        index_dict: dict[str, int] = {}
        language_dict: dict[str, int] = {}
        tags_dict: dict[str, int] = {}
        rating_dict: dict[int, int] = {}
        solved_set: set[str] = set()
        unsolved_dict: dict[str, int] = {}
        teammate_set: set[str] = set()
        attempt_count = 0
        first_attempt_passed_count = 0
        virtual_participation_set: set[str] = set()
        for submission in submissions['result'][::-1]:
            verdict_dict[submission['verdict']] = verdict_dict.get(submission['verdict'], 0) + 1
            language_dict[submission['programmingLanguage']] = language_dict.get(submission['programmingLanguage'], 0) + 1
            for team_member in submission['author']['members']:
                team_member_name = team_member.get('handle', '')
                if team_member_name != user_name:
                    teammate_set.add(team_member_name)
            if submission['author']['participantType'] == 'VIRTUAL':
                virtual_participation_set.add(submission['problem']['contestId'])
            pid = str(submission['problem']['contestId']) + submission['problem']['index']
            if pid in solved_set:
                continue
            if submission['verdict'] == 'OK':
                solved_set.add(pid)
                attempt_count += unsolved_dict.get(pid, 0) + 1
                if unsolved_dict.pop(pid, None) is None:
                    first_attempt_passed_count += 1
                if submission['problem'].get('rating') is not None:
                    rating_dict[submission['problem']['rating']] = rating_dict.get(submission['problem']['rating'], 0) + 1
                for tag in submission['problem']['tags']:
                    tags_dict[tag] = tags_dict.get(tag, 0) + 1
                index_dict[submission['problem']['index']] = index_dict.get(submission['problem']['index'], 0) + 1
            else:
                unsolved_dict[pid] = unsolved_dict.get(pid, 0) + 1
        verdict_dict = dict(sorted(verdict_dict.items(), key=lambda item: item[0]))
        index_dict = dict(sorted(index_dict.items(), key=lambda item: item[0]))
        language_dict = dict(sorted(language_dict.items(), key=lambda item: item[0]))
        tags_dict = dict(sorted(tags_dict.items(), key=lambda item: item[0]))
        rating_dict = dict(sorted(rating_dict.items(), key=lambda item: item[0]))
        teammate_list = sorted(teammate_set)
        unsolved_list = sorted(unsolved_dict.keys())
        yield CodeforcesUserSubmissionItem(
            user_name=getattr(self, 'user_name', ''),
            verdict_dict=verdict_dict,
            index_dict=index_dict,
            language_dict=language_dict,
            tags_dict=tags_dict,
            rating_dict=rating_dict,
            # submission_heat_map=submission_heat_map,
            teammate_list=teammate_list,

            virtual_participation_count=len(virtual_participation_set),

            tried=len(solved_set) + len(unsolved_list),
            solved=len(solved_set),
            average_attempts=attempt_count / len(solved_set) if len(solved_set) else 0,
            first_attempt_passed_count=first_attempt_passed_count,
            unsolved=unsolved_list,
        )

import json
import logging

from itemadapter import ItemAdapter

from dao.database import load_session
from dao.models import RecentContests, Rating, Codeforces
from .items import ContestItem, RatingItemBase, NowcoderUserItem, CodeforcesUserSubmissionItem, CodeforcesUserContestItem


class ContestsPipeline:

    def __init__(self):
        self.session = load_session()
        self.count = 0
        self.contests = []

    def close_spider(self, spider):
        if self.count % 10 != 0:
            try:
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                logging.error(e)
            finally:
                self.session.close()
        else:
            self.session.close()

    def process_item(self, item, spider):
        if isinstance(item, ContestItem):
            new_contest = RecentContests(
                CID=item.get('cid', ''),
                Title=item.get('title', ''),
                Type=item.get('type', ''),
                Duration=item.get('duration', 0),
                StartTime=item.get('start_time', 0),
                OJ=item.get('oj', ''),
                URL=item.get('url', '')
            )
            try:
                self.count += 1
                self.session.merge(new_contest)
                if self.count % 10 == 0:
                    self.session.commit()
                return item
            except Exception as e:
                self.session.rollback()
                logging.error(e)
        else:
            return item


class RatingPipeline:

    def __init__(self):
        self.session = load_session()
        self.count = 0

    def close_spider(self, spider):
        if self.count % 10 != 0:
            try:
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                logging.error(e)
            finally:
                self.session.close()
        else:
            self.session.close()

    def process_item(self, item, spider):
        if not isinstance(item, RatingItemBase):
            return item
        rating = item.get('rating', 0)
        max_rating = item.get('max_rating', 0)
        if spider.name == 'codeforces':
            existing_rating = self.session.query(Rating).filter_by(CodeforcesID=item.get('user_name', '')).first()
            if existing_rating:
                existing_rating.CodeforcesRating = rating
                existing_rating.CodeforcesMaxRating = max_rating
        elif spider.name == 'atcoder':
            existing_rating = self.session.query(Rating).filter_by(AtcoderID=item.get('user_name', '')).first()
            if existing_rating:
                existing_rating.AtcoderRating = rating
                existing_rating.AtcoderMaxRating = max_rating
        elif spider.name == 'nowcoder':
            existing_rating = self.session.query(Rating).filter_by(NowcoderID=item.get('ncid', '')).first()
            if existing_rating:
                existing_rating.NowcoderRating = rating
                existing_rating.NowcoderMaxRating = max_rating
        try:
            self.count += 1
            if self.count % 10 == 0:
                self.session.commit()
            return item
        except Exception as e:
            self.session.rollback()
            logging.error(e)


class NowcoderUserPipeline:
    def __init__(self):
        self.session = load_session()
        self.count = 0

    def close_spider(self, spider):
        if self.count != 0:
            try:
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                logging.error(e)
            finally:
                self.session.close()
        else:
            self.session.close()

    def process_item(self, item, spider):
        if isinstance(item, NowcoderUserItem):
            self.count += 1
            existing_rating = self.session.query(Rating).filter_by(UID=item.get('uid', '')).first()
            if existing_rating:
                existing_rating.NowcoderID = item.get('ncid', '')
            return item
        else:
            return item


class CodeforcesStatisticsPipeline:
    def __init__(self):
        self.session = load_session()
        self.count = 0

    def close_spider(self, spider):
        if self.count != 0:
            try:
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                logging.error(e)
            finally:
                self.session.close()
        else:
            self.session.close()

    def process_item(self, item, spider):
        user_name = item.get('user_name', '')
        if isinstance(item,  CodeforcesUserSubmissionItem):
            statistics = self.session.query(Codeforces).filter_by(CodeforcesID=user_name).first()
            if statistics is None:
                statistics = Codeforces(
                    CodeforcesID=user_name,
                    maxUp=0,
                    maxDown=0,
                    bestRank=0,
                    worstRank=0,
                    contestCount=0,
                )
            statistics.verdict = item['verdict_dict']
            statistics.problemIndex = item['index_dict']
            statistics.language = item['language_dict']
            statistics.tags = item['tags_dict']
            statistics.problemRating = item['problem_rating_dict']
            # statistics.submissionHeatMap = json.dumps(item['submission_heat_map_dict'], ensure_ascii=False)
            statistics.teamMates = ';'.join(item['teammate_list'])

            statistics.submissionCount = item['submission_count']
            statistics.tried = item['tried']
            statistics.solved = item['solved']
            statistics.averageAttempts = item['average_attempts']
            statistics.firstAttemptPassedCount = item['first_attempt_passed_count']
            statistics.unsolved = ';'.join(item['unsolved'])

            statistics.virtualParticipationCount = item['virtual_participation_count']
            self.count += 1
            self.session.merge(statistics)
        elif isinstance(item, CodeforcesUserContestItem):
            statistics = self.session.query(Codeforces).filter_by(CodeforcesID=user_name).first()
            if statistics is None:
                statistics = Codeforces(
                    CodeforcesID=user_name,
                    teamMates='',

                    submissionCount=0,
                    tried=0,
                    solved=0,
                    averageAttempts=0.00,
                    firstAttemptPassedCount=0,
                    unsolved='',

                    virtualParticipationCount=0,
                )
            statistics.maxUp = item['max_up']
            statistics.maxDown = item['max_down']
            statistics.bestRank = item['best_rank']
            statistics.worstRank = item['worst_rank']
            statistics.contestCount = item['contest_count']
            statistics.rating = {
                k: {
                    'contestID': v.contest_id,
                    'contestName': v.contest_name,
                    'rating': v.rating,
                } for k, v in item['rating'].items()
            }
            self.count += 1
            self.session.merge(statistics)
        return item

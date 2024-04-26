import logging

from itemadapter import ItemAdapter

from dao.database import load_session
from dao.models import RecentContests, Rating
from .items import ContestItem, RatingItemBase, NowcoderUserItem


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
            adapter = ItemAdapter(item)
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
                if self.count % 10 == 0:
                    self.session.commit()
                self.session.merge(new_contest)
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
        adapter = ItemAdapter(item)
        rating = item.get('rating', 0)
        max_rating = item.get('max_rating', 0)
        if spider.name == 'codeforces':
            existing_rating = self.session.query(Rating).filter_by(CodeforcesID=item.get('user_name')).first()
            if existing_rating:
                existing_rating.CodeforcesRating = rating
                existing_rating.CodeforcesMaxRating = max_rating
        elif spider.name == 'atcoder':
            existing_rating = self.session.query(Rating).filter_by(AtcoderID=item.get('user_name')).first()
            if existing_rating:
                existing_rating.AtcoderRating = rating
                existing_rating.AtcoderMaxRating = max_rating
        elif spider.name == 'nowcoder':
            existing_rating = self.session.query(Rating).filter_by(NowcoderID=item.get('uid')).first()
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
        self.users = []

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
            adapter = ItemAdapter(item)
            new_user = Rating(
                id=item.get('uid', ''),
                user_name=item.get('name', ''),
            )
            self.users.append(new_user)
        else:
            return item

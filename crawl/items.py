from scrapy.item import Item, Field


class ContestItem(Item):
    cid: int = Field()
    title: str = Field()
    type: str = Field()
    start_time: int = Field()
    duration: int = Field()
    oj: str = Field()
    url: str = Field()


class RatingItemBase(Item):
    rating: int = Field()
    max_rating: int = Field()


class CodeforcesRatingItem(RatingItemBase):
    user_name: str = Field()


class AtcoderRatingItem(RatingItemBase):
    user_name: str = Field()


class NowcoderRatingItem(RatingItemBase):
    uid: str = Field()


class NowcoderUserItem(Item):
    uid: str = Field()
    user_name: str = Field()
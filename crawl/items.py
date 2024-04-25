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
    uid: str = Field()


class CodeforcesRatingItem(RatingItemBase):
    rating: int = Field()
    max_rating: int = Field()
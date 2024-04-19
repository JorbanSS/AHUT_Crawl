from scrapy.item import Item, Field


class ContestItem(Item):
    cid: int = Field()
    title: str = Field()
    type: str = Field()
    start_time: int = Field()
    duration: int = Field()
    oj: str = Field()
    url: str = Field()

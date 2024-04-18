from scrapy.item import Item, Field


class ContestItem(Item):
    rcid: int = Field()
    title: str = Field()
    type: str = Field()
    start_time: int = Field()
    duration: int = Field()
    oj: str = Field()

from scrapy.item import Item, Field

class ContestItem(Item):
    rcid: int = Field()
    title: str = Field()
    type: str = Field()
    duration: int = Field()
    start_time: int = Field()
    oj: str = Field()
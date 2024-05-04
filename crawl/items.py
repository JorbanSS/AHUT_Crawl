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
    ncid: str = Field()


class NowcoderUserItem(Item):
    uid: str = Field()
    ncid: str = Field()


class CodeforcesUserSubmissionItem(Item):
    user_name: str = Field()
    verdict_dict: dict[str, int] = Field()
    index_dict: dict[str, int] = Field()
    language_dict: dict[str, int] = Field()
    tags_dict: dict[str, int] = Field()
    rating_dict: dict[int, int] = Field()
    # submission_heat_map: dict = Field()
    teammate_list: list[str] = Field()

    tried: int = Field()
    solved: int = Field()
    average_attempts: float = Field()
    first_attempt_passed_count: int = Field()
    unsolved: list[str] = Field()

    virtual_participation_count: int = Field()


class CodeforcesUserContestItem(Item):
    uid: str = Field()
    max_up: int = Field()
    max_down: int = Field()
    best_rank: int = Field()
    worst_rank: int = Field()
    contest_count: int = Field()

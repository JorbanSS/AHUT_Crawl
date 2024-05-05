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
    problem_rating_dict: dict[int, int] = Field()
    # submission_heat_map: dict = Field()
    teammate_list: list[str] = Field()

    submission_count: int = Field()
    tried: int = Field()
    solved: int = Field()
    average_attempts: float = Field()
    first_attempt_passed_count: int = Field()
    unsolved: list[str] = Field()

    virtual_participation_count: int = Field()


class RatingMap:
    contest_id: str = Field()
    contest_name: str = Field()
    rating: int = Field()

    def __init__(self, contest_id, contest_name, rating):
        self.contest_id = contest_id
        self.contest_name = contest_name
        self.rating = rating


class CodeforcesUserContestItem(Item):
    user_name: str = Field()
    max_up: int = Field()
    max_down: int = Field()
    best_rank: int = Field()
    worst_rank: int = Field()
    contest_count: int = Field()
    rating: dict[int, RatingMap] = Field()

from pydantic import BaseModel, ConfigDict
from typing import Optional


class BaseResponse(BaseModel):
    Code: int = 0
    Msg: str = ''

    class Config:
        orm_mode = True


class RecentContestBase(BaseModel):
    CID: str
    Title: str
    Type: str
    StartTime: int
    Duration: int
    OJ: str
    URL: str


class RecentContest(RecentContestBase):
    class Config:
        orm_mode = True
        from_attributes = True


class RecentContestsBase(BaseResponse):
    RecentContests: list[RecentContestBase]
    Count: int


class RecentContests(RecentContestsBase):
    class Config:
        orm_mode = True
        from_attributes = True


class UserBase(BaseModel):
    UID: str


class UserCreate(UserBase):
    UserName: str
    Year: int

    class Config:
        orm_mode = True
        from_attributes = True


class UserBind(UserBase):
    CodeforcesID: Optional[str] = None
    NowcoderID: Optional[str] = None
    AtcoderID: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class RatingBase(BaseModel):
    UID: str
    UserName: str
    Rating: int
    CodeforcesID: str
    CodeforcesRating: int
    CodeforcesMaxRating: int
    NowcoderID: str
    NowcoderRating: int
    NowcoderMaxRating: int
    AtcoderID: str
    AtcoderRating: int
    AtcoderMaxRating: int

    class Config:
        orm_mode = True
        from_attributes = True


class RatingRank(BaseResponse):
    RatingRank: list[RatingBase]
    Count: int

    class Config:
        orm_mode = True


class RatingMap(BaseModel):
    contestID: int
    contestName: str
    rating: int


class CodeforcesStatistics(BaseResponse):
    CodeforcesID: str
    verdict: dict[str, int]
    problemIndex: dict[str, int]
    language: dict[str, int]
    tags: dict[str, int]
    problemRating: dict[str, int]
    unsolved: str
    # submissionHeatMap: dict[str, int]
    teamMates: str
    rating: dict[int, RatingMap]

    submissionCount: int
    tried: int
    solved: int
    averageAttempts: float
    firstAttemptPassedCount: int

    virtualParticipationCount: int

    maxUp: int
    maxDown: int
    bestRank: int
    worstRank: int
    contestCount: int

    class Config:
        orm_mode = True
        from_attributes = True

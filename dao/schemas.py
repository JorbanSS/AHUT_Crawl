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


class GetRecentContests(RecentContestsBase):
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
    AtcoderID: str
    AtcoderRating: int
    class Config:
        orm_mode = True
        from_attributes = True


class RatingRank(BaseResponse):
    RatingRank: list[RatingBase]
    Count: int
    class Config:
        orm_mode = True
from pydantic import BaseModel


class RecentContest(BaseModel):
    CID: str
    Title: str
    Type: str
    StartTime: int
    Duration: int
    OJ: str
    URL: str

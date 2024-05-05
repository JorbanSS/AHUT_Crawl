from sqlalchemy import Integer, String, Text, BigInteger, JSON, Float, Numeric
from sqlalchemy import Column, ForeignKey, UniqueConstraint

from .database import Base


class User(Base):
    __tablename__ = 'user'
    UID = Column(String(20), primary_key=True, comment='用户 ID')
    UserName = Column(String(20), comment='用户名')
    Pass = Column(String(128), comment='密码')
    School = Column(String(40), comment='学校')
    Year = Column(String(4), comment='入学年份')
    Class = Column(String(20), comment='班级')
    Major = Column(String(20), comment='专业')
    Signature = Column(String(128), comment='个性签名')
    Email = Column(String(40), comment='邮箱')
    QQ = Column(String(20), comment='QQ')
    HeadUrl = Column(Text, comment='头像地址')
    LoginIP = Column(String(20), comment='最近登录 IP')
    RegisterTime = Column(BigInteger, comment='注册时间')
    Submited = Column(Integer, comment='提交次数', default=0)
    Solved = Column(Integer, comment='通过次数', default=0)


class Rating(Base):
    __tablename__ = 'rating'
    UID = Column(String(20), ForeignKey('user.UID', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True, comment='用户 ID')
    Rating = Column(Integer, comment='评分', default=0)
    CodeforcesID = Column(String(20), unique=True, comment='Codeforces 用户名')
    CodeforcesRating = Column(Integer, comment='Codeforces 评分', default=0)
    CodeforcesMaxRating = Column(Integer, comment='Codeforces 最大评分', default=0)
    NowcoderID = Column(String(20), comment='Nowcoder 用户名')
    NowcoderRating = Column(Integer, comment='Nowcoder 评分', default=0)
    NowcoderMaxRating = Column(Integer, comment='Nowcoder 最大评分', default=0)
    AtcoderID = Column(String(20), comment='Atcoder 用户名')
    AtcoderRating = Column(Integer, comment='Atcoder 评分', default=0)
    AtcoderMaxRating = Column(Integer, comment='Atcoder 最大评分', default=0)


class RecentContests(Base):
    __tablename__ = 'recentcontests'
    CID = Column(String(10), primary_key=True, comment='比赛 ID')
    Title = Column(String(100), comment='比赛名称')
    Type = Column(String(10), comment='赛制')
    StartTime = Column(String(20), comment='开始时间')
    Duration = Column(String(10), comment='持续时间')
    OJ = Column(String(10), index=True, comment='平台')
    URL = Column(String(100), comment='比赛链接')


class Codeforces(Base):
    __tablename__ = 'codeforces'
    CodeforcesID = Column(String(20), primary_key=True, comment='Codeforces 用户名')
    verdict = Column(JSON, comment='提交结果')
    problemIndex = Column(JSON, comment='题目编号')
    language = Column(JSON, comment='提交语言')
    tags = Column(JSON, comment='题目标签')
    problemRating = Column(JSON, comment='题目评分')
    unsolved = Column(Text, comment='未解决题目')
    # submissionHeatMap = Column(JSON, comment='提交热力图')
    teamMates = Column(Text, comment='队友')
    rating = Column(JSON, comment='历史评分变化')

    submissionCount = Column(Integer, comment='提交次数')
    tried = Column(Integer, comment='尝试题目数')
    solved = Column(Integer, comment='通过题目数')
    averageAttempts = Column(Numeric(precision=8, scale=2), comment='平均尝试次数')
    firstAttemptPassedCount = Column(Integer, comment='首次通过次数')

    virtualParticipationCount = Column(Integer, comment='虚拟参加次数')

    maxUp = Column(Integer, comment='最大递增评分')
    maxDown = Column(Integer, comment='最大递减评分')
    bestRank = Column(Integer, comment='最好排名')
    worstRank = Column(Integer, comment='最差排名')
    contestCount = Column(Integer, comment='参加的比赛数量')

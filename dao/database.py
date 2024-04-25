from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import config

SQLALCHEMY_DATABASE_URL = (
    'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'
    .format(config.MYSQL_USER, config.MYSQL_PASSWORD, config.MYSQL_HOST, str(config.MYSQL_PORT), config.MYSQL_DATABASE)
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    max_overflow=0,     # 超过连接池大小外最多创建的连接
    pool_size=0,        # 连接池大小
    pool_timeout=30,    # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1     # 多久之后对线程池中的线程进行一次连接的回收(重置)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def load_session():
    session = SessionLocal()
    return session

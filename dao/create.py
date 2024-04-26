import os
import logging
import pymysql

from dao.database import engine
from config import config
from dao import models

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_database():
    conn = pymysql.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        charset=config.MYSQL_CHARSET
    )

    # 创建游标对象
    cursor = conn.cursor()

    file_path = os.path.join(PROJECT_ROOT, 'config', 'create_database.sql')

    try:
        sql_query = 'CREATE DATABASE IF NOT EXISTS `ahutoj`;'
        # 执行查询
        cursor.execute(sql_query)
        # 提交事务
        conn.commit()
    except Exception as err:
        logging.error(err)
        conn.rollback()

    # 关闭游标和连接
    cursor.close()
    conn.close()


def main():
    create_database()
    models.Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    main()

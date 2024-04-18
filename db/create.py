import os
import logging

import pymysql

from config import config

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

    with open(file_path, 'r', encoding='utf-8') as file:
        sql_queries = file.read()

    try:
        # 执行查询
        for sql_query in sql_queries.split('\n\n'):
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


if __name__ == '__main__':
    main()

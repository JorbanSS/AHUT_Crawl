import pymysql

from config import config


class ContestsPipeline:

    def __init__(self):
        self.conn = pymysql.connect(
            host=config.MYSQL_HOST,
            port=config.MYSQL_PORT,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DATABASE,
            charset=config.MYSQL_CHARSET
        )
        self.cursor = self.conn.cursor()
        self.contests = []

    def close_spider(self, spider):
        self._write_to_mysql()
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        rcid = item.get('rcid', '')
        title = item.get('title', '')
        contest_type = item.get('type', '')
        duration = item.get('duration', 0)
        start_time = item.get('start_time', 0)
        oj = item.get('oj', '')
        if start_time < 1e11:
            start_time *= 1000
        self.contests.append((rcid, title, contest_type, duration, start_time, oj))
        print('输出12121212121', (rcid, title, contest_type, duration, start_time, oj))
        return item

    def _write_to_mysql(self):
        self.cursor.executemany(
            'INSERT INTO recentcontests(RCID, Title, Type, Duration, StartTime, OJ) '
            'VALUES (%s, %s, %s, %s, %s, %s)',
            self.contests
        )
        self.conn.commit()

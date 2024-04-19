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
        cid = item.get('cid', '')
        title = item.get('title', '')
        contest_type = item.get('type', '')
        duration = item.get('duration', 0)
        start_time = item.get('start_time', 0)
        oj = item.get('oj', '')
        url = item.get('url', '')
        self.contests.append((cid, title, contest_type, duration, start_time, oj, url))
        return item

    def _write_to_mysql(self):
        self.cursor.executemany(
            'INSERT INTO recentcontests(CID, Title, Type, Duration, StartTime, OJ, URL) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s)',
            self.contests
        )
        self.conn.commit()

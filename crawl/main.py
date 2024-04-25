import os

from dao import create
from config import config


def run_luogu(opt: str = 'contests'):
    command = f'scrapy crawl luogu -a opt={opt}'
    if not config.SCRAPY_LOG:
        command += ' --nolog'
    os.system(command)


def run_nowcoder(opt: str = 'contests'):
    command = f'scrapy crawl nowcoder -a opt={opt}'
    if not config.SCRAPY_LOG:
        command += ' --nolog'
    os.system(command)


def run_codeforces(opt: str = 'contests', uid_list: str = ''):
    command = f'scrapy crawl codeforces -a opt={opt}'
    if uid_list != '':
        command += f' -a uid_list={uid_list}'
    if not config.SCRAPY_LOG:
        command += ' --nolog'
    os.system(command)


def run_atcoder(opt: str = 'contests'):
    command = f'scrapy crawl atcoder -a opt={opt}'
    if not config.SCRAPY_LOG:
        command += ' --nolog'
    os.system(command)


def get_recent_contests():
    run_luogu()
    run_atcoder()
    run_nowcoder()
    run_codeforces()


def get_codeforces_rating(uid_list: str):
    run_codeforces('rating', uid_list)


def main():
    create.create_database()
    get_recent_contests()


if __name__ == '__main__':
    main()

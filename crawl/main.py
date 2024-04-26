import os

from dao import create
from config import config


def run_luogu(opt: str = 'contests'):
    command = f'scrapy crawl luogu -a opt={opt}'
    if not config.SCRAPY_LOG:
        command += ' --nolog'
    os.system(command)


def run_nowcoder(opt: str = 'contests', uid: str = ''):
    command = f'scrapy crawl nowcoder -a opt={opt}'
    if uid != '':
        command += f' -a uid={uid}'
    if not config.SCRAPY_LOG:
        command += ' --nolog'
    os.system(command)


def run_codeforces(opt: str = 'contests', user_name_list: str = ''):
    command = f'scrapy crawl codeforces -a opt={opt}'
    if user_name_list != '':
        command += f' -a user_name_list={user_name_list}'
    if not config.SCRAPY_LOG:
        command += ' --nolog'
    os.system(command)


def run_atcoder(opt: str = 'contests', user_name: str = ''):
    command = f'scrapy crawl atcoder -a opt={opt}'
    if user_name != '':
        command += f' -a user_name={user_name}'
    if not config.SCRAPY_LOG:
        command += ' --nolog'
    os.system(command)


def get_recent_contests():
    run_luogu()
    run_atcoder()
    run_nowcoder()
    run_codeforces()


def get_codeforces_rating(user_name_list: str):
    run_codeforces('rating', user_name_list)


def get_atcoder_rating(user_name: str):
    run_atcoder('rating', user_name)


def get_nowcoder_rating(uid: str):
    run_nowcoder('rating', uid)


def get_nowcoder_id(uid: str):
    run_nowcoder('id', uid)


def main():
    create.create_database()
    get_recent_contests()


if __name__ == '__main__':
    main()

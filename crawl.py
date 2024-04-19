import os

from db import create


def run_luogu(opt: str = 'contests'):
    command = f'scrapy crawl luogu -a opt={opt} --nolog'
    os.system(command)


def run_nowcoder(opt: str = 'contests'):
    command = f'scrapy crawl nowcoder -a opt={opt} --nolog'
    os.system(command)


def run_codeforces(opt: str = 'contests'):
    command = f'scrapy crawl codeforces -a opt={opt} --nolog'
    os.system(command)


def run_atcoder(opt: str = 'contests'):
    command = f'scrapy crawl atcoder -a opt={opt} --nolog'
    os.system(command)


def get_contests():
    run_luogu()
    run_nowcoder()
    run_codeforces()
    run_atcoder()


def main():
    create.create_database()
    get_contests()


if __name__ == '__main__':
    main()

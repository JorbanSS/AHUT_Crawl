import logging
import os

from dao import create
from config import config


def run_crawl(crawl_name: str):
    def inner(func):
        def wrapper(**kwargs):
            command = 'scrapy crawl ' + crawl_name
            for k, v in kwargs.items():
                command += ' -a' + k + '=' + v
            if not config.SCRAPY_LOG:
                command += ' --nolog'
            func()
            logging.info(f'Running command: {command}')
            os.system(command)
        return wrapper
    return inner


def with_opt(opt: str):
    def inner(func):
        def wrapper(**kwargs):
            kwargs['opt'] = opt
            func(**kwargs)
        return wrapper
    return inner


@with_opt('contests')
@run_crawl('codeforces')
def get_codeforces_contests(**kwargs):
    ...


@with_opt('contests')
@run_crawl('nowcoder')
def get_nowcoder_contests(**kwargs):
    ...


@with_opt('contests')
@run_crawl('atcoder')
def get_atcoder_contests(**kwargs):
    ...


@with_opt('contests')
@run_crawl('luogu')
def get_luogu_contests(**kwargs):
    ...


@with_opt('rating')
@run_crawl('codeforces')
def get_codeforces_rating(**kwargs):
    ...


@with_opt('rating')
@run_crawl('nowcoder')
def get_nowcoder_rating(**kwargs):
    ...


@with_opt('rating')
@run_crawl('atcoder')
def get_atcoder_rating(**kwargs):
    ...


@with_opt('ncid')
@run_crawl('nowcoder')
def get_nowcoder_id(**kwargs):
    ...


@with_opt('submissions')
@run_crawl('codeforces')
def get_codeforces_submissions(**kwargs):
    ...


@with_opt('user_contests')
@run_crawl('codeforces')
def get_codeforces_user_contests(**kwargs):
    ...


def main():
    # create.create_database()
    # get_codeforces_contests()
    # get_nowcoder_contests()
    # get_atcoder_contests()
    # get_luogu_contests()
    kwargs = {
        'user_name': 'JorbanS'
    }
    get_codeforces_submissions(**kwargs)
    get_codeforces_user_contests(**kwargs)


if __name__ == '__main__':
    main()

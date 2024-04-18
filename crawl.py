# 通过 CrawlerRunner 运行多个爬虫
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from db import create
from crawl.spiders.codeforces import CodeforcesSpider
from crawl.spiders.nowcoder import NowcoderSpider


def get_contests():
    create.create_database()
    opt = 'contests'
    configure_logging()
    runner = CrawlerRunner()
    runner.crawl(NowcoderSpider, opt=opt)
    # runner.crawl(CodeforcesSpider, opt=opt)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def main():
    get_contests()


if __name__ == '__main__':
    main()


# def getNowcoderContests():
#     opt = 'contests'
#     command = f'scrapy crawl nowcoder -a opt={opt}'
#     cmdline.execute(command.split())
#
# def getCodeforcesContests():
#     opt = 'contests'
#     command = f'scrapy crawl codeforces -a opt={opt}'
#     cmdline.execute(command.split())
#
# def getContests():
#     create.create_database()
#     getCodeforcesContests()
#     getNowcoderContests()

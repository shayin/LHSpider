#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from DoubanCrawler import DoubanCrawler


class DouBan(object):
    def __init__(self):
        self.crawler = DoubanCrawler()

    def start(self):
        self.crawler.set_seed_url("http://cuiqingcai.com/1319.html", deep=0)
        self.crawler.start(fetcher_num=2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
    douban = DouBan()
    douban.start()
    exit()

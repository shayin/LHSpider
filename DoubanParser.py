# -*- coding: utf-8 -*-

from LHSpider import LhParser


class DoubanParser(LhParser):
    def __init__(self):
        LhParser.__init__(self)

    def get_total_pages(self):
        return self.soup.select(".thispage")[0].attrs["data-total-page"]

# -*- coding: utf-8 -*-

from Spider import LhParser


class DoubanParser(LhParser):
    def __init__(self, max_deep=0):
        LhParser.__init__(self, max_deep)

    def get_total_pages(self):
        return self.soup.select(".thispage")[0].attrs["data-total-page"]

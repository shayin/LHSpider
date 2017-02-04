# -*- coding: utf-8 -*-

import Spider
from DoubanParser import DoubanParser


class DoubanCrawler(Spider.LhCrawler):
    def __init__(self):
        fetcher = Spider.LhFetcher(6, 1)
        parser = DoubanParser(6)
        saver = Spider.LhSaver()
        Spider.LhCrawler.__init__(self, fetcher, parser, saver, url_filter=None)
        self.perpage = 25.0

    def __get_topic_pages(self, topic_lists):
        url_lists = {}
        for topic in topic_lists:
            main_url = "https://www.douban.com/group/" + topic + "/discussion"
            result, status_code, text = self.fetcher.fetch_url_content(main_url)
            self.parser.init(text)
            total_pages = self.parser.get_total_pages()
            url_lists[topic] = {}
            url_lists[topic]['total_pages'] = total_pages
            url_lists[topic]['main_url'] = main_url
        return url_lists

    def start_producer(self):
        url_lists = self.__get_topic_pages(['tianhezufang', 'yuexiuzufang'])
        for topic in url_lists:
            for node in range(int(url_lists[topic]['total_pages'])):
                page_index = str(node * int(self.perpage))
                url = url_lists[topic]['main_url'] + "?start=" + page_index
                self.fetch_queue.put(url)
        print self.fetch_queue

    def start_consumer(self):
        pass

    # def start(self, thread_num=10):
    #     pass

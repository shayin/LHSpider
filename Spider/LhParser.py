# -*- coding: utf-8 -*-

import re
import logging
from urlparse import *
from bs4 import BeautifulSoup


class LhParser(object):
    def __init__(self, max_deep=0):
        self.soup = None
        self._max_deep = max_deep

    def init(self, html):
        self.soup = BeautifulSoup(html)

    def parse_work(self, url, code, text, deep):
        logging.info("%s parser: url=%s", self.__class__.__name__, url)
        try:
            result, url_lists, save_lists = self.parse_html(text, deep, url)
        except Exception as err:
            result, url_lists, save_lists = -1, [], {}
            logging.error("%s parser[deep=%s] error: %s", self.__class__.__name__, deep, err)
        else:
            logging.info("%s parser[deep=%s]: url=%s", self.__class__.__name__, deep, url)

        return result, (url_lists, save_lists)

    def parse_html(self, text, deep, url):
        url_lists = []
        save_lists = {}
        if deep <= self._max_deep:
            soup = BeautifulSoup(text)
            for a_tag in soup.find_all("a"):
                if a_tag.has_attr('href') and a_tag.attrs['href'] != "#" and a_tag.attrs['href'] != "/" and not re.match(r'^javascript?.+$', a_tag.attrs['href']):
                    if re.match(r'^http(s)?://.+$', a_tag.attrs['href']):
                        url_lists.append(a_tag.attrs['href'])
                    else:
                        try:
                            url_analyse = urlparse(url)
                            if re.match(r'^//.+$', a_tag.attrs['href']):
                                url_lists.append(url_analyse.scheme + ":" + a_tag.attrs['href'])
                            else:
                                url_lists.append(url_analyse.scheme + "://" + url_analyse.netloc + "/" + a_tag.attrs['href'])

                        except Exception as error:
                            logging.error("%s parser url error: %s", self.__class__.__name__, error)
            if soup.title:
                title = soup.title.string
            else:
                title = ""
            save_lists = {
                "title": title,
                # "content": text,
                "url": url,
            }
        else:
            logging.warning("%s parser[deep=%s] error: has try more than max deep %s", self.__class__.__name__, deep, self._max_deep)

        return 1, url_lists, save_lists

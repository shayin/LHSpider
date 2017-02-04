# -*- coding: utf-8 -*-

import sys
import logging
import threading

class LhSaver(object):
    def __init__(self, saver=sys.stdout):
        self._saver = saver
        self._lock = threading.Lock()

    def save_work(self, url, item):
        logging.info("%s saver: url=%s", self.__class__.__name__, url)

        try:
            result = self.save_item(item)
        except Exception as err:
            result = False
            logging.error("%s saver error: %s", self.__class__.__name__, err)
            exit()
        else:
            logging.info("%s saver: url=%s", self.__class__.__name__, url)

        return result

    def save_item(self, item):
        if not item.title:
            title = ""
        else:
            title = item.title
        self._saver.write("title: " + title + "\n")
        self._saver.flush()
        return True
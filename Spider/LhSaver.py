# -*- coding: utf-8 -*-

import logging
import threading
from pymongo import MongoClient

class LhSaver(object):
    def __init__(self, db_name, collection_name):
        self._lock = threading.Lock()
        client = MongoClient("127.0.0.1", 27017)
        self.db = client[db_name][collection_name]

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
        # encode_type = sys.getfilesystemencoding()
        # logging.error(encode_type)
        # logging.error(item)
        # title = item["title"].decode('utf-8').encode(encode_type)
        self.db.insert(item)
        return True

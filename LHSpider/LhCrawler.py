# -*- coding: utf-8 -*-

import copy
import logging
import threading
from LhTask import LhTask
from LhQueue import LhQueue
from LhWorker import FetcherWorker, ParserWorker, SaverWorker


class LhCrawler(object):
    def __init__(self, fetcher, parser, saver, url_filter=None):
        self.fetcher = fetcher
        self.parser = parser
        self.saver = saver
        self.filter = url_filter
        self.fetch_queue = LhQueue()
        self.parse_queue = LhQueue()
        self.save_queue = LhQueue()
        self._task_statue = {
            LhTask.TASK_RUNNING: 0,
            LhTask.TASK_FETCH: 0,
            LhTask.TASK_PARSE: 0,
            LhTask.TASK_SAVE: 0,
            LhTask.TASK_NOT_FETCH: 0,
            LhTask.TASK_NOT_PARSE: 0,
            LhTask.TASK_NOT_SAVE: 0,
            LhTask.TASK_ERROR: 0,
            LhTask.TASK_FAIL: 0,
        }
        self._lock = threading.Lock()

    def set_seed_url(self, seed_url, deep=0):
        logging.info("%s set_seed_url: url=%s, deep=%s", self.__class__.__name__, seed_url, deep)
        self.add_task(LhTask.TASK_FETCH, (seed_url, deep, 0))
        return

    def add_task(self, task_name, task_config):
        if task_name == LhTask.TASK_FETCH:
            self.fetch_queue.put(task_config)
            self.update_task_status(LhTask.TASK_NOT_FETCH, +1)
        elif task_name == LhTask.TASK_PARSE:
            self.parse_queue.put(task_config)
            self.update_task_status(LhTask.TASK_NOT_PARSE, +1)
        elif task_name == LhTask.TASK_SAVE:
            self.save_queue.put(task_config)
            self.update_task_status(LhTask.TASK_NOT_SAVE, +1)
        else:
            logging.error("%s add_task error: task_name[%s] is invalid", self.__class__.__name__, task_name)
            self.update_task_status(LhTask.TASK_ERROR, +1)
            exit()
        return

    def get_task(self, task_name):
        task_config = None
        if task_name == LhTask.TASK_FETCH:
            task_config = self.fetch_queue.get(block=True, timeout=5)
            self.update_task_status(LhTask.TASK_NOT_FETCH, -1)
        elif task_name == LhTask.TASK_PARSE:
            task_config = self.parse_queue.get(block=True, timeout=5)
            self.update_task_status(LhTask.TASK_NOT_PARSE, -1)
        elif task_name == LhTask.TASK_SAVE:
            task_config = self.save_queue.get(block=True, timeout=5)
            self.update_task_status(LhTask.TASK_NOT_SAVE, -1)
        else:
            logging.error("%s get_task error: task_name[%s] is invalid", self.__class__.__name__, task_name)
            self.update_task_status(LhTask.TASK_ERROR, +1)
            exit()
        self.update_task_status(LhTask.TASK_RUNNING, +1)
        return task_config

    def finish_task(self, finish_worker):
        self.update_task_status(LhTask.TASK_RUNNING, -1)
        return

    def update_task_status(self, task_name, num):
        self._lock.acquire()
        self._task_statue[task_name] += num
        self._lock.release()
        return

    def is_task_complete(self):
        # logging.warn(self._task_statue)
        if self._task_statue[LhTask.TASK_RUNNING] or self._task_statue[LhTask.TASK_NOT_FETCH] or \
                self._task_statue[LhTask.TASK_NOT_PARSE] or self._task_statue[LhTask.TASK_NOT_SAVE]:
            return False
        else:
            return True

    def start(self, fetcher_num=10):
        logging.info("%s start: fetcher_num=%s", self.__class__.__name__, fetcher_num)
        fetcher_lists = []
        for i in range(fetcher_num):
            fetcher_lists.append(FetcherWorker("fetcher-" + str(i), copy.deepcopy(self.fetcher), self))
        thread_lists = fetcher_lists + [ParserWorker("parser", self.parser, self), SaverWorker("saver", self.saver, self)]

        for thread in thread_lists:
            thread.setDaemon(True)
            thread.start()

        for thread in thread_lists:
            if thread.is_alive():
                thread.join()

        logging.info("%s crawler complete: fetcher_num=%s", self.__class__.__name__, fetcher_num)
        return

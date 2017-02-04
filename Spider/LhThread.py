# -*- coding: utf-8 -*-

import threading
import logging
import Queue


class LhThread(threading.Thread):
    def __init__(self, name, worker, pool):
        threading.Thread.__init__(self, name=name)
        self._worker = worker
        self._pool = pool
        self._name = name

    def run(self):
        logging.info("%s[%s] thread start", self.__class__.__name__, self.getName())
        while True:
            try:
                self.start_work()
            except Queue.Empty:
                logging.info("%s worker complete:  %s", self.__class__.__name__, self._name)
                if self._pool.is_task_complete():
                    break

    def start_work(self):
        raise NotImplementedError

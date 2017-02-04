# -*- coding: utf-8 -*-

import Queue

class LhQueue(object):

    def __init__(self):
        self.queue = Queue.Queue()

    def put(self, val):
        self.queue.put(val)

    def empty(self):
        return self.queue.empty()

    def get(self, block=True, timeout=5):
        return self.queue.get(block, timeout)

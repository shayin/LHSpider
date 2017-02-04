# -*- coding: utf-8 -*-

import logging
from LhTask import LhTask
from LhThread import LhThread


def fetcher_worker(self):
    # (url, deep, 0)
    url, deep, repeate = self._pool.get_task(LhTask.TASK_FETCH)
    try:
        result_code, (status_code, text, deep) = self._worker.fetch_work(url, deep, repeate)
    except Exception as err:
        result_code, status_code, text, deep = -1, None, None, None
        logging.error("%s fetcher_worker error: %s", self.__class__.__name__, err)

    if result_code > 0:
        self._pool.update_task_status(LhTask.TASK_FETCH, +1)
        self._pool.add_task(LhTask.TASK_PARSE, (url, status_code, text, deep))
    elif result_code == 0:
        self._pool.add_task(LhTask.TASK_FETCH, (url, deep, repeate + 1))
    else:
        pass

    self._pool.finish_task(LhTask.TASK_FETCH)
    return


def parser_worker(self):
    # (url, status_code, text, deep)
    url, code, text, deep = self._pool.get_task(LhTask.TASK_PARSE)
    try:
        result_code, (url_lists, save_lists) = self._worker.parse_work(url, code, text, deep)
    except Exception as err:
        result_code, url_lists, save_lists = -1, [], {}
        logging.error("%s parser_worker error: %s", self.__class__.__name__, err)

    if result_code > 0:
        self._pool.update_task_status(LhTask.TASK_PARSE, +1)
        for children_url in url_lists:
            self._pool.add_task(LhTask.TASK_FETCH, (children_url, deep+1, 0))
        # for save_item in result_content.save_lists:
        #     self._pool.add_task(LhTask.TASK_SAVE, (url, save_item))
        if save_lists:
            self._pool.add_task(LhTask.TASK_SAVE, (url, save_lists))

    self._pool.finish_task(LhTask.TASK_PARSE)
    return


def saver_worker(self):
    # (url, save_item)
    url, save_item = self._pool.get_task(LhTask.TASK_SAVE)

    try:
        result_code = self._worker.save_work(url, save_item)
    except Exception as err:
        result_code = False
        logging.error("%s saver_worker error: %s", self.__class__.__name__, err)

    if result_code:
        self._pool.update_task_status(LhTask.TASK_SAVE, +1)

    self._pool.finish_task(LhTask.TASK_SAVE)
    return

FetcherWorker = type("FetcherWorker", (LhThread,), {"start_work": fetcher_worker})
ParserWorker = type("ParserWorker", (LhThread,), {"start_work": parser_worker})
SaverWorker = type("SaverWorker", (LhThread,), {"start_work": saver_worker})

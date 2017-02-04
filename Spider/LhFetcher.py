# -*- coding: utf-8 -*-

import time
import random
import logging
import requests
from Config import CONFIG_USER_AGENT_PC, CONFIG_USER_AGENT_PHONE


class LhFetcher(object):
    def __init__(self, max_repeate_time=6, sleep_time=0, verify=False):
        self.requests = requests.session()
        self.requests.adapters.DEFAULT_RETRIES = 0
        self.max_repeate_time = max_repeate_time
        self.sleep_time = sleep_time
        self.verify = verify

    def fetch_work(self, url, deep, repeate):
        logging.info("%s fetcher[repeate=%s]: url=%s", self.__class__.__name__, repeate, url)

        if self.sleep_time > 0:
            time.sleep(random.randint(0, self.sleep_time))

        try:
            result, status_code, text = self.fetch_url_content(url)
        except Exception as err:
            if repeate >= self.max_repeate_time:
                result, status_code, text = -1, None, None
                logging.warning("%s fetcher[repeate=%s, url=%s] error: has try more than max allowed time ------ %s", self.__class__.__name__, repeate, url, err)
            else:
                result, status_code, text = 0, None, None
                logging.error("%s fetcher[repeate=%s, url=%s] error: will try again ------ %s", self.__class__.__name__, repeate, url, err)
        else:
            logging.info("%s fetcher[repeate=%s]: success url=%s", self.__class__.__name__, repeate, url)

        return result, (status_code, text, deep)

    def fetch_url_content(self, url, ua_type="pc"):
        header = {
            "User-Agent": self._get_random_user_agent(ua_type),
            "Accept-Encoding": "gzip",
        }
        res = requests.get(url, headers=header, timeout=(3, 10), verify=self.verify)
        return 1, res.status_code, res.text

    @staticmethod
    def _get_random_user_agent(user_agent_type="pc"):
        user_agent_type = user_agent_type.lower()
        assert user_agent_type in ("pc", "phone"), "get_random_user_agent: user_agent_type[%s] is invalid" % user_agent_type
        if user_agent_type == "pc":
            ua = random.choice(CONFIG_USER_AGENT_PC)
        else:
            ua = random.choice(CONFIG_USER_AGENT_PHONE)
        return ua

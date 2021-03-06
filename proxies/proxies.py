import random
import re

import requests
from bs4 import BeautifulSoup
from typing import Text


class Proxies:
    __proxy_pointer = 0

    def __init__(self) -> None:
        self.__proxies = self.get_proxies()

        self.__user_agents = [
            'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) \
            like Gecko',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        ]

    def get_proxies(self) -> []:
        response = requests.get('https://free-proxy-list.net/')
        if response.status_code == requests.codes.ok:
            page_soup = BeautifulSoup(response.text, 'html.parser')
            textarea = page_soup.find('textarea').text
            proxies = re.findall('\d+\.\d+\.\d+\.\d+\:\d+', textarea)
            return proxies
        else:
            return []

    def get_proxy(self) -> Text:
        if self.__proxy_pointer == len(self.__proxies):
            return False
        proxy = 'http://' + self.__proxies[self.__proxy_pointer]
        return proxy

    def next_proxy(self) -> None:
        self.__proxy_pointer = self.__proxy_pointer + 1

    def get_user_agent(self) -> Text:
        return self.__user_agents[
            random.randint(0, (len(self.__user_agents) - 1))
        ]

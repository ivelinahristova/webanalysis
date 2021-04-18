# content of test_proxy.py
import re

from proxies.proxies import Proxies


class TestProxies:

    def init(self):
        self.proxy = Proxies()

    def test_get_user_agent(self):
        self.init()
        user_agent = self.proxy.get_user_agent()
        assert isinstance(user_agent, str)
        matches = re.findall('^(Mozilla|Chrome)', user_agent)
        assert len(matches) == 1

    def test_get_proxies(self):
        self.init()
        proxies = self.proxy.get_proxies()
        assert isinstance(proxies, list)

    def test_get_proxy(self):
        self.init()
        proxy = self.proxy.get_proxy()
        matches = re.findall('(^[1-9.]+)', proxy)
        assert len(matches) == 0

    def test_get_all_proxies(self):
        self.init()
        all = self.proxy.get_proxies()
        print(all)
        proxy = True
        for id in range(len(all)):
            proxy = self.proxy.get_proxy()
            print(proxy)
            self.proxy.next_proxy()
            assert isinstance(proxy, str)
        proxy = self.proxy.get_proxy()
        assert proxy is False


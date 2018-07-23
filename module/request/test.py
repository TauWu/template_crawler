# -*- coding: utf-8 -*-
# HTTP Proxies test

from util.web.proxies import ProxiesVaild

class HTTPProxiesTest(object):

    @staticmethod
    def test():
        vld = ProxiesVaild(num=10)
        # Here is a log about the result of vaild proxies.
        print(vld.vaild_proxies_a)
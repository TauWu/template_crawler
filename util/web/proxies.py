# The Proxies site is http://www.xdaili.cn/

import time
import hashlib
import requests

# MutilProcess and Gevent
from multiprocessing import Process
import gevent
from gevent import monkey; monkey.patch_all()

# 配置文件
from constant.config import conf_kv_func
import asyncio

from util.common.logger import LogBase
# from module.mail.mail import Mail

# 代理 用户验证部分 - 一天检查一次，所以多次调用时不重复此步骤
class ProxiesHeaders():
    '''
    使用本代理 需要在请求头中添加 Proxy-Authorization 字段

    '''
    def __init__(self):
        # 获取配置文件
        self._conf = conf_kv_func("sys.proxy", all=True)
        self.__timestamp = str(int(time.time()))
        self.__string = "orderno={},secret={},timestamp={}".format(
            self._conf["orderno"],self._conf["secret"],self.__timestamp)
        self.__string=self.__string.encode()

    @property
    def _auth_(self):
        self.__md5_string = hashlib.md5(self.__string).hexdigest()
        self.__sign = self.__md5_string.upper()
        self._auth = "sign=%s&orderno=%s&timestamp=%s"%(self.__sign, self._conf["orderno"], self.__timestamp)
        return self._auth

    @property
    def auth_with_time(self):
        # 搭配时间戳保证时间间隔为一天（第三方要求）
        auth = self._auth_
        timestamp = self.__timestamp
        return auth, timestamp

class ProxiesRequests(ProxiesHeaders, LogBase):
    '''
    通过端口转发发起请求
    这里发起的请求应当是一个待请求的 列表

    '''
    def __init__(self, urls=[], project_name="sample", **kwargs):
        ProxiesHeaders.__init__(self)
        LogBase.__init__(self, project_name, "proxy")
        self._urls          = urls
        self._method        = 'GET'
        self._need_cookies  = False

        if "data_list" in kwargs.keys():
            self._datas     = kwargs['data_list']
            self._method    = 'POST'
        if "need_cookies" in kwargs.keys():
            self._need_cookies = True
            self._resp_cookies = None

        self.__auth_with_time   = self.auth_with_time
        self.__proxy_auth       = self.__auth_with_time[0]
        self.__timestamp        = self.__auth_with_time[1]
        self._proxy             = {
            "http"  : "http://%s"%self._conf["ip_port"],
            "https" : "https://%s"%self._conf["ip_port"]
        }
        self._headers           = {"Proxy-Authorization": self.__proxy_auth}
        self._cookies           = None
        self._single_content    = None
        self._content           = list()
        self._content_dict      = dict()

    @property
    def _get_headers_(self):
        return self._headers

    def _proxy_request_(self, url, *args):
        self._proxy_content_singal_(url, *args)
        self._content_dict[url] = self._single_content

    def _proxy_content_singal_(self, url, *args):
        '''发起单个的代理请求 可被继承'''

        self.info("start request", url=url, args=args)

        # 去除代理不安全的警告 - InsecureRequestWarning
        import requests
        from requests.packages.urllib3.exceptions import InsecureRequestWarning 
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        idx = 0
        while True:
            idx += 1
            if idx > 10:
                self._single_content = b"{}"
                self.error("BAD REQUEST =>", url=url)
                break

            try:
            # URL 请求发送
                if self._method == 'GET':
                    req = requests.get(url, headers=self._headers, cookies=self._cookies, proxies=self._proxy, allow_redirects=False, timeout=20, verify=False)
                else:
                    req = requests.post(url, headers=self._headers, cookies=self._cookies, proxies=self._proxy, allow_redirects=False, timeout=2, verify=False, data=args[0])#
                req_content = req.content
                
                if str(req_content).find("Concurrent number exceeds limit") != -1 or str(req_content) == "b''":
                    # 端口转发太频繁 重新发起请求
                    # 针对安居客 返回数据为空 重新发起请求
                    self.warn("Request too fast, continue...")
                    time.sleep(0.5)
                    continue

                if str(req_content).find("The number of requests exceeds the limit") != -1:
                    # 代理需要续费
                    self.fatal("Exceed the limit, STOP!!!")
                    break

                if str(req_content).find("Bad Gateway") != -1 or str(req_content).find("The requested URL could not be retrieved") != -1:
                    self.warn("Get bad gateway, continue...")
                    time.sleep(0.5)
                    continue
                    
                self._single_content = req_content
                self._resp_cookies   = req.cookies
                break

            except Exception as e:
                self.warn('Proxy Request timeout, continue...')
                self.debug('Proxy Err', err=e)
                time.sleep(0.5)
                continue

    @property
    def _batch_request_(self):
        '''协程执行请求 可被继承'''
        task_list = []
        if self._method == 'POST':
            for url, data in zip(self._urls, self._datas):
                task_list.append(gevent.spawn(self._proxy_request_, url, data))
        else:
            for url in self._urls:
                task_list.append(gevent.spawn(self._proxy_request_, url))
        gevent.joinall(task_list)

    @property
    def req_content_list(self):

        self.info("Start proxy request =>", length=len(self._urls))
        self._batch_request_
        self.info("Proxy request finished.")
        for url in self._urls:
            self._content.append((self._content_dict[url], url))
        if self._need_cookies:
            return self._content, self._resp_cookies
        else:
            return self._content
        
    def add_headers(self, headers):
        '''特殊的网页请求可以添加Headers'''
        self._headers = dict(self._headers, **headers)

    def add_cookies(self, cookies):
        '''特殊网页请求可以添加Cookies'''
        headers_tmp = {"Cookies":cookies}
        self.add_headers(headers_tmp)

    def add_cookies_dict(self, cookies):
        self._cookies = cookies

class ProxiesVaild(ProxiesRequests):
    '''测试代理代码'''

    def __init__(self, num=1, project_name="test"):
        raw_url = conf_kv_func("sys.proxy", "raw_url")        
        self.vaild_urls = [raw_url] * num
        self.ip_infos = []
        ProxiesRequests.__init__(self, self.vaild_urls, project_name)
        self.info("Here is debug urls =>",urls=self.vaild_urls)

        
    def _get_ip_info_(self, content):
        '''从网页中获取IP信息'''
        import re

        ip_info = re.findall(r"<center>您的IP是：\[(.+)\] 来自：(.+)</center>", content)
        try:
            ip_info = ip_info[0]
            return ip_info
        except Exception as e:
            self.err("未有匹配 %s %s %s"%(str(e)," content: ", content))
            return

    @property
    def vaild_proxies_a(self):
        '''A验证 req打包发送 resp打包返回'''
        for url in self.vaild_urls:
            self._proxy_request_(url)
        for _single_content in self._content:
            self.ip_infos.append(self._get_ip_info_(_single_content[0].decode("gb2312")))
        return self.ip_infos

    @property
    def _vaild_proxies_b_base(self):
        '''请求分别发送 更省内存'''
        for url in self.vaild_urls:
            self._proxy_content_singal_(url)
            yield self._get_ip_info_(self._single_content.decode("gb2312"))

    @property
    def vaild_proxies_b(self):
        '''B验证 req打包发送 resp分别返回'''
        for ip_info in self._vaild_proxies_b_base:
            self.ip_infos.append(ip_info)
        return self.ip_infos

    def clear_ip_info(self):
        self.ip_infos = []

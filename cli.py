from haipproxy.client.py_cli import ProxyFetcher
from log import get_log
from requests.exceptions import ReadTimeout, \
    ProxyError, ConnectTimeout, TooManyRedirects, ConnectionError
from urllib3.exceptions import MaxRetryError
import os
from redis import StrictRedis

from db import err

log = get_log('proxy')
err_log = get_log('err_log')
# log_url = get_log('urls')


import requests
args = dict(host='111.231.92.31', port=6379, password='123456', db=0)
args1 = dict(host='111.231.92.31', port=6379, password='123456', db=1)
args2= dict(host='111.231.92.31', port=6379, password='123456', db=2)

usedConn = StrictRedis(**args1)
badConn = StrictRedis(**args2)
badConn.flushdb()




headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    'Host': 'baike.molbase.cn',
    # 'Sec-Metadata': 'cause="forced", destination="document", target="top-level", site="same-origin"',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    }

import random

class Proxy:

    def __init__(self):
        self.fetcher = ProxyFetcher('https', strategy='greedy', redis_args=args)
        self.pools = self.fetcher.get_proxies()
        self.used = 1

    def get_ip(self):
        self.used += 1
        log.info("pid: {} , used: {}, length: {}, ***** {} %".format(os.getpid(),self.used, len(self.pools), self.used/(len(self.pools)+1)*100))
        if self.used > len(self.pools)/10:
            # self.fetcher = ProxyFetcher('http', strategy='greedy', redis_args=args)
            self.pools = self.fetcher.get_proxies()
            self.used = 0
            log.info("""
                        ******************************
                        ******    {}          ********
                        ******************************
                        """.format(str(len(self.pools))))
        return random.choice(self.pools)

    def remove(self, url):
        self.fetcher.delete_proxy(url)
        self.pools.remove(url)

proxy = ''

from lxml import etree
from datetime import datetime
def bads(url, content):
    badConn.sadd(url, datetime.now().strftime("%m-%d %H:%M:%S"))
    err().insert({'url':url, 'msg':content})
    if badConn.scard(url)>3:
        badConn.sadd('bads', url)

def check(content, url):
    if url.find('sds') > 0:
        return True
    # try:
    #     eles = etree.HTML(content)
    #     keys = eles.xpath('//div[@class="product clearfix"]/dl/dd/table/tbody/tr/th/text()')
    #     keys = [key[:-1] for key in keys]
    #     vals = eles.xpath('//div[@class="product clearfix"]/dl/dd/table/tbody/tr/td')
    #     vals = [ele.xpath('string(.)') for ele in vals]
    #     dt = dict(zip(keys, vals))
    #     if dt['分子式 ']:
    #         return True
    #     bads(url, content)
    # except:
    #     bads(url, content)
    #     return False
    return True

def get_data(url):
    global proxy
    if not proxy:
        proxy = Proxy()
    success = True
    retry = 3
    ips = proxy.get_ip()
    # log_url.info(url)
    while success:
        try:
            retry -= 1
            resp = requests.get(url, headers=headers, proxies={'http': ips}, timeout=15, allow_redirects=False)
            # resp = requests.get(url, headers=headers, timeout=6)
            if resp.status_code == 200:
                # nerr = check(resp.content.decode(), url)
                nerr = True
                if nerr:
                    usedConn.sadd('useful', ips)
                    # usedConn.delete(url)
                    return resp
                else:
                    if retry < 0:
                        # proxy.remove(ips)
                        # log.info("^^{}^^^  remove {} +++++{}++++".format(os.getpid(), ips, url))
                        ips = proxy.get_ip()
            # print(resp.status_code)
            err_log.info(resp.status_code)
            err_log.info(resp.url)
            log.info(resp.status_code)
            # if retry < 0:
            ips = proxy.get_ip()
        except ReadTimeout:
            print('timeout')
        except (MaxRetryError, ProxyError,
                ConnectTimeout, TooManyRedirects, ConnectionError):
            # proxy.remove(ips)
            # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
            ips = proxy.get_ip()
        except:
            # print(e)
            # log.exception(e)
            # log.info(ips)
            if retry < 0:
                # proxy.remove(ips)
                # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
                ips = proxy.get_ip()

def get_ips():
    ips = usedConn.srandmember('useful')
    if ips:
        return ips.decode()


import time
def get_use_data(url):
    success = True
    retry = 3
    ips = get_ips()
    # log_url.info(url)
    while success:
        try:
            retry -= 1
            if not ips:
                time.sleep(20)
                continue
            resp = requests.get(url, headers=headers, proxies={'http': ips}, timeout=15, allow_redirects=False)
            # resp = requests.get(url, headers=headers, timeout=6)
            if resp.status_code == 200:
                nerr = check(resp.content.decode(), url)
                if nerr:
                    usedConn.delete(url)
                    return resp

            err_log.info(resp.status_code)
            err_log.info(resp.url)
            print(resp.status_code)
            log.info(resp.status_code)
            # if retry < 0:
            if retry < 0:
                usedConn.srem('useful', ips)
                log.info("^^^^^  remove {} +++++{}++++".format(ips, url))
                ips = get_ips()
        except ReadTimeout:
            print('timeout')
        except (MaxRetryError, ProxyError,
                ConnectTimeout, TooManyRedirects, ConnectionError):
            if retry < 0:
                usedConn.srem('useful', ips)
                log.info("====  remove {} ===={}====".format(ips, url))
                ips = get_ips()
        except:
            # print(e)
            # log.exception(e)
            # log.info(ips)
            # if retry < 0:
            if retry < 0:
                usedConn.srem('useful', ips)
                log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
                ips = get_ips()

def get_data_header(url, headers):
    global proxy
    if not proxy:
        proxy = Proxy()
    success = True
    retry = 3
    ips = proxy.get_ip()
    # log_url.info(url)
    while success:
        try:
            retry -= 1
            resp = requests.get(url, headers=headers, proxies={'http': ips}, timeout=15, allow_redirects=False)
            # resp = requests.get(url, headers=headers, timeout=6)
            if resp.status_code == 302:
                # nerr = check(resp.content.decode(), url)
                usedConn.sadd('useful', ips)
                usedConn.delete(url)
                return resp
                # else:
                #     proxy.remove(ips)
                #     log.info("^^{}^^^  remove {} +++++{}++++".format(os.getpid(), ips, url))
                #     ips = proxy.get_ip()
            if resp.status_code == 200:
                return
            else:
                err_log.info(resp.status_code)
                err_log.info(resp.url)
            print(resp.status_code)
            log.info(resp.status_code)
            if retry < 0:
                ips = proxy.get_ip()
        except ReadTimeout:
            print('timeout')
        except (MaxRetryError, ProxyError,
                ConnectTimeout, TooManyRedirects, ConnectionError):
            if retry < 0:
                # proxy.remove(ips)
                # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
                ips = proxy.get_ip()
        except:
            # print(e)
            # log.exception(e)
            # log.info(ips)
            if retry < 0:
                # proxy.remove(ips)
                # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
                ips = proxy.get_ip()


def get_c_data(url):
    success = True
    while success:
        try:
            resp = requests.get(url, headers=headers, proxies={'http': '222.186.44.10:4321'}, timeout=15, allow_redirects=False)
            # resp = requests.get(url, headers=headers, timeout=6)
            if resp.status_code == 200:
                # nerr = check(resp.content.decode(), url)
                return resp
            else:
                log.info('222.186.44.10:4321*** status{}'.format(resp.status_code))
            # else:
            #     err_log.info(resp.status_code)
            #     err_log.info(resp.url)
            # print(resp.status_code)
            # log.info(resp.status_code)
        except ReadTimeout:
            print('timeout')
        except (MaxRetryError, ProxyError,
                ConnectTimeout, TooManyRedirects, ConnectionError):
            # log.info('222.186.44.10:4321+++++++++failed')
            pass
        except:
            # print(e)
            # log.exception(e)
            # log.info(ips)
            # log.info('222.186.44.10:4321+++++++++failed')
            pass


if __name__ == '__main__':
    # import sentry_sdk
    #     # sentry_sdk.init("https://34a7992a425e4144a9f4f1eadd193278@sentry.io/1355103")
    #     # from db import get_urls
    #     # urls = get_urls().find()[60000:60010]
    #     # for url in urls:
    #     #     print(get_data(url['url']).text)
    #     # try:
    #     #     requests.get("djjjkks")
    #     # except:
    #     #     pass
    resp = get_data('http://baike.molbase.cn/cidian/35609?search_keyword=67287-36-9&page=1&per_page=10')
    print(resp.status_code)

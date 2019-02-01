import requests
from log import get_log

log = get_log('http')

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

ips = ""

def get_proxy_ip():
    global ips
    # try:
    #     # resp = requests.get('http://10.9.60.13:8080/get', headers=headers, timeout=1).content.decode()
    #     resp = requests.get('http://123.207.35.36:5010/get/', headers=headers)
    #     # res = json.loads(resp.content.decode())
    #     # print(res)
    #     # if res['success']:
    #     #     res = res['data'][0]
    #     #     ips = res['ip'] + ":" + str(res['port'])
    #     ips = resp.content.decode()
    #     log.info(ips)
    #     return resp.text
    # except Exception as e:
    #     print(e)


# def get_data(url):
#     success = True
#     # retry = 6
#     # global  ips
#     # if not ips:
#     #     get_proxy_ip()
#     while success:
#         try:
#             # retry -= 1
#             resp = requests.get(url, headers=headers, proxies={'http': '111.231.92.31:3128'}, timeout=8)
#             # resp = requests.get(url, headers=headers, timeout=6)
#             if resp.status_code == 200:
#                 return resp
#                 # self.change_ip()
#             # print(resp.status_code)
#             # if retry < 0:
#             #     get_proxy_ip()
#         except Exception as e:
#             print(e)
#             log.exception(e)
#             # if retry < 0:
#             #     get_proxy_ip()

from cli import get_data


if __name__ == '__main__':
    pass
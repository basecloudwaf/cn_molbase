import requests
from cli import get_data, get_data_header
from parse import funcs
from pymongo.errors import DuplicateKeyError
from log import get_log
from run_cn import save


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "laravel_session=99f74a6aac6ee32849d4feaaee132f7d80a79692; lighting=eyJpdiI6IllvUWMwVDAxSjRJUlRcL25mdGV6d1F3PT0iLCJ2YWx1ZSI6IkdhS1J4NnhjOVJDR2NhS09oc0J0amcrcmkwcDUzT1BoQStkQUUzOXc1Z2hQU2VxUkg5UjBua01yd2haN0VlQkxhMEw3TEpHU0o1cjVXZnJYUGlmR2ZBPT0iLCJtYWMiOiI2YjkwMGI4MDNlYzk4NzU2YzA0YWEzZjAzMDlhMjgzYTVlZDA4NTkwYWQxOWY0YzY3YjA2MmVhZThiNmFiYmQwIn0%3D",
    "Host": "www.molbase.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

headers1 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Host": "baike.molbase.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

requests.get('http://www.molbase.cn/new/baike/?keyword=67287-36-9', headers=headers)
log = get_log('molbase')


def search(cas):
    resp = get_data_header('http://www.molbase.cn/new/baike/?keyword=%s'%cas, headers)
    url = resp.headers['location']
    resp = get_data('http:%s'%url)
    print(resp.text)
    parse(resp)

def parse(resp):
    try:
        dt = {'url': resp.url}
        for func in funcs:
            res = func(resp.content.decode())
            if isinstance(res, dict):
                dt[func.__name__] = res
            else:
                dt[func.__name__] = res
        # print(dt)
        save(dt)
    except DuplicateKeyError:
        flag = False
    except IndexError as e:
        # log.exception(e)
        # print(content)
        # get_proxy_ip()
        pass
    except Exception as e:
        # err().insert_many([{'url': url, 'msg': str(e)}])
        log.exception(e)


if __name__ == '__main__':
    search('67287-36-9')


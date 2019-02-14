import requests
from cli import get_data, get_data_header, get_use_data,get_c_data
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
    # print(resp.text)
    # parse(resp)
    return resp

def search_use(cas):
    resp = get_data_header('http://www.molbase.cn/new/baike/?keyword=%s'%cas, headers)
    url = resp.headers['location']
    resp = get_use_data('http:%s'%url)
    # print(resp.text)
    # parse(resp)
    return resp

def search_c(cas):
    resp = get_data_header('http://www.molbase.cn/new/baike/?keyword=%s'%cas, headers)
    url = resp.headers['location']
    resp = get_c_data('http:%s'%url)
    # print(resp.text)
    # parse(resp)
    return resp

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
        print(dt)
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

import pickle

def import_data():
    datas = pickle.load(open('add_url.pickle', 'rb'))
    for url in list(datas)[:3]:
        resp = get_data(url)
        parse(resp)
        # print(url)

from multiprocessing import Process, Queue
from queue import Empty
from db import db, err
import random
import time


def process(queue):
    print('line start')
    while True:
        try:
            dt = queue.get(True, timeout=3)
            resp = get_data(dt)
            parse(resp)
        except Empty:
            pass
        except Exception as e:
            log.exception(e)

def process_user(queue):
    print('line start')
    while True:
        try:
            dt = queue.get(True, timeout=3)
            resp = get_data(dt)
            parse(resp)
        except Empty:
            pass
        except Exception as e:
            log.exception(e)


def engin(line):
    # messages = get_urls().find()
    dbs = db()
    count = 0
    queues = [Queue() for i in range(line)]
    ps = [Process(target=process, args=(queue,)) for queue in queues[25:]]
    pss = [Process(target=process_user, args=(queue,)) for queue in queues[:25]]
    # p1 = Process(target=async_func, args=(queues, ))
    # p1.start()
    # p2 = Process(target=async_func, args=(queues, ))
    # p2.start()
    for index, p in enumerate(ps):
        p.start()
        pss[index].start()
    # for pp in pss:
    #     pp.start()
    print('enginstart')
    datas = list(pickle.load(open('add_url.pickle', 'rb')))
    while True:
        try:
            if count>=len(datas):
                continue
            msg = datas[count]
            count += 1
            print(count)
            flag = dbs.find_one({'url': msg})
            if flag:
                # print(msg['url'])
                continue
            random.choice(queues).put(msg)
            # time.sleep(500)
        except StopIteration:
            # for p in ps:
            #     p.join()
            time.sleep(500)
        except:
            # log.exception(e)
            print('err, main')
            # messages = get_urls().find()[count:]

def check_lost():
    datas = list(pickle.load(open('add_url.pickle', 'rb')))
    dbs = db()
    for url in datas:
        flag = dbs.find_one({'url': url})
        if not flag:
            print(url)
            err().insert_many([{'url':url}])


if __name__ == '__main__':
    engin(50)
    # check_lost()


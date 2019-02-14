# import gevent
# from gevent import monkey
#
# monkey.patch_all()


from parse import funcs
from proxy import get_data, get_proxy_ip
from log import get_log
from db import get_urls, db, err, cn_check_dbs
from multiprocessing import Process, Queue
import random
from pymongo.errors import DuplicateKeyError
from queue import Empty
import time
from cli import get_use_data


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
}


log = get_log('molbase')

def parse(msg):
    flag = True
    url = msg['url']
    category = msg['category']
    while flag:
        content = get_data(url).content.decode()
        try:
            dt = {'url': url, 'category': category}
            for func in funcs:
                res = func(content)
                if isinstance(res, dict):
                    dt[func.__name__] = res
                else:
                    dt[func.__name__] = res
            save(dt)
            flag = False
        except DuplicateKeyError:
            flag = False
        except IndexError as e:
            # log.exception(e)
            # print(content)
            get_proxy_ip()
        except Exception as e:
            err().insert_many([{'url': url, 'msg': str(e)}])
            log.exception(e)
            flag = False

def parse_use(msg):
    flag = True
    url = msg['url']
    category = msg['category']
    while flag:
        content = get_use_data(url).content.decode()
        try:
            dt = {'url': url, 'category': category}
            for func in funcs:
                res = func(content)
                if isinstance(res, dict):
                    dt[func.__name__] = res
                else:
                    dt[func.__name__] = res
            save(dt)
            flag = False
        except DuplicateKeyError:
            flag = False
        except IndexError as e:
            # log.exception(e)
            # print(content)
            get_proxy_ip()
        except Exception as e:
            err().insert_many([{'url': url, 'msg': str(e)}])
            log.exception(e)
            flag = False

dds = cn_check_dbs()

def save(item):
    # print(item)
    img_url = item['product_info']['product_img']
    name = down_img(img_url)
    item['product_info']['product_img_name'] = name
    props = {}
    for key, val in item.items():
        # key = key.replace('.', ' ')
        if isinstance(val, dict):
            for k, v in val.items():
                # k = k.replace('.', ' ')
                props[k] = v
        else:
            props[key] = val
    props['item'] = item
    # print(props)
    dds.insert_many([props])
    log.info('          * {} *          '.format(item['url']))


import uuid
import requests

def down(url):
    flag = True
    retry = 6
    while flag:
        try:
            # print(url)
            if retry < -1:
                return
            resp = requests.get(url, headers=headers, timeout=6)
            if resp.status_code == 200:
                return resp.content
            retry -= 1
            # print(resp.status_code)
            # print(url)
            log.info(resp.status_code)
        except Exception as e:
            retry -= 1
            print(e)
            log.error(e)

def down_img(url):
    if not url:
        return ""
    name = str(uuid.uuid4())+".png"
    content = down(url)
    with open('images/'+name, 'wb') as f:
        f.write(content)
    return name

# def async_func(queues):
#     jobs = [gevent.spawn(process, queue=queue) for queue in queues[40:]]
#     gevent.joinall(jobs)
#
# def async_func_use(queues):
#     jobs = [gevent.spawn(process_user, queue=queue) for queue in queues[40:]]
#     gevent.joinall(jobs)

def engin(line):
    messages = get_urls().find()
    dbs = db()
    count = 0
    queues = [Queue() for i in range(line)]
    ps = [Process(target=process, args=(queue,)) for queue in queues[50:]]
    pss = [Process(target=process_user, args=(queue,)) for queue in queues[:50]]
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
    while True:
        try:
            msg = messages.next()
            count += 1
            print(count)
            flag = dbs.find_one({'url': msg['url']})
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
            messages = get_urls().find()[count:]




def process(queue):
    print('line start')
    while True:
        try:
            dt = queue.get(True, timeout=3)
            parse(dt)
        except Empty:
            pass
        except Exception as e:
            log.exception(e)

def process_user(queue):
    print('line start')
    while True:
        try:
            dt = queue.get(True, timeout=3)
            parse_use(dt)
        except Empty:
            pass
        except Exception as e:
            log.exception(e)


if __name__ == '__main__':
    engin(100)
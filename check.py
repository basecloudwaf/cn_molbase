from multiprocessing import Process, Queue
from queue import Empty
from db import db, err, get_en_data, cn_check_dbs
import random
import time
from cli import get_use_data, get_data
from log import get_log
from search import search, search_use, search_c
from parse import funcs
from run_cn import save
from pymongo.errors import DuplicateKeyError



log = get_log('check_en')


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

def process(queue):
    print('line start')
    while True:
        try:
            dt = queue.get(True, timeout=3)
            resp = search(dt)
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
            resp = search_use(dt)
            parse(resp)
        except Empty:
            pass
        except Exception as e:
            log.exception(e)

def process_c(queue):
    print('line start')
    while True:
        try:
            dt = queue.get(True, timeout=3)
            resp = search_c(dt)
            parse(resp)
        except Empty:
            pass
        except Exception as e:
            log.exception(e)

def engin(line):
    # messages = get_urls().find()
    # dbs = db()
    cn_dbs = cn_check_dbs()
    count = 0
    queues = [Queue() for i in range(line)]
    ps = [Process(target=process, args=(queue,)) for queue in queues[20:]]
    # ps = [Process(target=process, args=(queue,)) for queue in queues[:1]]
    pss = [Process(target=process_user, args=(queue,)) for queue in queues[20:40]]
    psc = [Process(target=process_c, args=(queue,)) for queue in queues[10:]]
    # pss = [Process(target=process_user, args=(queue,)) for queue in queues[:-1]]
    for index, p in enumerate(ps):
        p.start()
    for ps in pss:
        ps.start()
    for pc in psc:
        pc.start()
    en_datas = get_en_data().find()
    print('enginstart')
    while True:
        try:
            msg = en_datas.next()
            count += 1
            print(count)
            # flag = dbs.find_one({'CAS ': msg['cas']})
            rep = cn_dbs.find_one({'CAS ': msg['cas']})
            if rep:
                # print(msg['url'])
                continue
            # log.info(msg['cas'])
            random.choice(queues).put(msg['cas'])
            # time.sleep(500)
        except StopIteration:
            # for p in ps:
            #     p.join()
            time.sleep(500)
        except:
            # print(e)
            # log.exception(e)
            print('err, main')
            en_datas = get_en_data().find()[count:]


if __name__ == '__main__':
    engin(50)
    # en_datas = get_en_data().find()
    # msg = en_datas.next()
    # print(msg)
import time

from prometheus_client import start_http_server
from prometheus_client.core import (
    CounterMetricFamily, REGISTRY
)
# from db import db
# from cli import usedConn

import pymongo

def db():
    client = pymongo.MongoClient('47.100.104.246', 27017, username='root', password='rootadmin', authSource='admin',
                                 authMechanism='DEFAULT')
    db = client.OLBASE
    return db.molbase_cn

from redis import StrictRedis

args1 = dict(host='111.231.92.31', port=6379, password='123456', db=1)
usedConn = StrictRedis(**args1)

args2= dict(host='111.231.92.31', port=6379, password='123456', db=2)
badConn = StrictRedis(**args2)


class CustomCollector:
    def __init__(self):
        self.db = db()
        self.used = usedConn
        self.bad = badConn
        self.current = 0

    def collect(self):
        try:
            redis_count = self.db.estimated_document_count()
            count = redis_count-self.current
            self.current = redis_count
            useds = self.used.scard("useful")
            bad = self.bad.scard('bads')
            dbsize = self.bad.dbsize()
        except AttributeError:
            redis_count = 0
            useds = 0
            bad = 0
            count = 0
            dbsize = 0
        yield CounterMetricFamily('total_success_requests',
                                  'successful requests', value=redis_count)
        yield CounterMetricFamily('total_proxy_ips', 'successful requests', value=useds)
        yield CounterMetricFamily('total_current_count', 'useful proxy', value=count)
        yield CounterMetricFamily('total_bad_tem_count', 'current bad', value=dbsize)
        yield CounterMetricFamily('total_bad_url', 'bad url', value=bad)


if __name__ == '__main__':
    port = 7000
    print('starting server http://127.0.0.1:{}/metrics'.format(port))
    REGISTRY.register(CustomCollector())
    start_http_server(port, addr='0.0.0.0')
    while True:
        time.sleep(3)


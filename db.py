import pymongo

def get_urls():
    client = pymongo.MongoClient('47.100.104.246', 27017, username='root', password='rootadmin', authSource='admin',
                                 authMechanism='DEFAULT')
    db = client.OLBASE
    return db.cn_olbase_unique_url


def db():
    client = pymongo.MongoClient('47.100.104.246', 27017, username='root', password='rootadmin', authSource='admin',
                                 authMechanism='DEFAULT')
    db = client.OLBASE
    return db.molbase_cn


def err():
    client = pymongo.MongoClient('47.100.104.246', 27017, username='root', password='rootadmin', authSource='admin',
                                 authMechanism='DEFAULT')
    db = client.OLBASE
    return db.molbase_cn_err

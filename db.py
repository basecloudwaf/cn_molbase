import pymongo

def get_urls():
    client = pymongo.MongoClient('47.100.104.246', 27017, username='root', password='rootadmin', authSource='admin',
                                 authMechanism='DEFAULT')
    db = client.OLBASE
    return db.cn_olbase_unique_url


def db():
    client = pymongo.MongoClient('47.100.104.246', 27017, username='root', password='rootadmin', authSource='admin',
                                 authMechanism='DEFAULT')
    db = client.Data
    return db.cn_olbase


def err():
    client = pymongo.MongoClient('47.100.104.246', 27017, username='root', password='rootadmin', authSource='admin',
                                 authMechanism='DEFAULT')
    db = client.OLBASE
    return db.molbase_cn_err

def get_en_data():
    client = pymongo.MongoClient('47.100.104.246', 27017, username='root', password='rootadmin', authSource='admin',
                                 authMechanism='DEFAULT')
    db = client.Data
    return db.en_olbase

def cn_check_dbs():
    client = pymongo.MongoClient('47.100.104.246', 27017, username='root', password='rootadmin', authSource='admin',
                                 authMechanism='DEFAULT')
    db = client.Data
    return db.cn_olbase_sup
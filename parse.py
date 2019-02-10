from lxml import etree
# from proxy import get_data
from cli import get_use_data as get_data


def filter(eles):
    if len(eles) > 0:
        return eles[0]
    return ''

"""
key 'SOLID (1.0% IN KBr PELLET)' must not contain '.'
"""
def product_info(content):
    eles = etree.HTML(content)
    product_img = filter(eles.xpath('//img[@id="listimg_0"]/@src'))
    if product_img:
        product_img = 'http:'+product_img
    名称 = filter(eles.xpath('//div[@class="product clearfix"]/dl/dd/h1/text()'))
    英文名 = filter(eles.xpath('//div[@class="product clearfix"]/dl/dd/p/text()'))
    英文名 = 英文名.split('：')[1] if 英文名 else ''
    keys = eles.xpath('//div[@class="product clearfix"]/dl/dd/table/tbody/tr/th/text()')
    keys = [key[:-1] for key in keys]
    vals = eles.xpath('//div[@class="product clearfix"]/dl/dd/table/tbody/tr/td')
    vals = [ele.xpath('string(.)') for ele in vals]
    参考价 = filter(eles.xpath('//div[@class="molbase-price"]/span/text()'))
    dt = dict(zip(keys, vals))
    dt['product_img'] = product_img
    dt['名称'] = 名称
    dt['英文名'] = 英文名
    dt['参考价'] = 参考价
    return dt

# <!--化合物简介-->
def info(content):
    eles = etree.HTML(content)
    return filter(eles.xpath('//div[@class="text1"]/text()'))



def detail_basic(content):
    eles = etree.HTML(content)
    keys = eles.xpath('//div[@class="detail-list basic"]/dl/dt/text()')
    keys = [key[:-1].replace('.', ' ') for key in keys]
    vals = eles.xpath('//div[@class="detail-list basic"]/dl/dd')
    vals = [val.xpath('string(.)').strip() for val in vals]
    vals[1] = [val.strip() for val in vals[1].split(';')]
    if '查看更多中文别名\n                                收起' in vals[1]:
        vals[1] = ';'.join(vals[1][:-1])
    else:
        vals[1] = ';'.join(vals[1])
    vals[3] = [val.strip() for val in vals[3].split(';')]
    if '查看更多英文别名\n                                收起' in vals[3]:
        vals[3] = ';'.join(vals[3][:-1])
    else:
        vals[3] = ';'.join(vals[3])
    # vals[3] = ";".join([:-1])
    return dict(zip(keys, vals))

# <!--分析方法开始-->
def detail_quality(content):
    eles = etree.HTML(content)
    keys = eles.xpath('//div[@class="detail-list quality"]/dl/dt/text()')
    keys = [key.replace('.', ' ') for key in keys]
    vals = eles.xpath('//div[@class="detail-list quality"]/dl/dd/text()')
    return dict(zip(keys, vals))

# <!--安全信息开始-->
def safe_info(content):
    eles = etree.HTML(content)
    items = eles.xpath('//ul[@class="way1"]/li')
    items = [item.xpath('string(.)').split('：') for item in items]
    dt = {}
    for item in items:
        dt[item[0].replace('.', ' ')] = item[1]
    return dt


# <!--生产方法以及用途-->
def method(content):
    eles = etree.HTML(content)
    method = filter(eles.xpath('//div[@id="method"]'))
    if method:
        content = etree.tostring(method, encoding="utf-8").decode()
        return content
    else:
        return ''

# <!--msds开始-->
import re
import json
import time
def parse_json(url):
    res = get_data(url).content.decode()
    flag = True
    while flag:
        try:
            sds = json.loads(res)
            if sds['code'] == 'success':
                return sds['data']
            else:
                return ''
        except Exception as e:
            time.sleep(2)
            # print(res)

def sds(content):
    res = filter(re.findall('sds_url="(.*?)"', content))
    sds = ""
    if res:
        sds = parse_json("http:"+res)
    res = filter(re.findall('sds_en_url="(.*?)"', content))
    sds_en = ""
    if res:
        sds_en = parse_json("http:" + res)
    return {'sds': sds, 'sds_en': sds_en}

def msds(content):
    eles = etree.HTML(content)
    msds = filter(eles.xpath('//div[@id="msds"]'))
    if len(msds)>0:
        msds = etree.tostring(msds, encoding="utf-8").decode()
        return msds
    else:
        return ''

# <!--海关数据开始-->
def haiguan(content):
    eles = etree.HTML(content)
    t1 = filter(eles.xpath('//div[@id="t1"]'))
    if len(t1)>0:
        content = etree.tostring(t1).decode()
        return content
    else:
        return ''

# <!--图谱开始-->
def map(content):
    eles = etree.HTML(content)
    titles = eles.xpath('//div[@class="map"]/dl/dt/span/text()')
    titles = [title.replace('.', ' ') for title in titles]
    imgs = eles.xpath('//div[@class="map"]/dl/dd/div[2]/span/img/@src')
    imgs = ['http:'+img for img in imgs]
    return dict(zip(titles, imgs))

# <!--毒性信息开始-->
def toxic(content):
    eles = etree.HTML(content)
    duxing = filter(eles.xpath('//div[@class="detail-list toxic"]'))
    if duxing:
        content = etree.tostring(duxing, encoding="utf-8").decode()
        return content
    else:
        return ''

funcs = [product_info, info, detail_basic, detail_quality, safe_info, method, sds, msds, haiguan, map, toxic]








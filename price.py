#! usr/bin/env python
#coding:utf-8
import socket
import requests
import json
import re
import logging
import httplib
from collections import OrderedDict
from getitemid import *

# print amazon_get_itemid(u'')
# print jd_get_itemid(u'')
# print dangdang_get_itemid(u'')
# print tmall_get_itemid(u'')

def getgoodip(purl):
    ipaddr = socket.getaddrinfo(purl,'http')[0][4][0]
    return ipaddr

def amazon_init(url):
    try:
        r = requests.get(url)
    except:
        return None
    start = r.text.find(u'variationDimensionValue')
    # purl = 'http://www.amazon.cn/gp/twister/ajax/prefetch?parentAsin=B00CWQI2PA&asinList=B00CWQI2PA'
    # print r.text[start:start+2000].encode('utf8')
    resultlist=[]
    if start == -1:
        oneitem={}
        start = purl.rfind(u'/',0)
        itemid = purl[start+1:].encode('utf8')
        purl = 'http://'+ip+'/gp/twister/ajax/prefetch?parentAsin='+itemid+'&asinList='+itemid
        try:
            pr = requests.get(purl)
        except:
            return None
        pstart = pr.text.find(u'actualPriceValue')
        pstart = pr.text.find(u'<b class="priceLarge">￥',pstart+len('actualPriceValue'))
        pend = pr.text.find(u'</b>',pstart+len(r'<b class="priceLarge">￥ '))
        price = pr.text[pstart+len(u'<b class="priceLarge">￥ '):pend]
        # print itemid,price
        oneitem['tag'] = ';'
        oneitem['price'] = price
        resultlist.append(oneitem)
        return resultlist
    else:
        while True:
            oneitem={}
            if start == -1:
                break
            start = r.text.find(u'.',start)
            end = r.text.find(u'"',start)
            itemid = r.text[start+1:end]
            start = r.text.find(u'value="',start)
            end = r.text.find(u'"',start+len(u'value="'))
            value = r.text[start+len(u'value="'):end]
            purl = 'http://'+ip+'/gp/twister/ajax/prefetch?parentAsin='+itemid+'&asinList='+itemid
            try:
                pr = requests.get(purl)
            except:
                return None
            pstart = pr.text.find(u'actualPriceValue')
            pstart = pr.text.find(u'<b class="priceLarge">￥',pstart+len('actualPriceValue'))
            pend = pr.text.find(u'</b>',pstart+len(r'<b class="priceLarge">￥ '))
            price = pr.text[pstart+len(u'<b class="priceLarge">￥ '):pend]
            print itemid,value.encode('utf8'),price
            # print r.text[start+1:end].encode('utf8')
            start = r.text.find(u'variationDimensionValue',start)

def amazon_search(itemid,ip):
    # purl = 'http://www.amazon.cn/gp/twister/ajax/prefetch?parentAsin=B00CWQI2PA&asinList=B00CWQI2PA'
    # print r.text[start:start+2000].encode('utf8')
    resultlist=[]
    oneitem={}
    # start = purl.rfind(u'/',0)
    # itemid = purl[start+1:].encode('utf8')
    purl = 'http://'+ip+'/gp/twister/ajax/prefetch?parentAsin='+itemid+'&asinList='+itemid
    try:
        pr = requests.get(purl)
    except:
        return None
    pstart = pr.text.find(u'actualPriceValue')
    pstart = pr.text.find(u'<b class="priceLarge">￥',pstart+len('actualPriceValue'))
    pend = pr.text.find(u'</b>',pstart+len(r'<b class="priceLarge">￥ '))
    price = pr.text[pstart+len(u'<b class="priceLarge">￥ '):pend]
    # print itemid,price
    oneitem['tag'] = ';'
    oneitem['price'] = price
    resultlist.append(oneitem)
    return resultlist

def jd_search(itemid,ip):
    purl = 'http://'+ip+'/prices/mgets?skuIds=J_'+itemid
    try:
        r = requests.get(purl)
    except:
        return None
    dic_r = json.loads(r.text)
    price = dic_r[0]["p"]
    oneitem={}
    resultlist=[]
    '''use text.find to find the price
    start = r.text.find(u'"p":"')
    end = r.text.find(u'","m"',start+len(r'","p"'))
    price = r.text[start+len(u'","p"'):end]
    use text.find to find the price'''
    oneitem['tag'] = ';'
    oneitem['price'] = price
    resultlist.append(oneitem)
    return resultlist

def dangdang_search(itemid,ip):
    purl = 'http://'+ip+'/'+itemid+'.html'
    try:
        r = requests.get(purl)
    except:
        return None
    start1 = r.text.find(u'id="promo_price"')#is there any promo
    start2 = r.text.find(u'prdJson')        #is there many items
    start3 = r.text.find(u'"proid_price":"')#is there different item have different price
    resultlist=[]
    oneitem = {}
    if start1 == -1:
        if start2 == -1:
            tag=';'
            oneitem={}
            start = r.text.find(u'id="d_price"')
            if r.text.find(u'salePriceTag">&yen;',start) != -1:
                start = r.text.find(u'salePriceTag">&yen;',start)
                end = r.text.find(u'</span>',start+len(u'id="salePriceTag">'))
                price = r.text[start+len(u'salePriceTag">&yen;'):end]
            else:
                start = r.text.find(u'</span>',start)
                end = r.text.find(u'</b>',start)
                price = r.text[start+len(u'</span>'):end]
            oneitem['tag'] = tag.encode('utf8')
            oneitem['price'] = price.encode('utf8')
            resultlist.append(oneitem)
            # print price.encode('utf8')
        else:
            start = 0
            while True:
                tag = ';'
                oneitem = {}
                start = r.text.find(u'prdid',start)
                if start == -1:
                    break
                start = r.text.find(u'"color":"',start)
                end = r.text.find(u'"',start+len(u'"color":"'))
                color = r.text[start+len(u'"color":"'):end]
                tag += 'color:'+color+';'
                start = r.text.find(u'"size":"',start)
                end = r.text.find(u'"',start+len(u'"size":"'))
                size = r.text[start+len(u'"size":"'):end]
                tag += 'size:'+size+';'
                start = r.text.find(u'"salePrice":"',start)
                end = r.text.find(u'"',start+len(u'"salePrice":"'))
                price = r.text[start+len(u'"salePrice":"'):end]
                oneitem['tag'] = tag.encode('utf8')
                oneitem['price'] = price.encode('utf8')
                resultlist.append(oneitem)
                # print tag.encode('utf8')
                # print price.encode('utf8')
    else:
        if start2 == -1 or start3 == -1:
            tag=';'
            oneitem = {}
            start = r.text.find(u'id="promo_price">')
            end = r.text.find(u' </i>',start+len(u'id="promo_price">'))
            price = r.text[start+len(u'id="promo_price">&yen;'):end]
            # print price.encode('utf8')
        else:
            start = 0
            while True:
                tag = ';'
                oneitem = {}
                start = r.text.find(u'prdid',start)
                if start == -1:
                    break
                start = r.text.find(u'"color":"',start)
                end = r.text.find(u'"',start+len(u'"color":"'))
                color = r.text[start+len(u'"color":"'):end]
                tag += 'color:'+color+';'
                start = r.text.find(u'"size":"',start)
                end = r.text.find(u'"',start+len(u'"size":"'))
                size = r.text[start+len(u'"size":"'):end]
                tag += 'size:'+size+';'
                start = r.text.find(u'"proid_price":"',start)
                end = r.text.find(u'"',start+len(u'"proid_price":"'))
                price = r.text[start+len(u'"proid_price":"'):end]
                oneitem['tag'] = tag.encode('utf8')
                oneitem['price'] = price.encode('utf8')
                resultlist.append(oneitem)
                # print tag.encode('utf8')
                # print price.encode('utf8')
    return resultlist

def tmall_search(itemid,ip):
    detail_url = 'http://detail.tmall.com/item.htm?id='+itemid
    price_url  = 'http://'+ip+ '/core/initItemDetail.htm?itemId='+itemid
    header = {'Referer':detail_url}
    try:
        dr = requests.get(detail_url)
    except:
        return None
    try:
        pr = requests.get(price_url,headers = header)
    except:
        return None
    start = pr.text.find(u'"itemPriceResultDO":')
    end = pr.text.find(u',"memberRightDO"')
    pricedata = json.loads(pr.text[start+len(u'"itemPriceResultDO":'):end])
    resultlist = []
    # print pr.text[start+len(u'"itemPriceResultDO":'):end].encode('utf8')
    for i in pricedata["priceInfo"]:
        tag=';'
        oneitem={}
        tagdic={}
        if i == 'def':
            if len(pricedata['priceInfo']) == 1:
                oneitem['tag'] = ';'
                price = pricedata["priceInfo"][i]['price']
                if pricedata["priceInfo"][i]['promotionList'] != None and pricedata["priceInfo"][i]['promotionList'][0]['type'] != u'店铺vip':
                    price = pricedata["priceInfo"][i]['promotionList'][0]['price']
                oneitem['price'] = price
                resultlist.append(oneitem)
            continue

        start = dr.text.find(i)
        if start == -1:
            continue
        end = dr.text.rfind(u';',0,start)
        while True:
            start = dr.text.rfind(u':',0,end)
            value = dr.text[start+1:end]
            end = start
            start = dr.text.rfind(u';',0,start)
            key = dr.text[start+1:end]
            end = start
            tagdic[key] = value
            # print key,value
            if dr.text[start-1] == '"':
                break
        for j in tagdic:
            tags = 'data-value="'+j+':'+tagdic[j]
            start = dr.text.find(tags)
            start = dr.text.find(u'<span>',start)
            end = dr.text.find(u'</span>',start)
            tagname = dr.text[start+len(u'<span>'):end]
            tagdic[j] = tagname.encode('utf8')
            tag += j.encode('utf8')+':'+tagdic[j]+';'
            oneitem['tag'] = tag
            # print tagname.encode('utf8')
        price = pricedata["priceInfo"][i]['price']
        if pricedata["priceInfo"][i]['promotionList'] != None and pricedata["priceInfo"][i]['promotionList'][0]['type'] != u'店铺vip':
            price = pricedata["priceInfo"][i]['promotionList'][0]['price']
        oneitem['price'] = price
        resultlist.append(oneitem)
        # print price
    # oneprice = resultlist[0]['price']
    # for i in resultlist:
    #   if i['price']!= oneprice:
    #       return resultlist
    # return [{'price':oneprice}]
    return resultlist

def taobao_brief_url(url):
    start = url.find(u'id=')
    itemid = url[start+len(u'id='):]
    return "item.taobao.com/item.htm?id="+itemid
def search_taobao(url):
    header = {'Referer':'http://item.taobao.com/item.htm?id=19565193398'}
    try:
        r = requests.get(url,headers = header)
    except:
        return None
    print r.text.encode('utf8')

# amazon_search(u'B00960YR3Q',u'203.81.17.246')
# print jd_search(u'499116',u'58.83.220.19')
# dangdang_search(u'1059068822',u'119.255.240.100')
# rest = tmall_search(u'13961714037',u'110.75.82.61')


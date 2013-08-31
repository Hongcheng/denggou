import socket
import requests
import json
import re
import logging
import httplib
from collections import OrderedDict
def amazon_get_itemid(url):
    if url.find(u'/dp/') != -1:
        start = url.find(u'/dp/')
        end  = url.find(u'/',start+len(r'/dp/'))
        itemid = url[start+len(u'/dp/'):end]
        return itemid
    elif url.find(u'/gp/product/') != -1:
        start = url.find(u'/gp/product/')
        end  = url.find(u'/',start+len(r'/gp/product/'))
        itemid = url[start+len(u'/gp/product/'):end]
        return itemid
def jd_get_itemid(url):
    start = url.find(u'item.jd.com/')
    end = url.find(u'.html',start+len(r'/'))
    itemid = url[start+len(u'item.jd.com/'):end]
    return itemid
def dangdang_get_itemid(url):
    start = url.find(u'product_id=')
    if start == -1:
        start = url.find(u'dangdang.com/')
        end = url.find(u'.html',start)
        itemid = url[start+len(u'dangdang.com/'):end]
    else:
        end = url.find(u'&',start+len(u'product_id'))
        itemid = url[start+len(u'product_id='):end]
    return itemid
def tmall_get_itemid(url):
    start = url.find(u'id=')
    end = url.find(u'&',start)
    if end == -1:
        itemid = url[start+len(u'id='):]
    else:
        itemid = url[start+len(u'id='):end]
    return itemid

# amazon_get_itemid(u'')
# jd_get_itemid(u'')
# dangdang_get_itemid(u'')
# tmall_gei_itemid(u'')
















################################################amazon######################################################
# def amazon_brief_url(url):
#     if url.find(u'/dp/') != -1:
#         start = url.find(u'/dp/')
#         end  = url.find(u'/',start+len(r'/dp/'))
#         itemid = url[start+len(u'/dp/'):end]
#         return 'http://www.amazon.cn' + '/dp/'+itemid   
#     elif url.find(u'/gp/product/') != -1:
#         start = url.find(u'/gp/product/')
#         end  = url.find(u'/',start+len(r'/gp/product/'))
#         itemid = url[start+len(u'/gp/product/'):end]
#         return 'http://www.amazon.cn' + '/gp/product/'+itemid   
# def amazon_price_url(burl):
#     '''use original url
#     start = url.find(u'/dp/')
#     end  = url.find(u'/',start+len(r'/dp/'))
#     itemid = url[start:end]
#     return 'http://www.amazon.cn' + itemid
#     '''
#     return burl
################################################jd######################################################
# def jd_brief_url(url):
#     return url
# def jd_price_url(burl):
#     start = burl.find(u'item.jd.com/')
#     end = burl.find(u'.html',start+len(r'/'))
#     itemid = burl[start+len(u'item.jd.com/'):end]
#     return 'http://p.3.cn/prices/mgets?skuIds=J_'+itemid
################################################dangdang######################################################
# def dangdang_brief_url(url):
#     start = url.find(u'product_id=')
#     if start == -1:
#         start = url.find(u'dangdang.com/')
#         end = url.find(u'.html',start)
#         itemid = url[start+len(u'dangdang.com/'):end]
#     else:
#         end = url.find(u'&',start+len(u'product_id'))
#         itemid = url[start+len(u'product_id='):end]
#     return 'http://product.dangdang.com/'+itemid+'.html'
# def dangdang_price_url(burl):
#     return burl
################################################tmall######################################################
# def tmall_brief_url(url):
#     start = url.find(u'id=')
#     end = url.find(u'&',start)
#     if end == -1:
#         itemid = url[start+len(u'id='):]
#     else:
#         itemid = url[start+len(u'id='):end]
#     '''get user_id useless
#     user_id = ''
#     start = url.find(u'user_id=')
#     if start != -1:
#         end = url.find(u'&',start)
#         if end == -1:
#             user_id = url[start+len(u'user_id='):]
#         else:
#             user_id = url[start+len(u'user_id='):end]
#     '''

#     return "http://detail.tmall.com/item.htm?id="+itemid
# def tmall_price_url(burl):
#     '''use original url
#     start = url.find(u'id=')
#     itemid = url[start+len(u'id='):]
#     '''
#     start = burl.find(u'id=')
#     itemid = burl[start+len(u'id='):]
#     return 'http://mdskip.taobao.com/core/initItemDetail.htm?itemId='+itemid



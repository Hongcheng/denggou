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
	# for i in range(10):
	# 	ipaddr = socket.getaddrinfo(purl,'http')[i][4][0]
	# 	conn = httplib.HTTPConnection(ipaddr)
	# 	conn.request("GET", "")
	# 	r1 = conn.getresponse()
	# 	print r1.status
	# 	if r1.status == 200:
	# 		return ipaddr
# print getgoodip(u'detail.tmall.com')
def amazon_search(itemid,ip):
	purl = 'http://'+ip+'/dp/'+itemid
	try:
		r = requests.get(purl)
	except:
		return None
	start = r.text.find(u'variationDimensionValue')
	# purl = 'http://www.amazon.cn/gp/twister/ajax/prefetch?parentAsin=B00CWQI2PA&asinList=B00CWQI2PA'
	# print r.text[start:start+2000].encode('utf8')
	if start == -1:
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
		print itemid,price
		# start = r.text.find(u'actualPriceValue')
		# start = r.text.find(u'<b class="priceLarge">￥',start+len('actualPriceValue'))
		# end = r.text.find(u'</b>',start+len(r'<b class="priceLarge">￥ '))
		# price = r.text[start+len(u'<b class="priceLarge">￥ '):end]
	else:
		resultlist={}
		while True:
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

def jd_search(itemid,ip):
	purl = 'http://'+ip+'/prices/mgets?skuIds=J_'+itemid
	try:
		r = requests.get(purl)
	except:
		return None
	dic_r = json.loads(r.text)
	price = dic_r[0]["p"]
	'''use text.find to find the price
	start = r.text.find(u'"p":"')
	end = r.text.find(u'","m"',start+len(r'","p"'))
	price = r.text[start+len(u'","p"'):end]
	use text.find to find the price'''
	return price

def dangdang_search(itemid,ip):
	purl = 'http://'+ip+'/'+itemid+'.html'
	try:
		r = requests.get(purl)
	except:
		return None
	start1 = r.text.find(u'id="promo_price"')
	start2 = r.text.find(u'prdJson')
	start3 = r.text.find(u'"proid_price":"')
	if start1 == -1:
		if start2 == -1:
			start = r.text.find(u'id="d_price"')
			if r.text.find(u'salePriceTag">&yen;',start) != -1:
				start = r.text.find(u'salePriceTag">&yen;',start)
				end = r.text.find(u'</span>',start+len(u'id="salePriceTag">'))
				price = r.text[start+len(u'salePriceTag">&yen;'):end]
			else:
				start = r.text.find(u'</span>',start)
				end = r.text.find(u'</b>',start)
				price = r.text[start+len(u'</span>'):end]
			print price
		else:
			start = 0
			while True:
				start = r.text.find(u'prdid',start)
				if start == -1:
					break
				tag = ';'
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
				print tag.encode('utf8')
				print price
	else:
		if start2 == -1 or start3 == -1:
			start = r.text.find(u'id="promo_price">')
			end = r.text.find(u' </i>',start+len(u'id="promo_price">'))
			price = r.text[start+len(u'id="promo_price">&yen;'):end]
			print price
		else:
			start = 0
			while True:
				start = r.text.find(u'prdid',start)
				if start == -1:
					break
				tag = ';'
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
				print tag.encode('utf8')
				print price

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
	# print pr.text[start+len(u'"itemPriceResultDO":'):end].encode(u'utf8')
	pricedata = json.loads(pr.text[start+len(u'"itemPriceResultDO":'):end])
	resultlist = []
	
	for i in pricedata["priceInfo"]:
		start = dr.text.find(i)
		if start == -1:
			continue
		tagdic = {}
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
			# print tagname.encode('utf8')
		price = pricedata["priceInfo"][i]['price']
		if pricedata["priceInfo"][i]['promotionList'] != None and pricedata["priceInfo"][i]['promotionList'][0]['type'] != u'店铺vip':
			price = pricedata["priceInfo"][i]['promotionList'][0]['price']
		tagdic['price'] = price
		resultlist.append(tagdic)
		# print price
	# oneprice = resultlist[0]['price']
	# for i in resultlist:
	# 	if i['price']!= oneprice:
	# 		return resultlist
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

# burl = tmall_brief_url(u'http://detail.tmall.com/item.htm?spm=a230r.1.14.202.fzOXGO&id=26704100255')
# purl = tmall_price_url(burl)
# rest = tmall_search(purl)
# print 123
# for i in rest:
# 	# print i
# 	for j in i:
# 		print i[j]




















#############################amazon_search##################################
ip = getgoodip(u'amazon.cn')
print 'blue'
amazon_search(u'B007WQP1ZY',ip)
# print "blue"
# print amazon_search(u"http://www.amazon.cn/dp/B007WQP1ZF")
# print "cha"
# print amazon_search(u"http://www.amazon.cn/dp/B007RSKTXQ")
# print "red"
# print amazon_search(u"http://www.amazon.cn/dp/B007RSKSR8")
# print "xi"
# print amazon_search(u"http://www.amazon.cn/dp/B005EE1G46")
# print "cu"
# print amazon_search(u"http://www.amazon.cn/dp/B005EE1FOW")
# print 'jdhei'
# print jd_search('http://p.3.cn/prices/mgets?skuIds=J_912574')
# print 'hei'
# print jd_search('http://p.3.cn/prices/mgets?skuIds=J_584773')
# print 'blue'
# print jd_search('http://p.3.cn/prices/mgets?skuIds=J_613974')
# print 'red'
# print jd_search('http://p.3.cn/prices/mgets?skuIds=J_613972')
# print 'cha'
# print jd_search('http://p.3.cn/prices/mgets?skuIds=J_613970')
# print 'xi'
# print jd_search('http://p.3.cn/prices/mgets?skuIds=J_372416')
# print 'cu'
# print jd_search('http://p.3.cn/prices/mgets?skuIds=J_372412')

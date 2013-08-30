#! usr/bin/env python
#coding:utf-8
import requests
import json
import re
import logging
from collections import OrderedDict
def amazon_brief_url(url):
	if url.find(u'/dp/') != -1:
		start = url.find(u'/dp/')
		end  = url.find(u'/',start+len(r'/dp/'))
		itemid = url[start+len(u'/dp/'):end]
		return 'http://www.amazon.cn' + '/dp/'+itemid	
	elif url.find(u'/gp/product/') != -1:
		start = url.find(u'/gp/product/')
		end  = url.find(u'/',start+len(r'/gp/product/'))
		itemid = url[start+len(u'/gp/product/'):end]
		return 'http://www.amazon.cn' + '/gp/product/'+itemid	
def amazon_price_url(burl):
	'''use original url
	start = url.find(u'/dp/')
	end  = url.find(u'/',start+len(r'/dp/'))
	itemid = url[start:end]
	return 'http://www.amazon.cn' + itemid
	'''
	return burl
def amazon_search(purl):
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
		purl = 'http://www.amazon.cn/gp/twister/ajax/prefetch?parentAsin='+itemid+'&asinList='+itemid
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
			purl = 'http://www.amazon.cn/gp/twister/ajax/prefetch?parentAsin='+itemid+'&asinList='+itemid
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
	# return price
amazon_search(u'http://www.amazon.cn/dp/B003U8YLH2')
# print amazon_brief_url(u'http://www.amazon.cn/Philips%E9%A3%9E%E5%88%A9%E6%B5%A630074%E9%85%B7%E6%8D%B7LED%E5%8F%B0%E7%81%AF%E7%99%BD%E8%89%B2/dp/B00647F8Z0/ref=br_lf_m_396728_1_1_img?ie=UTF8&s=home-improvement&pf_rd_p=82733012&pf_rd_s=center-1&pf_rd_t=1401&pf_rd_i=396728&pf_rd_m=A1AJ19PSB66TGU&pf_rd_r=0HK1KF3W6ZWMAYZF3ZNP&tag=undefined')

def jd_brief_url(url):
	return url
def jd_price_url(burl):
	start = burl.find(u'item.jd.com/')
	end = burl.find(u'.html',start+len(r'/'))
	itemid = burl[start+len(u'item.jd.com/'):end]
	return 'http://p.3.cn/prices/mgets?skuIds=J_'+itemid
def jd_search(purl):
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



def dangdang_brief_url(url):
	start = url.find(u'product_id=')
	if start == -1:
		start = url.find(u'dangdang.com/')
		end = url.find(u'.html',start)
		itemid = url[start+len(u'dangdang.com/'):end]
	else:
		end = url.find(u'&',start+len(u'product_id'))
		itemid = url[start+len(u'product_id='):end]
	return 'http://product.dangdang.com/'+itemid+'.html'
def dangdang_price_url(burl):
	return burl
def dangdang_search(purl):
	try:
		r = requests.get(purl)
	except:
		return None
	start1 = r.text.find(u'id="promo_price"')
	start2 = r.text.find(u'prdJson')
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
				start = r.text.find(u'"color":"',start)
				end = r.text.find(u'"',start+len(u'"color":"'))
				color = r.text[start+len(u'"color":"'):end]
				start = r.text.find(u'"salePrice":"',start)
				end = r.text.find(u'"',start+len(u'"salePrice":"'))
				price = r.text[start+len(u'"salePrice":"'):end]
				print color.encode('utf8')
				print price
	else:
		if start2 == -1:
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
				start = r.text.find(u'"color":"',start)
				end = r.text.find(u'"',start+len(u'"color":"'))
				color = r.text[start+len(u'"color":"'):end]
				start = r.text.find(u'"proid_price":"',start)
				end = r.text.find(u'"',start+len(u'"proid_price":"'))
				price = r.text[start+len(u'"proid_price":"'):end]
				print color.encode('utf8')
				print price


def tmall_brief_url(url):
	start = url.find(u'id=')
	end = url.find(u'&',start)
	if end == -1:
		itemid = url[start+len(u'id='):]
	else:
		itemid = url[start+len(u'id='):end]
	'''get user_id useless
	user_id = ''
	start = url.find(u'user_id=')
	if start != -1:
		end = url.find(u'&',start)
		if end == -1:
			user_id = url[start+len(u'user_id='):]
		else:
			user_id = url[start+len(u'user_id='):end]
	'''

	return "http://detail.tmall.com/item.htm?id="+itemid
def tmall_price_url(burl):
	'''use original url
	start = url.find(u'id=')
	itemid = url[start+len(u'id='):]
	'''
	start = burl.find(u'id=')
	itemid = burl[start+len(u'id='):]
	return 'http://mdskip.taobao.com/core/initItemDetail.htm?itemId='+itemid
def tmall_search(purl):
	start = purl.find(u'itemId=')
	itemid = purl[start+len(u'itemId='):]
	detail_url = 'http://detail.tmall.com/item.htm?id='+itemid
	price_url = 'http://mdskip.taobao.com/core/initItemDetail.htm?itemId='+itemid
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
	oneprice = resultlist[0]['price']
	for i in resultlist:
		if i['price']!= oneprice:
			return resultlist
	return [{'price':oneprice}]


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

# burl = tmall_brief_url(u'http://detail.tmall.com/item.htm?id=12280524326')
# purl = tmall_price_url(burl)
# rest = tmall_search(purl)
# for i in rest:
# 	print i
# 	for j in i:
# 		print i[j]
# print "blue"
# print amazon_search(u"http://www.amazon.cn/dp/B007WQP1ZY")
# print "cha"
# print amazon_search(u"http://www.amazon.cn/dp/B007RSKTXQ")
# print "red"
# print amazon_search(u"http://www.amazon.cn/dp/B007RSKSR8")
# print "xi"
# print amazon_search(u"http://www.amazon.cn/dp/B005EE1G46")
# print "cu"
# print amazon_search(u"http://www.amazon.cn/dp/B005EE1FOW")
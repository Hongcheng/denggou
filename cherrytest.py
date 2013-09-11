import socket
import requests
import json
import re
import logging
import httplib
from collections import OrderedDict
from price import *

print '#############################amazon_search##################################'
ip = getgoodip(u'amazon.cn')
print 'blue'
rest = amazon_search(u'B007WQP1ZY',ip)
for i in rest:
    print i['price']

print 'tea'
rest = amazon_search(u'B007RSKTXQ',ip)
for i in rest:
    print i['price']

print 'red'
rest = amazon_search(u'B007RSKSR8',ip)
for i in rest:
    print i['price']    

print 'black'
rest = amazon_search(u'B007IQ0DZ6',ip)
for i in rest:
    print i['price']    

print 'xi'
rest = amazon_search(u'B005EE1G46',ip)
for i in rest:
    print i['price']    

print 'cu'
rest = amazon_search(u'B005EE1FOW',ip)
for i in rest:
    print i['price']    
print '#############################jd_search##################################'
ip = getgoodip(u'p.3.cn')
print 'jdblack'
rest = jd_search(u'912574',ip)
for i in rest:
    print i['price']    

print 'black'
rest = jd_search(u'584773',ip)
for i in rest:
    print i['price']    

print 'blue'
rest = jd_search(u'613974',ip)
for i in rest:
    print i['price']    

print 'tea'
rest = jd_search(u'613970',ip)
for i in rest:
    print i['price']    

print 'red'
rest = jd_search(u'613972',ip)
for i in rest:
    print i['price']    

print 'xi'
rest = jd_search(u'372416',ip)
for i in rest:
    print i['price']    

print 'cu'
rest = jd_search(u'372412',ip)
for i in rest:
    print i['price']
print '#############################dangdang_search##################################'
ip = getgoodip(u'product.dangdang.com')
rest = dangdang_search(u'1003538107',ip)
for i in rest:
    print i['tag']
    print i['price']    
print '#############################tmall_search##################################'
ip = getgoodip(u'mdskip.taobao.com')
rest = tmall_search(u'13961714037',ip)
for i in rest:
    print i['tag']
    print i['price']    
rest = tmall_search(u'15786958795',ip)
for i in rest:
    print i['tag']
    print i['price']    
rest = tmall_search(u'18177449596',ip)
for i in rest:
    print i['tag']
    print i['price']    
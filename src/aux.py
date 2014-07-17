# -*- coding: utf-8 -*-
__author__ = 'steven'


import urllib2
import urllib
from pyquery import PyQuery as pq
from setting import search_URL

'''
根据给定的关键字确定对应的贴吧链接
'''
def searchTieBa(keyword):

    f = {'ie': 'UTF-8', 'qw' : keyword.encode('utf-8')}
    url = search_URL + str(urllib.urlencode(f))

    try:
        searchPage = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        return 'Fail to login, HTTP error code: '+ e.code

    #with open('search_page.htm', 'w') as out:
    #    out.write(searchPage.read())

    content = searchPage.read()
    doc = pq(content)

    connect = doc.find('a.forum-name')


    if connect != None:
        item = connect[0]
        div = pq(item)
        link = div.attr['href']
        return link.encode('utf-8')
    else:
        return None


'''
验证码的破解参考文档
'''
def crackVerifyCode():
    pass
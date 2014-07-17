# -*- coding: utf8 -*-


__author__ = 'Yifan Steven Yang'


import urllib2
import urllib
import cookielib
import re
import time
import gzip
import random
import json
from setting import *

from StringIO import StringIO
from pyquery import PyQuery as pq
from setting import mouse_crack
from datetime import datetime



'''
登录模块
返回一个 tupple = （[true/false], message）
'''
def do_login(username, password):

    #自动的cookie管理
    cookie_jar2     = cookielib.LWPCookieJar()
    cookie_support2 = urllib2.HTTPCookieProcessor(cookie_jar2)
    opener2         = urllib2.build_opener(cookie_support2, urllib2.HTTPHandler)
    urllib2.install_opener(opener2)

    #这一步貌似是必须的
    try:
        reqReturn = urllib2.urlopen(URL_BAIDU_INDEX)
    except urllib2.HTTPError, e:
        return (False, 'Fail to login, HTTP error code: '+ e.code)

    #获取token, 这里使用指定tpl=pp来获得token，使用其他参数获得的token value会有所不同
    tokenReturn = urllib2.urlopen(URL_BAIDU_TOKEN)
    matchVal = re.search(u'"token" : "(?P<tokenVal>.*?)"',tokenReturn.read())
    tokenVal = matchVal.group('tokenVal')

    print 'token value is ', tokenVal

    #tpl的值还可以是tb，rsa_key也是可以拿到的，但是现在并没有加密也可以登录
    postData = {
        'username' : username,
        'password' : password,
        'u' : 'https://passport.baidu.com/',
        'tpl' : 'pp',
        'token' : tokenVal,
        'staticpage' : 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
        'isPhone' : 'false',
        'charset' : 'UTF-8',
        'callback' : 'parent.bd__pcbs__ra48vi'
        }
    postData = urllib.urlencode(postData)

    #发送登录请求
    loginRequest = urllib2.Request(URL_BAIDU_LOGIN,postData)
    loginRequest.add_header('Accept','text/html,application/xhtml+xml,application/xmlq=0.9,*/*q=0.8')
    loginRequest.add_header('Accept-Encoding','gzip,deflate,sdch')
    loginRequest.add_header('Accept-Language','zh-CN,zhq=0.8')
    loginRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')
    loginRequest.add_header('Content-Type','application/x-www-form-urlencoded')
    sendPost = urllib2.urlopen(loginRequest)

    '''
    返回的文件是gzip格式的，打开下面的代码用以解压并取出其中的跳转连接
    '''
    #buffer = StringIO( sendPost.read())
    #f = gzip.GzipFile(fileobj=buffer)
    #loginResponse = f.read()
    #
    #URL_matcher = re.search(u"encodeURI\('(?P<URL>.*?)'\)", loginResponse)
    #redirectURL = URL_matcher.group('URL')

    if checkLoginStatus(username):
        #将cookie保存出去
        cookie_jar2.save('../cookie/'+username, ignore_discard=True, ignore_expires=True)
        return (True, 'Login in success.')
    else:
        return (False, 'Fail to login in.')

def checkLoginStatus(username):
    '''
    用来检测登录是否成功，检查i百度主页信息
    '''
    check = urllib2.urlopen(INFO_BAIDU)
    content = check.read()

    responseHtml = pq(content)
    connect = responseHtml.find('a.ibx-uc-nick')
    for item in connect:
        p = pq(item)
        if p.text().strip() == username:
            return True
        else:
            return False


'''
发帖模块
'''
def addThread(title, content, tiebaURL):

    testPage = urllib2.urlopen(tiebaURL)
    pageContent = testPage.read()

    #fidPattern = re.compile(u"forumId:'(?P<fidValue>.*?)'")
    #tbsPattern = re.compile(u'PageData\.tbs = \"(?P<tbsValue>.*?)\"')

    #with open('test.html','w') as out:
    #    out.write(pageContent)

    fidMatch = re.search(u"\"id\":([0-9]+),\"is_like\"", pageContent)
    tbsMatch = re.search(u'PageData\.tbs = \"(?P<tbsValue>.*?)\"', pageContent)
    #kwpattern  = re.search(ur'kw=(?P<kwValue>.*?)', str(tiebaURL))

    #字符集要注意
    kwpattern = re.compile(ur'kw=(.*)', re.UNICODE)


    #获得发帖必备的几个参数
    fid = fidMatch.group(1)
    tbs = tbsMatch.group('tbsValue')
    kw = kwpattern.search(tiebaURL).group(1)

    print 'fid is:',fid
    print 'tbs is: ',tbs

    #生成时间戳
    timestamp = str(int(time.time()*1000))
    print 'time stamp is:   ',timestamp

    '''
    mouse_pwd 是JS生成的一串数字，侧才用于机器人检测
    这里的kw是指定的吧名，按需修改
    '''

    threadData = {

        '__type__'  :	'thread',
        'content'	:   content.encode('utf-8'),
        'fid'       :	fid,
        'floor_num' :   '0',
        'ie'        :	'utf-8',
        'kw'        :	kw,
        'mouse_pwd' :   mouse_crack[random.randint(0, len(mouse_crack)) - 1] + timestamp,
        'mouse_pwd_isclick' : '0',
        'mouse_pwd_t'   :   timestamp,
        'rich_text' :	'1',
        'tbs'       :   tbs,
        'tid'       :   '0',
        'title'     :   title.encode('utf-8'),

    }

    headers = {}
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Accept-Encoding'] = 'gzip,deflate,sdch'
    headers['Accept-Language'] = 'en-US,en;q=0.5'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    postData = urllib.urlencode(threadData)

    '''
    返回的文件是gzip格式，注意解压
    '''
    postThread = urllib2.Request(ADD_THREAD, postData,headers)
    send = urllib2.urlopen(postThread)
    buffer = StringIO( send.read())
    f = gzip.GzipFile(fileobj=buffer)
    postResponse = f.read()

    #保存出来可以看到一个类json的文件，其中有获得vcode所需的字串
    #with open('test.html','w') as output:
    #    output.write(postResponse)

    with open('../log/error_code','a') as out:
        out.write('********************' + str(datetime.now()))
        out.write('\n')
        out.write(postResponse)
        out.write('\n')
        out.close()

    #发帖成功
    if "\"err_code\":0" in postResponse:
        return (False, 'Your thread is on the way')
    else:
        #错误代码40为验证码，但是其余的真的不知道什么意思。这里返回的数据被保存在log文件夹中
        if "\"err_code\":40" in postResponse:
            jsonData = json.loads(postResponse)
            vcodeMD5 =  jsonData['data']['vcode']['captcha_vcode_str']
            vcodeURL = urllib2.urlopen(VCODE_IMAGE + vcodeMD5)
            vcodeImage = vcodeURL.read()

            with open('../vcode/vcode_image.png', 'w') as out:
                out.write(vcodeImage)

            return (True, 'Oops~ Verify code is required.')

        else:
            fidMatch = re.search(u"\"err_code\":([0-9]*)", postResponse)
            err_code = fidMatch.group(1)

            return (False, 'Something strange happend. Error code: ' + err_code)

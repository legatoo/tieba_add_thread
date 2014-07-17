 #-*- coding: utf8 -*-

__author__ = 'steven'

from tieba import do_login, addThread
from setting import *
from aux import searchTieBa


if __name__ == '__main__':
    #please set your own username and password
    status, message = do_login(username, password)

    print message

    if searchTieBa(u'易语言管理') != None:

        tiebaURL =  TIEBA_BASEURL + str(searchTieBa(u'易语言管理'))

        print 'Target tieba URL is: ',tiebaURL

        title = u'易语言管理吧是一个可以用来做测试的吧'
        content  = u'所以这是一个好吧！'

        flag, message = addThread(title, content, tiebaURL)

        print message
    else:
        print 'there is no such tieba. '



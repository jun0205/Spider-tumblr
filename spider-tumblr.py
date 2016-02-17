# coding:utf-8
# author:Karblue
# date:2016年2月16日

import os
from threading import Thread

import requests
from pytumblr import TumblrRestClient


API_KEY = "J6UfdqkxWegQ1EymJuotPj4IEXYLK5N922Lr24BzT7p9mRWYgp"
SECRTY_KEY = ""
TOKEN_KEY = ""
TOKEN_SECRTY = ""
TURL = [u'm-ad-dog.tumblr.com', u'fffgh1234.tumblr.com', u'malsexy.tumblr.com', u'dh5874.tumblr.com',
        u'sora--love.tumblr.com', u'smlove2.tumblr.com', u'judge01.tumblr.com', u'moregoin.tumblr.com',
        u'junia-official.tumblr.com', u'jjujjang.tumblr.com', u'sksisiej.tumblr.com', u'olleh.tumblr.com',
        u'tigris8556.tumblr.com', u'yyyysss104.tumblr.com', u'psak1561.tumblr.com', u'seorabeolkim.tumblr.com',
        u'yesdaejeon.tumblr.com', u'cxb841006.tumblr.com', u'nonononotme.tumblr.com', u'xxxsgifttous.tumblr.com',
        u'nonononotme.tumblr.com', u'xxxsgifttous.tumblr.com', u'sex9988.tumblr.com', u'josephings.tumblr.com',
        u'albertjj.tumblr.com', u'o-eroero.tumblr.com', u'asd0plm.tumblr.com', u'erokawa-ga-suki.tumblr.com',
        u'lackironaquarius.tumblr.com', u'luckycobain.tumblr.com', u'leehyunhoo.tumblr.com', u'huangyuchi.tumblr.com',
        u'tvrosur.tumblr.com', u'ddtskullbreaker.tumblr.com', u'leechongho.tumblr.com', u'ggn321.tumblr.com',
        u'kkkrrrjjj.tumblr.com', u'kimms66hd.tumblr.com', u'ku777.tumblr.com', u'somatan.tumblr.com',
        u'ku777.tumblr.com', u'somatan.tumblr.com', u'katana-san.tumblr.com', u'jundaegi.tumblr.com',
        u'uhyohyo.tumblr.com', u'morethan3cm.tumblr.com', u'kanakuni.tumblr.com', u'smile67yt.tumblr.com',
        u'tumbtter.tumblr.com', u'seif-sexy-photo.tumblr.com', u'rhdwh.tumblr.com', u'hughqi.tumblr.com',
        u'kakakaka101.tumblr.com', u'blueeyes79.tumblr.com', u'yipkinning.tumblr.com', u'iishrek.tumblr.com',
        u'kong2010.tumblr.com', u'zzaini123.tumblr.com', u'fuligongxiang.tumblr.com', u'sa703.tumblr.com',
        u'zzaini123.tumblr.com', u'fuligongxiang.tumblr.com', u'sa703.tumblr.com', u'beautifulgirlbody.tumblr.com',
        u'yiriyise.tumblr.com', u'dainifei.tumblr.com']

STOREPATH = "tumblr/"

# 获取关注的人列表
def getFollowings():
    _retVal = []
    client = TumblrRestClient(API_KEY, SECRTY_KEY, TOKEN_KEY, TOKEN_SECRTY)
    _followings = client.following(limit=1)
    if "meta" in _followings:
        print "Server Return ERROR : %s,code :%s" % (_followings["msg"], _followings["status"])
        return

    # 先确定总关注数
    _total = _followings["total_blogs"]
    _flBlogArr = []
    for offset in xrange(0, _total / 20 + 1):
        _followings = client.following(limit=20, offset=offset * 20)
        for ele in _followings["blogs"]:
            _flBlogArr.append(ele["uuid"])

        _retVal = _flBlogArr

    return _retVal


# 多线程获取数据
def getData(client, url, type, resKey):
    _resource = client.posts(url, type=type)
    if "meta" in _resource:
        _errData = _resource["meta"]
        print "URL:%s,Server Return ERROR : [%s], code :%s" % (url, _errData["msg"], _errData["status"])
        return

    #确定总post数
    _total = _resource["total_posts"]
    for offset in xrange(0, _total / 20 + 1):
        _resource = client.posts(url, type=type, limit=20, offset=offset * 20)
        #获取post的数据
        for posts in _resource["posts"]:
            #获取资源
            for ele in posts[resKey]:
                _resURL = ele["original_size"]["url"]
                _fileName = _resURL.split("/")[-1]
                print "get Resource:%s" % _resURL
                try:
                    _rawData = requests.get(_resURL, stream=True).content
                    with file(STOREPATH + _fileName, "wb") as _rFile:
                        _rFile.write(_rawData)
                except Exception, e:
                    print "Spider Exception:%s" % str(e)


#获取资源
def getResource(filter='photo', resKey="photos"):
    client = TumblrRestClient(API_KEY)
    _thArr = []
    for url in TURL:
        print "start Spider-URL:%s" % url
        _thread = Thread(target=getData, args=[client, url, filter, resKey])
        _thread.start()
        _thArr.append(_thread)

    for th in _thArr:
        th.join()

    print "all Spider finish ..."


if __name__ == "__main__":
    #初始化资源目录
    if not os.path.exists(STOREPATH):
        os.mkdir(STOREPATH)

    _flArr = getResource()
    raw_input()



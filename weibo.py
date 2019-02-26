# encoding: utf-8
# file:post_weibo.py
import json
import urllib
import urllib.request
import time
import requests


def post_weibo(weibo_text, pic_uri=None):
    url_post_a_text = "https://api.weibo.com/2/statuses/share.json"
    ACCESS_TOKEN = ""
    playload = {
        "access_token": ACCESS_TOKEN,
        "status": weibo_text
    }
    if pic_uri is None:
        r = requests.post(url_post_a_text, data=playload, verify=False)
        print(r.text)

    else:
        files = {"pic": open(pic_uri, "rb")}
        r = requests.post(url_post_a_text, data=playload, files=files, verify=False)
        print(r.text)

def post_myweibo(weibo_text, pic_uri=None):
    url_post_a_text = "https://api.weibo.com/2/statuses/update.json"
    ACCESS_TOKEN = ""
    weibo_text = weibo_text + time.strftime(u'[来自微信,更新时间:%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    playload = {
        "access_token": ACCESS_TOKEN,
        "status": weibo_text.encode('unicode')
    }
    if pic_uri is None:
        r = requests.post(url_post_a_text, data=playload, verify=False)
        print(r.text)

    else:
        files = {"pic": open(pic_uri, "rb")}
        r = requests.post(url_post_a_text, data=playload, files=files, verify=False)

def get_jokes():
    """获得笑话"""
    API_KEY = "填写你的百度APIKEY"
    url = 'http://apis.baidu.com/showapi_open_bus/showapi_joke/joke_text?page=1'
    headers = {"apikey": API_KEY}
    r = requests.get(url, headers=headers, verify=False)
    jokes = []
    # import sys, urllib, urllib.request
    # req = urllib.request.Request(url)
    # req.add_header("apikey", API_KEY)
    # resp = urllib.request.urlopen(req)
    # content = resp.read()
    content = r.text
    if (content):
        print(type(content))
        js_cont = json.loads(content)
        for i in js_cont['showapi_res_body']['contentlist']:
            jokes.append((i['text'], i['ct']))
    return jokes


def get_one_info():
    """抓取ONE-APP网页并提取信息"""
    from bs4 import BeautifulSoup

    URL_ONE = "http://wufazhuce.com/"
    r = requests.get(URL_ONE, verify=False)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    info = {}
    for i in soup.find_all("div", "item"):
        info["pic_url"] = i.img["src"]
        for j in i.find_all("a"):
            info["text"] = j.string
        info["date"] = []
        for j in i.find_all("p"):
            info["date"].append(j.string)
        for j in i.find_all("div", "fp-one-imagen-footer"):
            info["pic_info"] = j.string.strip()
    return info


def get_words_info(index):
    """获得笑话"""
    # API_KEY = "填写你的百度APIKEY"
    myurl = 'http://apis.haoservice.com/lifeservice/JingDianYulu/?key=8acd60f7c6a24ee79d11e9c65cd6fab8&typeId=13&pageIndex=' + str(
        index) + '&pageSize=15&paybyvas=false'
    # headers = {"apikey": API_KEY}
    r = requests.get(myurl)
    words = []
    # import sys, urllib, urllib.request
    # req = urllib.request.Request(url)
    # req.add_header("apikey", API_KEY)
    # resp = urllib.request.urlopen(req)
    # content = resp.read()
    content = r.text
    if (content):
        print(type(content))
        js_cont = json.loads(content)
        words = js_cont[u'result'][u'List'][index]['Content']
    return words

def result(queryStr,userid):
    loginUrl = 'http://www.tuling123.com/openapi/api'
    key = '3798004d74c9426d90e28d0fbb7ecebc'
    postdata = urllib.parse.urlencode({
        'key': key,
        'info': queryStr,
        'userid': userid
    })
    req = urllib.request.Request(url=loginUrl,data=postdata)
    result = urllib.request.urlopen(req).read()
    hjson = json.loads(result)
    print(hjson)
    code = hjson['code']
    if code == 100000:
        recontent = hjson['text']
    elif code == 200000:
        recontent = hjson['text'] + hjson['url']
    elif code == 302000:
        recontent = hjson['text'] + hjson['list'][0]['info'] + hjson['list'][0]['detailurl']
    elif code == 308000:
        recontent = hjson['text'] + hjson['list'][0]['info'] + hjson['list'][0]['detailurl']
    else:
        recontent = '这个消息人类不能回答，额。。。对了，我不是人类，也不能识别。。。很尴尬'
    words = recontent + time.strftime(u'[更新时间：%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    return words

if __name__ == "__main__":
    import time

    index = 0
    while True:
        try:
            info = get_one_info()
            pic_name = "pic.png"
            web_text = info["text"] + info["date"][1] + u"," + info["date"][2] + u"[图]" + info["pic_info"]
            # print requests.get(info["pic_url"], verify=False).content
            with open(pic_name, "wb") as pic:
                # 由于直接通过图片url的形式发表微博的API接口需要申请
                # 所以选择先把图片保存成图片文件再发布
                # 当然也可以使用StringIO不保存直接编码进POST请求

                pic.write(requests.get(info["pic_url"], verify=False).content)
                pic.close()
            time.sleep(10)
            post_weibo(weibo_text=web_text, pic_uri=pic_name)
            print("Done")
            # time.sleep(10)
        except Exception as e:
            print(e)

        try:
            words = result("南京天气","12345678")
            post_weibo(words)
        except Exception as e:
            print(e)

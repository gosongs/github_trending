# coding:utf-8

import datetime
import time
import requests
import codecs
import os
from pyquery import PyQuery as pq
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# 需要抓取的语言
LANG_LIST = [
    'all',  # all language
    'unknown',  # unknown language
    'c++',
    'css',
    'coffeescript',
    'html',
    'javascript',
    'python',
    'vue'
]

# ua
HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":
    "gzip, deflate, br",
    "Accept-Language":
    "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"
}


# 抓取信息
def fetch_trending(lang, filename):
    print('fetch {lang} ...'.format(lang=lang))
    lang2 = '' if lang == 'all' else lang  # 传空表示所有语言

    url = 'https://github.com/trending/{lang}'.format(lang=lang2)
    r = requests.get(url, headers=HEADERS)

    with codecs.open(lang + '/' + filename, "a", "utf-8") as f:
        if r.status_code == 200:
            d = pq(r.content)
            items = d('ol.repo-list li')
            for item in items:
                i = pq(item)
                name = i("h3 a").text()
                link = 'https://github.com' + i("h3 a").attr('href')
                desc = i(".py-1 p").text()
                # info['total_star'] =
                f.write(u"* [{name}]({link}):{desc}\n".format(
                    name=name, link=link, desc=desc))
        else:
            pass


# 创建md
def createMd(lang, strdate, filename):
    with open(lang + '/' + filename, 'w') as f:
        f.write("## " + strdate + "\n\n")


# 获取所有语言
def get_all_lang():
    lang_urls = []

    url = 'https://github.com/trending/vue'
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        d = pq(r.content)
        langs = d(
            '.col-md-3 .select-menu-modal-holder .select-menu-modal .select-menu-list a'
        )
        for l in langs:
            lang_url = pq(l).attr('href')
            lang_urls.append(lang_url.split('/')[-1:][0])
    else:
        pass
    return lang_urls


# 入口
def fire(langs):
    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = '{date}.md'.format(date=strdate)

    for lang in langs:
        if os.path.exists(lang) is False:
            os.mkdir(lang)
        createMd(lang, strdate, filename)
        # print(filename)  # 2017-9-01.md

        fetch_trending(lang, filename)


if __name__ == '__main__':
    langs = get_all_lang()  # 抓取所有语言

    # langs = LANG_LIST # 抓取自定义语言
    fire(langs)
    time.sleep(24 * 60 * 60)
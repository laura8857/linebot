# -*- coding: utf-8 -*-
import json
import time
import requests
from bs4 import BeautifulSoup
import random


PTT_URL = 'https://www.ptt.cc'


def get_web_page(url):
    time.sleep(0.5)  # 每次爬取前暫停 0.5 秒以免被 PTT 網站判定為大量惡意爬取
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return get_articles(resp.text)


def get_articles(dom):
    no_reply = ["沒啥有趣的","今天休假","小柴我不想說","罷工罷工"]
    soup = BeautifulSoup(dom, 'html.parser')

    # 取得上一頁的連結
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = ''  # 儲存取得的文章資料
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        # print("_______________________")
        # print(d.find('div', 'nrec').string)


        if d.find('span'):
            if d.find('a'):
                if d.find('div','nrec').string =='爆':
                    print(d.find('div', 'nrec').string)

                    # 取得文章連結及標題
                    if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                        # print('href')
                        href = PTT_URL + d.find('a')['href']
                        title = d.find('a').string
                        articles += title +'\n' + href +'\n'

                else:
                    try:
                        pushcount = int(d.find('div', 'nrec').string)
                    except:
                        pushcount = 0
                    if pushcount>20:
                        # print(d.find('div', 'nrec').string)
                        href = PTT_URL +d.find('a')['href']
                        title = d.find('a').string
                        articles += title + '\n' + href+'\n'

    if len(articles)>0:
        return articles
    else:
        count = random.randint(0,3)
        # print(count)
        return no_reply[count]












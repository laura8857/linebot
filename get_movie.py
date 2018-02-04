# -*- coding: utf-8 -*-
# @Time    : 2018/1/30 下午17:22
# @Author  : Weiting
# @File    : get_movie.py
# @Software: PyCharm Community Edition
import json
import time
import requests
import datetime
from bs4 import BeautifulSoup




def get_web_page_movie(url):
    time.sleep(0.5)  # 每次爬取前暫停 0.5 秒以免被判定為大量惡意爬取
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def get_top_movie(dom):

    with open('movie.json', 'r') as reader:
        last_data = json.loads(reader.read())

    # last_date =datetime.datetime.strptime(last_data[0]['date'], '%Y-%m-%d')
    last_date_list = last_data[0]['last_date'].split("-")
    last_date = datetime.date(
        int(last_date_list[0]),
        int(last_date_list[1]),
        int(last_date_list[2])
    )

    datePosted = datetime.date.today()

    if (datePosted-last_date).days <=0:
        return last_data
    else:
        soup = BeautifulSoup(dom, 'html.parser')


        top_movie = []  # 儲存取得的文章資料
        # print(soup)
        divs = soup.find_all('',{'class' : "ranking_list_r"})
        # print(len(divs))
        for d in divs:
            # print("_______________________")
            # print(d)

            movies = d.find_all('',{'class' : "gabtn"})
            # print(len(movies))
            for item in movies:
                print("-"*20)
                # print(item)
                href = item['href']
                area = item['data-ga'].split("'")[3]
                movie = item['data-ga'].split("'")[5]
                # print(type,movie,href)

                movie_page = get_web_page_movie(href)
                if movie_page:
                    length, date, style, actor, score = get_movie_detail(movie_page)
                    top_movie.append(
                        {
                        'movie': movie,
                        'url':href,
                        'area':area,
                        'length':length,
                        'date':date,
                        'style':style,
                        # 'actor':actor,
                        'score':score,
                        'last_date':str(datePosted)
                    })
        print(top_movie)
        with open('movie.json', 'w', encoding='utf-8') as f:
            json.dump(top_movie, f, indent=2, sort_keys=True, ensure_ascii=False)
        return top_movie


def get_movie_detail(dom):
    soup = BeautifulSoup(dom, 'html.parser')

    details = []  # 儲存取得的文章資料
    # print(soup)

    # movie info to get length and date
    divs = soup.find('div',{'class':"movie_intro_info_r"})
    # print(divs)
    info =divs.find_all('span')
    # print(info)
    for item in info:
        item_str = str(item.string)

        if "片　　長" in item_str:
            length = item_str[item_str.find("：")+1:]
        if "上映日期" in item_str:
            date= item_str[item_str.find("：") + 1:]

    # movie info to get style and actor
    movie_style_all = divs.find_all('',{'class':'gabtn'})
    # print(movie_style_all)
    style =[]
    actor =[]

    for i in movie_style_all:
        stylelist = i["data-ga"].split("'")
        # print(stylelist)
        if stylelist[3] =="電影介紹_類型icon":
            # print(stylelist[5])
            style.append(stylelist[5])
        elif stylelist[3] =="電影介紹_演員資訊":
            # print(i.string)
            actor.append(i.string)

    score = soup.find("div",{"class":"score_num count"}).string
    # print(score)

    # print(length,date,style,actor,score)

    return length,date,style,actor,score
if __name__ == "__main__":
    current_page = get_web_page_movie('https://movies.yahoo.com.tw/')
    if current_page:
        get_top_movie(current_page)

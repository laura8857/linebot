# -*- coding: utf-8 -*-
from flask import Flask, request, abort
import random
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction,
    URITemplateAction, ImageCarouselTemplate, ImageCarouselColumn, PostbackTemplateAction)
from linebot import LineBotApi
import json
import re
import dateutil.parser as dparser
import time

from crawl import get_web_page
from conf import configuration
from get_train import get_train
from get_movie import get_web_page_movie,get_top_movie


app = Flask(__name__)

line_bot_api = LineBotApi(configuration['Channel_Access_Token'])
handler = WebhookHandler(configuration['Channel_Secret'])

url = [
    'https://instagram.ftpe8-2.fna.fbcdn.net/vp/54c35607733cc001ceb776e367565e48/5AEB00CF/t51.2885-15/s640x640/sh0.08/'
    'e35/26321899_199945963917671_955816564811104256_n.jpg',
    'https://instagram.ftpe8-2.fna.fbcdn.net/vp/0c67d9e88135c9e399f10d861309a7c8/5B032658/t51.2885-15/s640x640/sh0.08/'
    'e35/26186863_369190093553204_4541536051293847552_n.jpg',
    'https://instagram.ftpe8-2.fna.fbcdn.net/vp/6c304f63c1e0cec5a2432104cdca4dbe/5B20C137/t51.2885-15/e35/26180651_87'
    '7212995777575_4765950776864407552_n.jpg',
    'https://instagram.ftpe8-2.fna.fbcdn.net/vp/5bf1c4926ccaaad57aef6e60eb957bd4/5B251E37/t51.2885-15/s640x640/sh0.08/'
    'e35/24125373_419084268494871_8757244398770585600_n.jpg',
    'https://instagram.ftpe8-2.fna.fbcdn.net/vp/044dc1dfdb420d48a037e82366050352/5AF1ED06/t51.2885-15/s640x640/sh0.08/'
    'e35/c0.2.1080.1080/23594889_159577694785903_6296751252294336512_n.jpg'
]

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
        # events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)

    if "火車" in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請輸入:起站/終站/年/月/日' + '\n(例如：台北/台東/2018/1/1)'))
        return 0

    pattern = re.compile(r'^([0-9]{4})[./]{1}([0-9]{1,2})[./]{1}([0-9]{1,2})$')
    test = None
    try:
        test = dparser.parse(event.message.text, fuzzy=True)
        if test is not None:
            message = event.message.text
            if len(message.split("/")) ==5:
                date = message.split("/")[2]+'/'+message.split("/")[3]+'/'+message.split("/")[4]
                content = want_train(message.split("/")[0],message.split("/")[1],date)
            else:
                content = "請輸入正確的查詢格式\n起站/終站/年/月/日\n(例如：台北/台東/2018/1/1)"
            print(content)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0

    except Exception:
        print(Exception)

    if event.message.text == "網球":
        content = tennis()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0


    elif event.message.text == "笨事一籮筐":
        content = stupidclown()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))

        return 0

    elif event.message.text == "柴photo":
        num = random.randint(0,4)
        image_message = ImageSendMessage(
            original_content_url=url[num],
            preview_image_url=url[num]
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0
    elif event.message.text =="今天吃什麼":
        content = today_eat()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))

        return 0
    elif event.message.text=="電影大小事":
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://instagram.ftpe8-3.fna.fbcdn.net/vp/4d14673bbc73f804285d8587fee67444/5B08EF3D/t51.2885-15/e15/10852686_1609466372614592_1128590266_n.jpg',
                title='柴看看',
                text='黑柴電影閒聊',
                actions=[
                    MessageTemplateAction(
                        label='天龍黑柴看電影',
                        text='台北票房榜',
                    ),
                    MessageTemplateAction(
                        label='美國黑柴see movie',
                        text='全美票房榜',
                    ),
                    MessageTemplateAction(
                        label='黑柴的預告',
                        text='預告片排行榜',
                    ),
                    # MessageTemplateAction(
                    #     label='黑柴的餓了',
                    #     text='今天吃什麼',
                    # ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
        return 0

    elif event.message.text == "台北票房榜":
        content = want_movie('台北票房榜')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))

        return 0
    elif event.message.text == "全美票房榜":
        content = want_movie('全美票房榜')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))

        return 0
    elif event.message.text == "預告片排行榜":
        content = want_movie('預告片排行榜')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))

        return 0

    else:
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://instagram.ftpe8-2.fna.fbcdn.net/vp/b9523c62d15bd54203e5f296e341a490/5B00598'
                                    '4/t51.2885-15/s480x480/e35/26867678_805458326322652_4714169701956059136_n.jpg',
                title='柴看看',
                text='黑柴的聊天室',
                actions=[
                    MessageTemplateAction(
                        label='黑柴看網球',
                        text='網球',
                    ),
                    MessageTemplateAction(
                        label='黑柴看笨事',
                        text='笨事一籮筐',
                    ),
                    MessageTemplateAction(
                        label='黑柴的自戀',
                        text='柴photo',
                    ),
                    MessageTemplateAction(
                        label='黑柴的餓了',
                        text='今天吃什麼',
                    ),

                    # URITemplateAction(
                    #     label='黑柴滴ig',
                    #     uri='https://www.instagram.com/mame.saku/'
                    # )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
        return 0

def tennis():
    target_url = 'https://www.ptt.cc/bbs/Tennis/index.html'
    print('Start tennis....')

    content = get_web_page(target_url)
    print(content)
    return content

def stupidclown():
    target_url = 'https://www.ptt.cc/bbs/stupidclown/index.html'
    print('Start stupidclown....')

    content = get_web_page(target_url)
    print(content)
    return content

def today_eat():
    with open('eatwhat.json', 'r') as reader:
        jf = json.loads(reader.read())
        dict = jf['eatwhat']
        random_seed = random.randrange(0, len(dict))
        print(random_seed, dict[random_seed], dict[random_seed]['address'], dict[random_seed]['storeName'])
        url ='https://www.google.com.tw/maps/place/'
        url+=dict[random_seed]['address']

        content = dict[random_seed]['storeName'] +'\n'+url+'\n'

        return content

def want_train(origin,destination,date):
    isformat,train_list = get_train(origin,destination,date)

    if isformat:
        content = origin+'-'+destination+' 火車時刻表\n'
        content += '-'*25 +'\n'

        for item in train_list:
            content +=\
                "火車編號:"+ item['train_NO']+'\n火車種類:'+item['train_type']+'\n起站-終站:'+item['origin_station']+'-'\
                +item['destination_station']+'\n起站出發時間:'+item['origin_departure_time']+'\n終站抵達時間:'\
                +item['destination_arrival_time']+'\n'+'-'*25+'\n'
    else:
        content = train_list

    return content

def want_movie(area):
    content_taipei ='台北票房榜\n'+'-'*30
    content_america ='全美票房榜\n'+'-'*30
    content_not_on ='預告片榜\n'+'-'*30

    current_page = None
    current_page = get_web_page_movie('https://movies.yahoo.com.tw/')

    if current_page:
        top_movie = get_top_movie(current_page)


        for movie in top_movie:

                if movie['area'] =='電影排行榜_台北票房榜':
                    content_taipei +=movie['movie']+'\n電影類別:'

                    for style in movie['style']:
                        content_taipei+=style+','
                    content_taipei += '\n上映時間:' + movie['date'] + '\n電影長度:' + movie['length']+'\n評分:'+movie['score']+'/5'+'\n'

                    # for actor in movie['actor']:
                    #     content_taipei +=actor+','
                    content_taipei +='\n'+movie['url']+'\n'+'-'*25+'\n'
                elif movie['area'] =='電影排行榜_全美票房榜':
                    content_america += movie['movie'] + '\n電影類別:'

                    for style in movie['style']:
                        content_america += style + ','
                    content_america += '\n上映時間:' + movie['date'] + '\n電影長度:' + movie['length'] + '\n評分:' + movie['score']+ '/5' + '\n'

                    # for actor in movie['actor']:
                    #     content_america += actor + ','
                    content_america += '\n' + movie['url']+'\n'+'-'*25+'\n'
                elif movie['area'] =='電影排行榜_預告片榜':
                    content_not_on += movie['movie'] + '\n電影類別:'

                    for style in movie['style']:
                        content_not_on += style + ','
                    content_not_on += '\n上映時間:' + movie['date'] + '\n電影長度:' + movie['length'] + '\n評分:' + movie['score']+ '/5' + '\n'

                    # for actor in movie['actor']:
                    #     content_not_on += actor + ','
                    content_not_on += '\n' + movie['url']+'\n'+'-'*25+'\n'
                else:
                    content_taipei += 'Something Error.'
                    content_america = 'Something Error.'
                    content_not_on = 'Something Error.'



    if area == "台北票房榜":
        return content_taipei
    elif area =="全美票房榜":
        return content_america
    elif area == "預告片排行榜":
        return content_not_on
    else:
        return "Something Error."



if __name__ == "__main__":
    app.run()
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
    URITemplateAction)
from linebot import LineBotApi
import json


from crawl import get_web_page
from conf import configuration



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
    except InvalidSignatureError:
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
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

def tennis():
    target_url = 'https://www.ptt.cc/bbs/Tennis/index.html'
    print('Start tesnnis....')

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


if __name__ == "__main__":
    app.run()
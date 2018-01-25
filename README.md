# linebot
linebot

柴看看 line

1.從ptt爬文 回傳網球熱門文章
2.從ptt爬文 回傳笨版文章
3.取json random出data，回傳餐廳
4.回傳圖片


參考：[https://becoder.org/python-flask-requests-line-bot-api/](https://becoder.org/python-flask-requests-line-bot-api/)

事前準備：

Python Flask

Ngrok ([教學連結](https://onmyvie.tumblr.com/post/170107008915/ngrok-%E8%AE%93%E6%9C%AC%E6%A9%9F%E4%B9%9F%E5%8F%AF%E4%BB%A5%E9%96%8B%E7%99%BC-webhook-%E5%85%8D%E9%83%A8%E7%BD%B2%E7%92%B0%E5%A2%83%E7%9A%84%E7%A5%9E%E5%99%A8))

line@ account

1.申請line@
![image](https://78.media.tumblr.com/79df4a0387f95b14a180f4bbaf642882/tumblr_inline_p33q14EA1e1uiyw8m_540.jpg)![image](https://78.media.tumblr.com/94411550ad70557fb181a158bddbe5a6/tumblr_inline_p33q4av1Cq1uiyw8m_540.jpg)

**
**

進入line manager後，進入帳號設定--&gt;messager api 設定，點擊開始api
![image](https://78.media.tumblr.com/dc55e06b5a5b7fe9e9c226959e96d226/tumblr_inline_p33qmh9NCt1uiyw8m_540.jpg)

要將webhook傳訊設定為允許，但要去line developers設定
![image](https://78.media.tumblr.com/ff59d7f0642ad7f54559b2b2e1478d14/tumblr_inline_p33qm7kmtT1uiyw8m_540.jpg)![image](https://78.media.tumblr.com/a344e1b68a476d511e0618458590c86d/tumblr_inline_p33qqatQvt1uiyw8m_540.jpg)

此時，在本頁，要記下很重要了兩個東西

*   Channel secret

*   Channel access token (long-lived)&nbsp; **如果是空白，點擊issue**

2.Ngrok 設定

因為Line Bot 需要 SSL憑證 ( https )，我使用是Ngrok

ngrok會給一組隨機的httpxxxxx &amp; https xxxxxx 對應到本機localhost:xxxx 啟的server，讓外部的網站能夠直接連接到localhost，節省掉開發的時間

[Ngrok的操作連結在此](https://onmyvie.tumblr.com/post/170107008915/ngrok-%E8%AE%93%E6%9C%AC%E6%A9%9F%E4%B9%9F%E5%8F%AF%E4%BB%A5%E9%96%8B%E7%99%BC-webhook-%E5%85%8D%E9%83%A8%E7%BD%B2%E7%92%B0%E5%A2%83%E7%9A%84%E7%A5%9E%E5%99%A8)

將Nogrol的網址設定跟localhost同個post，我這邊是設定5000(Flask預設)，複製nogrok產生的https的連結
連結後面要加上/callback
![image](https://78.media.tumblr.com/1276fe74e8231c99eb5fbd30f3283b66/tumblr_inline_p33tob7M4K1uiyw8m_540.jpg)
貼在line&nbsp;developers設定頁面
![image](https://78.media.tumblr.com/553d44b12aaf5082cf8fd8302f49d5d1/tumblr_inline_p33r49w3Dk1uiyw8m_540.jpg)

暫時不用管verify後是否會出現錯誤

3.執行Sample code

使用的是python 的flask

先使用[官方的sample code](https://github.com/line/line-bot-sdk-python)
<pre>from flask import Flask, request, abort

from linebot import (
 &nbsp; &nbsp;LineBotApi, WebhookHandler
)
from linebot.exceptions import (
 &nbsp; &nbsp;InvalidSignatureError
)
from linebot.models import (
 &nbsp; &nbsp;MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

@app.route("/callback", methods=['POST'])
def callback():
 &nbsp; &nbsp;# get X-Line-Signature header value
 &nbsp; &nbsp;signature = request.headers['X-Line-Signature']

 &nbsp; &nbsp;# get request body as text
 &nbsp; &nbsp;body = request.get_data(as_text=True)
 &nbsp; &nbsp;app.logger.info("Request body: " + body)

 &nbsp; &nbsp;# handle webhook body
 &nbsp; &nbsp;try:
 &nbsp; &nbsp; &nbsp; &nbsp;handler.handle(body, signature)
 &nbsp; &nbsp;except InvalidSignatureError:
 &nbsp; &nbsp; &nbsp; &nbsp;abort(400)

 &nbsp; &nbsp;return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
 &nbsp; &nbsp;line_bot_api.reply_message(
 &nbsp; &nbsp; &nbsp; &nbsp;event.reply_token,
 &nbsp; &nbsp; &nbsp; &nbsp;TextSendMessage(text=event.message.text))

if __name__ == "__main__":
 &nbsp; &nbsp;app.run()</pre>

**記得YOUR_CHANNEL_ACCESS_TOKEN要設定剛剛在line manager的Channel access token (long-lived)，YOUR_CHANNEL_SECRET則是要設定為Channel secret！**

4.執行sample.py

該sample code的內容就是 你打什麼字，機器人就回什麼
![image](https://78.media.tumblr.com/31c8a79630357c6c5ba3cd75a3bef5f9/tumblr_inline_p33ri2IURf1uiyw8m_540.png)

至於，感謝您那一段是預設機器人回傳訊息，可以去line manager，訊息--&gt;自動回傳訊息，刪掉預設訊息

## **如果機器人有回覆你打的字，代表你成功了一大半！**

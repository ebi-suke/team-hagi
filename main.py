from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, FlexSendMessage,CarouselContainer,BubbleContainer
from image_change import mosic_change, art_change, dot_change, illust_change
from output import output_method
import json
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

# リプライIDとイベントIDをテキストとして保存するためのやつ
work = {}
path_w1 = 'saveid.txt'
path_w2 = 'savereply.txt'
app = Flask(__name__)


# トークン情報もろもろ
YOUR_CHANNEL_ACCESS_TOKEN = "pJYr3wFv0fPHgCL0EJgKPjBkIjbg11mXqqkUaD70hmAAeMpcCfhFkuIztKg/xcUbu/E/dvzp3NhjTKqgKMY5zinBwzh+I9qyy/lrb42WbYh4ZXR/5rMBwfA8YzKSFzqrdrvBczvhlArg3ef9hPmh+wdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "3449c7705c5a5179752386f7e2717ebb"
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
FQDN = "https://team-hagi.herokuapp.com/"
cascade_path = "haarcascade_frontalface_default.xml"
cascade_eye_path = "haarcascade_eye.xml"




@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    print("Request body" + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# テキストデータを受け取ったときに走るやつ。
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=event.message.text),])
    print("取得イヴェント:{}".format(event))
    print("取得イヴェントメッセージID:{}".format(event.message.id))
    print("リプライトークン：{}".format(event.reply_token))
    print("------リプライ型------")
    print(type(event.reply_token))

    #モザイク(目)
    if event.message.text == ">>おめめモザイク":
        print("通過: {}".format(event.message.text))
        with open(path_w1) as f:
            work = f.read()
        with open(path_w2) as f2:
            work1 = f2.read()
        #line_bot_api.reply_message(event.reply_token,[TextSendMessage(text="目のモザイク処理をしています..."),])
        output_method.handle_send_message(work,event.reply_token)

    #線画
    elif event.message.text == ">>線画風":
        print("通過: {}".format(event.message.text))
        with open(path_w1) as f:
            work = f.read()
        with open(path_w2) as f2:
            work1 = f2.read()
        #line_bot_api.reply_message(event.reply_token,[TextSendMessage(text="画像を線画化しています..."),])
        output_method.handle_send_message(work,event.reply_token)

    #イラスト風
    elif event.message.text == ">>イラスト風":
        print("通過: {}".format(event.message.text))
        with open(path_w1) as f:
            work = f.read()
        with open(path_w2) as f2:
            work1 = f2.read()
        #line_bot_api.reply_message(event.reply_token,[TextSendMessage(text="イラスト風に変更しています..."),])
        output_method.handle_send_message(work,event.reply_token)

    #ドット絵
    elif event.message.text == ">>ドット絵風":
        print("通過: {}".format(event.message.text))
        with open(path_w1) as f:
            work = f.read()
        with open(path_w2) as f2:
            work1 = f2.read()
        #line_bot_api.reply_message(event.reply_token,[TextSendMessage(text="ドット絵風に変更しています..."),])
        output_method.handle_send_message(work,event.reply_token)

def text_save_id(work):
    s = work
    print("取得イヴェントメッセージIDDDDDDDDDDDDDDDD_text_saveID:{}".format(work))
    with open(path_w1, mode='w') as f:
        f.write(s)

def text_save_reply(work):
    s = work
    print("取得イヴェントメッセージIDDDDDDDDDDDDDDDD_text_saveReply:{}".format(work))
    with open(path_w2, mode='w') as f:
        f.write(s)


def carousel(event):
    work = event.message.id
    reply_work = event.reply_token
    print("取得イヴェントメッセージIDDDDDDDDDDDDDDDD:{}".format(work))
    text_save_id(work)
    text_save_reply(reply_work)

    # Json展開
    json_open = open('carousel.json', 'r')
    json_data = json.load(json_open)

    carousel_msg = FlexSendMessage(alt_text="test", contents=json_data)

    if event.reply_token == "00000000000000000000000000000000":
        return
    if event.reply_token == "ffffffffffffffffffffffffffffffff":
        return

    line_bot_api.reply_message(event.reply_token, messages=carousel_msg)

#画像受信後処理
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    print("メッセージID")
    print(event.message.id)

    message_content = line_bot_api.get_message_content(event.message.id)

    if not os.path.exists('static'):
        os.mkdir('static/')
    with open("static/" + event.message.id + ".jpg", "wb") as f:
        f.write(message_content.content)

    carousel(event)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

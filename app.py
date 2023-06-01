from flask import Flask, request
import json
import time
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import openai
from bardapi import Bard
import numpy

app = Flask(__name__)

@app.route('/', methods=['POST'])
def linebot():
    user_input = request.get_data(as_text=True)
    # msg = json_data['events'][0]['message']['text']
    acccess_token = 'YOUR_ACCESS_TOKEN'
    json_data = json.loads(user_input)
    secret = 'YOUR_SECRET'
    line_bot_api = LineBotApi(acccess_token)
    handler = WebhookHandler(secret)
    signature = request.headers['X-Line-Signature']
    handler.handle(user_input, signature)
    tk = json_data['events'][0]['replyToken']
    st = time.time()
    try:
        type = json_data['events'][0]['message']['type']
        if type == "text":
            user_msg = json_data['events'][0]['message']['text']
            print(f'{user_msg}')
            # Chat-GPT
            if user_msg[0:9]=='Chat-GPT:':
                openai.organization = 'OPENAI.ORGANIZATION'
                openai.api_key = 'OPENAI_API_KEY'
                model = user_msg[0:8]
                user_question = user_msg[9:]
                completion = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo-0301',
                    messages=[
                        {
                            'role': 'user', 'content': f'{user_question}#zh-tw'
                        }
                    ]
                )
                respond = completion.choices[0].message['content']
                et = time.time()
                line_bot_api.reply_message(tk, TextSendMessage(f'你的問題：{user_question}\n{model}：{respond}\n花費時間：{numpy.round(et-st,2)}秒'))
            # Bard
            elif user_msg[0:5]=='Bard:':
                bard_key = 'BARD_KEY'
                os.environ['_BARD_API_KEY'] = bard_key
                model = user_msg[0:4]
                user_question = user_msg[5:]
                respond = Bard().get_answer(f'{user_msg}')['content']
                et = time.time()
                line_bot_api.reply_message(tk, TextSendMessage(f'你的問題：{user_question}\n{model}：{respond}\n花費時間：{numpy.round(et-st,2)}秒'))
            # else:
                # respond = user_msg
                # line_bot_api.reply_message(tk, TextSendMessage(f'{respond}'))
        else:
            respond = 'Not Text'
        # print(reply)
    except Exception as e:
        line_bot_api.reply_message(tk, TextSendMessage(f'錯誤訊息:{e}'))
    return 'OK'


if __name__ == '__main__':
    # run_with_ngrok(app)
    app.run(debug=True)
    time.sleep(10)

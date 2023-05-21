from flask import Flask, request
import json

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import openai

openai.organization = 'org-gtPrrBF65iImcYUDhxzwQQJA'
openai.api_key = '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'

app = Flask(__name__)
@app.route('/', methods=['POST'])
def linebot():
    user_input = request.get_data(as_text=True)
    # msg = json_data['events'][0]['message']['text']
    try:
        json_data = json.loads(user_input)
        acccess_token = 'g1kdx2p4LAd4d/RL/rNEUxYzKN6Mb6SMqmyQ+JpGGRyVctJv5WyT6ap7ejxLB4Cm8RU1fSxEdIOneBL0779+FDrYjILQrHXYYe9YCV1v0ryqq/qFl1znpvjvQ7pcjlj7StL6YaJOb2vNOCjJn0pkzwdB04t89/1O/w1cDnyilFU='
        secret = 'd7f27bc016168116978f4b202235a3ab'
        line_bot_api = LineBotApi(acccess_token)
        handler = WebhookHandler(secret)
        signature = request.headers['X-Line-Signature']
        handler.handle(user_input, signature)
        tk = json_data['events'][0]['replyToken']
        type = json_data['events'][0]['message']['type']
        if type=="text":
            user_msg = json_data['events'][0]['message']['text']
            completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {
            'role':'user', 'content':f'{user_msg}'
            }
            ]
        )
            respond = completion.choices[0].message['content']
            print(f'Question:{user_msg}')
            print('Answer:',respond)
            reply = respond
        else:
            reply = 'Not Text'
        # print(reply)
        line_bot_api.reply_message(tk, TextSendMessage(reply))
    except:
        print(user_input)
    return 'OK'
if __name__ == '__main__':
    # run_with_ngrok(app)
    app.run(debug=True)
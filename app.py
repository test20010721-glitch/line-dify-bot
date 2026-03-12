from flask import Flask, request
import requests
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from linebot.exceptions import InvalidSignatureError

LINE_ACCESS_TOKEN = "LlTkej/6zspK9S66UptgB7URrQ9s+3ttH24rSNXWjhStLaoF0YwzfmT9EQWWpvPUXx9+0CimB+s7r1H/fszbG44ygtQFN5HDhFdh1nX1yyCHKpcQ+3HfhsGzxeHlIzD5gzHEBFzoUCHfFY/jFrSsoVwdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "e736ad79273449e4a4078ab9ce05dafe"

DIFY_API_KEY = "app-ynYrXvl0HjPmcG9xEuOkLuPb"

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():

    body = request.json
    events = body["events"]

    for event in events:

        if event["type"] == "message":

            user_message = event["message"]["text"]

            response = requests.post(
                "https://api.dify.ai/v1/chat-messages",
                headers={
                    "Authorization": f"Bearer {DIFY_API_KEY}"
                },
                json={
                    "inputs": {},
                    "query": user_message,
                    "response_mode": "blocking",
                    "conversation_id": "",
                    "user": "line-user"
                }
            )

            answer = response.json()["answer"]

            reply_token = event["replyToken"]

            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text=answer)
            )

    return "OK"

if __name__ == "__main__":
    app.run(port=5000)
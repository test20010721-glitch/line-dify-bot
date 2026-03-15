from flask import Flask, request
import requests
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("lTkej/6zspK9S66UptgB7URrQ9s+3ttH24rSNXWjhStLaoF0YwzfmT9EQWWpvPUXx9+0CimB+s7r1H/fszbG44ygtQFN5HDhFdh1nX1yyCHKpcQ+3HfhsGzxeHlIzD5gzHEBFzoUCHfFY/jFrSsoVwdB04t89/1O/w1cDnyilFU=")
DIFY_API_KEY = os.getenv("app-ynYrXvl0HjPmcG9xEuOkLuPb")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

@app.route("/")
def home():
    return "bot running"

@app.route("/callback", methods=["POST"])
def callback():

    body = request.get_json()
    event = body["events"][0]

    reply_token = event["replyToken"]
    user_message = event["message"]["text"]

    url = "https://api.dify.ai/v1/chat-messages"

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {},
        "query": user_message,
        "response_mode": "blocking",
        "user": "line-user"
    }

    response = requests.post(url, headers=headers, json=payload)
    answer = response.json().get("answer", "AIエラー")

    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text=answer)
    )

    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

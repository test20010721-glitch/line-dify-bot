from flask import Flask, request
import requests
import os
import json
from linebot import LineBotApi
from linebot.models import TextSendMessage

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

@app.route("/")
def home():
    return "LINE Dify Bot Running"

@app.route("/callback", methods=["POST"])
def callback():

    print("===== LINEからリクエスト受信 =====")

    body = request.get_json()
    print("受信データ:", json.dumps(body, indent=2, ensure_ascii=False))

    try:
        event = body["events"][0]

        reply_token = event["replyToken"]
        user_message = event["message"]["text"]

        print("ユーザー発言:", user_message)

        # Dify API呼び出し
        url = "https://api.dify.ai/v1/chat-messages"

        headers = {
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": {},
            "query": user_message,
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "line-user"
        }

        print("Difyへ送信:", payload)

        response = requests.post(url, headers=headers, json=payload)

        print("Difyレスポンスコード:", response.status_code)
        print("Difyレスポンス:", response.text)

        dify_response = response.json()

        answer = dify_response.get("answer", "AIから回答が取得できませんでした")

        print("AI回答:", answer)

        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=answer)
        )

        print("LINE返信成功")

    except Exception as e:
        print("エラー発生:", str(e))

    return "OK"


if __name__ == "__main__":
    app.run()




from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# 環境変数
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")

@app.route("/callback", methods=["POST"])
def callback():
    body = request.json

    for event in body["events"]:
        if event["type"] == "message":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]

            # Dify APIに送信
            dify_url = "https://api.dify.ai/v1/chat-messages"

            headers = {
                "Authorization": f"Bearer {DIFY_API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "inputs": {},
                "query": user_message,
                "response_mode": "blocking",
                "conversation_id": "",
                "user": "line-user"
            }

            response = requests.post(dify_url, headers=headers, json=data)

            dify_response = response.json()

            answer = dify_response.get("answer", "AIからの返信が取得できませんでした")

            # LINE返信
            line_url = "https://api.line.me/v2/bot/message/reply"

            line_headers = {
                "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }

            line_data = {
                "replyToken": reply_token,
                "messages": [
                    {
                        "type": "text",
                        "text": answer
                    }
                ]
            }

            requests.post(line_url, headers=line_headers, json=line_data)

    return "OK"

if __name__ == "__main__":
    app.run()

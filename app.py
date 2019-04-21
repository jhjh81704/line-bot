from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('4srE2J+eKTrC4fMj7C5rUmfJ8zyiNTwCNViqU19jh8c0RtLuey8Kk3ZwJOBdJ9QpOX5RBNm/A68h8Bieo6qrjhGvreR4xvSemwFck0lV1WwhJlDnGv4RVmZNIY35AKi8sQ9Xb3jNCqp7n3cUSEpRvwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('46778531e2dcd867c1309787409ff89b')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
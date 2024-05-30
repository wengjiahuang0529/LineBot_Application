# -*- coding: UTF-8 -*-
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('oazl76WLY4jVuc7ofYO5R2rQnmxEMuOsYHyjADIOfd9Gz1+SrlyVOjO1Dn4o95Jq8U1Z/b2ihjcsVwyyGGeboLMzhMokWRIMPovPzrfmM8ZqkixML+E2tDSEpnTYaUKF1RkIstfYIyrJ7P85AXLDpwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('0c4c7bf6cde5bbcb7b76a3e13fcea3a0')

# 監聽所有來自 /callback 的 Post Request
# @app.route("/callback", methods=['POST'])  #會一直return 404 not found，解決方法: https://hackmd.io/@Iamsowise17/S1AZbNFma
@app.route("/", methods=['POST'])
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
	message = TextSendMessage(text=event.message.text)
	line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
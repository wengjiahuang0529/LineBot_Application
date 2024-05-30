# -*- coding: UTF-8 -*-
from flask import Flask, request, abort
import DAN,csmapi, random, time, threading, stock
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import random

app = Flask(__name__)

#---------------------------------IoTtalk functions---------------------------------
def IoTtalk_registration():
    # set IoTtalk Server URL
    IoTtalk_ServerURL = 'http://140.114.77.93:9999'
    
    # set device profile
    # DAN.profile['dm_name'] = 'YOUR_DEVICEMODEL_NAME'
    # DAN.profile['df_list'] = ['YOUR_IDF', 'YOUR_ODF']
    DAN.profile['dm_name'] = 'm_DM'
    DAN.profile['df_list'] = ['m_in', 'm_out']
    
    # register device profile to IoTtalk Server
    DAN.device_registration_with_retry(IoTtalk_ServerURL, None)

def IoTtalk_push_and_pull(IDF, ODF, data):
    DAN.push(IDF, data)
    time.sleep(1.5)
    result = DAN.pull(ODF)
    if result is None:
        return "Error: Failed to retrieve data from IoTtalk server."
    return result

#---------------------------------IoTtalk functions---------------------------------
   
#---------------------------------LineBot API functions---------------------------------
# Channel Access Token
# line_bot_api = LineBotApi('YOUR CHANNEL ACCESS TOKEN')
line_bot_api = LineBotApi('oazl76WLY4jVuc7ofYO5R2rQnmxEMuOsYHyjADIOfd9Gz1+SrlyVOjO1Dn4o95Jq8U1Z/b2ihjcsVwyyGGeboLMzhMokWRIMPovPzrfmM8ZqkixML+E2tDSEpnTYaUKF1RkIstfYIyrJ7P85AXLDpwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
# handler = WebhookHandler('YOUR CHANNEL SECRET')
handler = WebhookHandler('0c4c7bf6cde5bbcb7b76a3e13fcea3a0')

# 監聽所有來自 /callback 的 Post Request
# @app.route("/callback", methods=['POST']) 這會回傳404
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
    
    #get message sent by line bot user
    text = event.message.text
    print(text)
    
    #============================================IMPLEMENT YOUR SCENARIO=====================================#

    #push and pull data through IoTtalk server
    # result = IoTtalk_push_and_pull("YOUR_IDF", "YOUR_ODF", text)
    result = IoTtalk_push_and_pull("m_in", "m_out", text)
    print(result)
    
    
    # add by myself
    if result[0] == '使用方法' :
        message = TextSendMessage('輸入股票代碼即可預測明日股價')
    else:
        # message = TextSendMessage(result[0])
        message = TextSendMessage('預測明日股價' + str(stock.stockpredict(result[0])))
    
    # write some codes here to handle the message 
    # message = TextSendMessage(result[0])
    
    # replay message to line bot user
    line_bot_api.reply_message(event.reply_token, message)
    
    #========================================================================================================#
    
#---------------------------------LineBot API functions---------------------------------

import os
if __name__ == "__main__":
         
    IoTtalk_registration()
     
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
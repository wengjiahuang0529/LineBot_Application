# -*- coding: UTF-8 -*-
from flask import Flask, request, abort
import DAN,csmapi, random, time, threading, stock, weather, earthquake
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
    valid_cities = ['宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣', '臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市', '基隆市', '新竹縣', '新竹市', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '嘉義市', '屏東縣']
    # add by myself
    if result[0] == '使用方法' : 
        message = TextSendMessage(f'1. *直接輸入想查詢天氣的縣市*，\nex:嘉義市\nAvailable values : {valid_cities}\
        \n\n2. *輸入股票代碼即可預測明日股價*\nex:2330 \n\n3. *輸入"xxx地震資訊"可取得xxx縣市的地震訊息*\nex:宜蘭縣地震資訊\n')
        line_bot_api.reply_message(event.reply_token, message)
        
    elif result[0].isdigit():
        message = TextSendMessage('預測明日股價' + str(stock.stockpredict(result[0])))
        line_bot_api.reply_message(event.reply_token, message)
        
    elif result[0].endswith('地震資訊'):
        city_prefix = result[0][:3]
        if city_prefix in valid_cities:
            print(city_prefix)
            # 取得地震資訊列表
            eq_info = earthquake.get_earthquake_info(city_prefix)
            messages = []
            if eq_info:
                for info in eq_info[:3]:  # 取前三筆，也可全部印出，只是可能會跑出很多資料很亂。
                    # 建立圖片訊息
                    image_message = ImageSendMessage(
                        original_content_url=info["imageThumbnail"],  # 圖片的原始 URL
                        preview_image_url=info["imageThumbnail"]      # 圖片的預覽 URL
                    )
                    # 建立地震資訊訊息
                    text_message = TextSendMessage(info["message"])
                    #messages.append(image_message) #append會讓line bot出現問題，他好像無法一次傳超過五筆，所以改成下面兩行分開傳
                    #messages.append(text_message)  #append會讓line bot出現問題，他好像無法一次傳超過五筆，所以改成下面兩行分開傳
                    line_bot_api.push_message(event.source.user_id, text_message)    
                    line_bot_api.push_message(event.source.user_id, image_message)
            else:
                messages.append(TextSendMessage(f"{city_prefix}很和平~"))
                line_bot_api.push_message(event.source.user_id, messages)    
                           
        else:
            message = TextSendMessage("請提供一個有效的縣市名稱以獲取地震資訊。")
            line_bot_api.reply_message(event.reply_token, message)
            
    elif result[0] in valid_cities:
        # message = TextSendMessage(result[0])
        message = TextSendMessage('以下為目前天氣狀況:\n' + str(weather.get_weather_data(result[0])))
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage('輸入錯誤，請輸入使用方法或重新輸入')
        line_bot_api.reply_message(event.reply_token, message)
    # write some codes here to handle the message 
    # message = TextSendMessage(result[0])
    
    # replay message to line bot user
    #line_bot_api.reply_message(event.reply_token, message)
    
    #========================================================================================================#
    
#---------------------------------LineBot API functions---------------------------------

import os
if __name__ == "__main__":
         
    IoTtalk_registration()
     
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
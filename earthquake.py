import requests

url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization=CWA-63E20F0D-0CB3-4549-90F4-997738A4871A'

def get_earthquake_info(city_name):
    print(f'Getting earthquake info for {city_name}...')

    response = requests.get(url)
    data = response.json()
    eq = data['records']['Earthquake']
    earthquake_data = []  # 存地震資訊
    for i in eq:
        if 'Epicenter' in i['EarthquakeInfo'] and 'Location' in i['EarthquakeInfo']['Epicenter']:
            loc = i['EarthquakeInfo']['Epicenter']['Location']
            if loc.startswith(city_name):  # 檢查是否是指定的縣市
                val = i['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue']
                dep = i['EarthquakeInfo']['FocalDepth']
                eq_time = i['EarthquakeInfo']['OriginTime']
                img = i['ReportImageURI']
                msg = f'{loc}，芮氏規模 {val} 級，深度 {dep} 公里，發生時間 {eq_time}'
                print(msg)
                
                send_data = {
                    'message': msg,            # 發送的訊息
                    'imageThumbnail': img,     # 預覽圖片網址
                    'imageFullsize': img       # 完整圖片網址
                }
                earthquake_data.append(send_data)  # 加入地震資訊
    return earthquake_data

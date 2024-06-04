# https://opendata.cwa.gov.tw/dataset/forecast/F-C0032-001

import requests

def get_weather_data(city_name):
    # 天氣預報API的URL
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-63E20F0D-0CB3-4549-90F4-997738A4871A&format=JSON"
    
    print('Getting earthquake info')
    
    # 發送請求並獲取數據
    response = requests.get(url)
    data = response.json()

    # 解析天氣數據
    def parse_weather_data(data, city_name):
        records = data['records']
        locations = records['location']

        for location in locations:
            location_name = location['locationName']
            if location_name == city_name:
                weather_state = None
                rain_prob = None
                min_temp = None
                max_temp = None

                weather_elements = location['weatherElement']

                for element in weather_elements:
                    element_name = element['elementName']
                    if element_name == "Wx":
                        weather_state = element['time'][0]['parameter']['parameterName']
                    elif element_name == "PoP":
                        rain_prob = element['time'][0]['parameter']['parameterName']
                    elif element_name == "MinT":
                        min_temp = element['time'][0]['parameter']['parameterName']
                    elif element_name == "MaxT":
                        max_temp = element['time'][0]['parameter']['parameterName']

                return {
                    'city_name': city_name,
                    'weather_state': weather_state,
                    'rain_prob': rain_prob,
                    'min_temp': min_temp,
                    'max_temp': max_temp
                }
        return None

    # 獲得指定城市的天氣數據
    weather_data = parse_weather_data(data, city_name)

    # 如果找不到天氣數據，返回錯誤信息
    if weather_data is None:
        return f"沒有 {city_name} 的資料 :( "
    else: 
        formatted_weather_data = (
            f"查詢的縣市: {weather_data['city_name']}\n"
            f"天氣狀態: {weather_data['weather_state']}\n"
            f"降雨機率: {weather_data['rain_prob']}%\n"
            f"溫度: {weather_data['min_temp']}°C ~ {weather_data['max_temp']}°C"
        ) 
        # print(type(formatted_weather_data))
        return formatted_weather_data

# # 範例:
# city_name = "嘉義縣"
# weather_data = get_weather_data(city_name)

# if isinstance(weather_data, dict):
#     print(f"城市: {weather_data['city_name']}")
#     print(f"天氣狀況: {weather_data['weather_state']}")
#     print(f"降雨機率: {weather_data['rain_prob']}%")
#     print(f"最低溫度: {weather_data['min_temp']}°C")
#     print(f"最高溫度: {weather_data['max_temp']}°C")
# else:
#     print(weather_data)

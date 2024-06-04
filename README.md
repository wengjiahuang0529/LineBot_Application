# LineBot:
Stock Prediction 📊
Weather Check 🌦️
Earthquake Monitoring 🌐
![image](https://github.com/wengjiahuang0529/LineBot_Application/assets/96289978/c7e6a4df-2336-4d22-8269-c23154cea998)

**<h2>linebot_echo.py</h2>**
• LineBot’s sample code for echo response  

**<h2>csmapi.py/DAN.py</h2>**
• Some useful APIs about IoTtalk connection  
• Don’t need to modify them
**<h2>app.py</h2>**
• Mainly modify this file

**<h2>Spec</h2>**
**• Design the scenario**  
> 1. Reply：the status of machines, the information of something, the location of something, etc.  
> 2. Recommendation： Restaurants, Movies, Attractions, etc.  
> 3. Other：Game …
   
**• IoTtalk**   
> • Design your own Device Model (at least one) 

**• LineBot**  
> • Your LineBot need to interact with IoTtalk(send/receive data to/from IoTtalk)  
> • You can modify ‘app.py’ to finish mini project 4

**Preliminary**  
• Line Account (https://developers.line.biz/en/)  
• Ngrok (https://ngrok.com/download)
   * You need to sign up and follow the instruction on the download page to add authtoken.
     
---
**<h2>How to operate</h2>**
1. Use Iottalk to add project :
![image](https://github.com/wengjiahuang0529/LineBot_PredictStock/assets/96289978/a80f1189-8d82-483d-8f22-2f672415ea22)

2. When you run python app.py, you will see the device name. IoTtalk's device needs to connect to this name.

3. You can run linebot_echo.py, but you need to change the token and secret to your own. You can apply for these at [Line Developers](https://developers.line.biz/en/).  
After executing, when you type in this Line channel, you'll see it echo back exactly what you typed.

4. Ngrok，it provides a service that helps developers share sites and apps running on their local machines or
servers.
   * Start a tunnel : ngrok http port  

5. Message API Settings
![image](https://github.com/wengjiahuang0529/LineBot_PredictStock/assets/96289978/0811af62-d190-4730-aefc-476b1d546a60)



heroku buildpacks:set heroku/python
from flask import Flask, request, abort  
from linebot import (
　　LineBotApi, WebhookHandler
 ) 
from linebot.exceptions import (
　　InvalidSignatureError
 ) 
from linebot.models import *

app = Flask(__name__)  
# 必須放上自己的Channel Access Token 
line_bot_api = LineBotApi('+NVSn1t0cmsD/NEdD7VxRf20f6ycv0O9ypddg1j8k4PB+h5o5DYQu70NDZKNWuKyiyEdARphwIRNt+9dvYyqA5NX35ilcxyivu9x/jCONecgMWqlJLYiLrmPHhQNucQarqbz8mMOIaB9tsFG7Hs9BgdB04t89/1O/w1cDnyilFU=')  
# 必須放上自己的Channel Secret
 handler = WebhookHandler('d10ad5359e10414a8bd074926ae0e643')
line_bot_api.push_message('Ue4d3f17768ea75f3bfa388142bf4b3b5', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request 
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
　　　　abort(400)      
　　return 'OK'

#訊息傳遞區塊 
##### 基本上程式編輯都在這個function ##### 
@handler.add(MessageEvent, message=TextMessage) 
def handle_message(event):     
　　message = event.message.text     
　　line_bot_api.reply_message(event.reply_token,TextSendMessage(message))
  
  #主程式 
import os if __name__ == "__main__":    
　　port = int(os.environ.get('PORT', 5000))     
　　app.run(host='0.0.0.0', port=port)


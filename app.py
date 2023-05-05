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


import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import pyfolio as pf

from models import BollingerModel, KdModel, RsiModel

MAX_TRY = 3

def user_input(max_try):
    for _ in range(max_try):

        stock = input("Please enter the stock name: ")

        try:
            days = int(input("Please enter how many days you want to test from now: "))
            end_day = dt.datetime.today()
        except:
            raise ValueError("The days you input is not valid !")
            continue

        try:
            capital = int(input("Please enter the capital you want to invest: "))
        except:
            raise ValueError("The capital you input is not valid !")
            continue

        try:
            strategy = int(input("Please choose the strategy you want to use(enter one of the numbers below):\n1.Boll 2.KD 3.RSI\n"))
        except:
            raise ValueError("The number you input is not valid!")
            continue
        if strategy < 1 or strategy > 3:
            print('The number must be in the range 1~3')
            continue

        break
        
    return stock, days, end_day, capital, strategy
            

def write_xlsx(self, file_name):
    with pd.ExcelWriter(file_name) as writer:
        self.data.to_excel(writer)


if __name__ == "__main__":
    stock, days, end_day, capital, strategy = user_input(MAX_TRY)
    # users choose Bollinger
    if strategy == 1:
        boll = BollingerModel(symbol=stock, end_day=end_day, days=days, capital=capital)
        try:
            start = int(input("Please input the minimum MA you want to use: "))
            end = int(input("Please input the maximum MA you want to use: "))
        except:
            raise ValueError("The MA you input is not valid!")
        if start > end:
            print('The number must be in the range 1~3')
            exit()
        best_window, best_dr, best_sr = boll.optimizer(start, end)
        print(best_window, best_dr, best_sr)
        boll.plot_equity_curve(best_window)
    
    # users choose KD
    elif strategy == 2:
        try:
            start = int(input("Please input the minimum number of days in the past you want to use: "))
            end = int(input("Please input the maximum number of days in the past you want to use: "))
        except:
            raise ValueError("The the number of days you input is not valid!")
        if start > end:
            print('The number must be in the range 1~3')
            exit()
        k_value = 50
        kd = KdModel(symbol=stock, end_day=end_day, days=days, capital=capital, k=k_value)
        best_window, best_dr, best_sr = kd.optimizer(start, end)
        print(best_window, best_dr, best_sr)
        kd.plot_equity_curve(best_window)
    
    # users choose RSI
    elif strategy == 3:
        try:
            start_short = int(input("Please input the minimum slow line you want to use: "))
            end_short = int(input("Please input the maximum slow line you want to use: "))
            start_long = int(input("Please input the minimum long line you want to use: "))
            end_long = int(input("Please input the maximum long line you want to use: "))
        except:
            raise ValueError("The the number of days you input is not valid!")
        if (start_short > end_short) or (start_long > end_long) or \
            (end_short > start_long):
                print('The number of days is out of the range')
                exit()
        rsi = RsiModel(symbol=stock, end_day=end_day, days=days, capital=capital)
        max_short, max_long, max_dr, max_sr = \
            rsi.optimizer(start_short, end_short, start_long, end_long)
        print(max_short, max_long, max_dr, max_sr)
        rsi.plot_equity_curve(max_short, max_long)

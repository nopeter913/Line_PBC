from flask_ngrok import run_with_ngrok
from flask import Flask, request

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 載入 json 標準函式庫，處理回傳的資料格式
import json
import os 

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = '+NVSn1t0cmsD/NEdD7VxRf20f6ycv0O9ypddg1j8k4PB+h5o5DYQu70NDZKNWuKyiyEdARphwIRNt+9dvYyqA5NX35ilcxyivu9x/jCONecgMWqlJLYiLrmPHhQNucQarqbz8mMOIaB9tsFG7Hs9BgdB04t89/1O/w1cDnyilFU='
        secret = 'd10ad5359e10414a8bd074926ae0e643'
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        msg = json_data['events'][0]['message']['text']      # 取得 LINE 收到的文字訊息
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        line_bot_api.reply_message(tk,TextSendMessage(msg))  # 回傳訊息
        print(msg, tk)                                       # 印出內容
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                 # 驗證 Webhook 使用，不能省略

@app.route('/test')
def test():
  return "This is test"

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))     
　app.run(host='0.0.0.0', port=port)

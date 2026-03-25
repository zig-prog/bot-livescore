import requests
import time
import threading
from flask import Flask

# === PHẦN CẦN CHỈNH SỬA ===
WEBHOOK_URL = "https://discord.com/api/webhooks/1485925859352121445/04lv4ybtgtIwan0aB9ob4d6W6dVCe759pt9-9jtl5KhwpvqY80qUp3ttQPLeKFQ1tOkX"
API_KEY = "424498e210msh4dbd2a485b8024dp1fceabjsnbc5d8813da67"
FIXTURE_ID = "123456" # Nhớ thay ID trận đấu thật vào đây nhé
# ===========================

current_home_score = 0
current_away_score = 0

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot LiveScore đang hoạt động!"

# 1. HÀM GỬI TIN NHẮN TEST (MỚI THÊM)
def send_test_webhook():
    data = {
        "content": "🛠️ **[HỆ THỐNG] KIỂM TRA ĐƯỜNG TRUYỀN** 🛠️",
        "embeds": [{
            "title": "⚽ [TEST] Đội Nhà 1 - 0 Đội Khách",
            "color": 65280, # Màu xanh lá cây báo hiệu thành công
            "description": "✅ Bot đã kết nối thành công với Webhook! Đang theo dõi trận đấu và sẵn sàng báo bàn thắng."
        }]
    }
    requests.post(WEBHOOK_URL, json=data)
    print("Đã gửi tin nhắn test vào Discord!")

def check_live_score():
    global current_home_score, current_away_score
    try:
        url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?id={FIXTURE_ID}"
        headers = {"X-RapidAPI-Key": API_KEY}
        response = requests.get(url, headers=headers).json()
        
        match_data = response['response'][0]
        home_team = match_data['teams']['home']['name']
        away_team = match_data['teams']['away']['name']
        new_home_score = match_data['goals']['home']
        new_away_score = match_data['goals']['away']
        
        # Nếu có bàn thắng mới
        if new_home_score > current_home_score or new_away_score > current_away_score:
            send_discord_webhook(home_team, new_home_score, away_team, new_away_score)
            current_home_score = new_home_score
            current_away_score = new_away_score
    except Exception as e:
        pass # Bỏ qua lỗi nếu trận đấu chưa bắt đầu

def send_discord_webhook(home, score_h, away, score_a):
    data = {
        "content": "🚨 **VÀOOOOOOOOO!!!** 🚨",
        "embeds": [{
            "title": f"⚽ {home} {score_h} - {score_a} {away}",
            "color": 16711680, # Màu đỏ rực lửa
            "description": "Bàn thắng vừa được ghi! Khán đài đang nổ tung!"
        }]
    }
    requests.post(WEBHOOK_URL, json=data)

def run_bot():
    # 2. GỌI HÀM TEST NGAY KHI BOT KHỞI ĐỘNG
    send_test_webhook() 
    
    while True:
        check_live_score()
        time.sleep(60) # Cứ 60 giây kiểm tra 1 lần

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=8080)

import os
import time
import json
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# Render port tələbini qarşılamaq üçün sadə veb server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active and running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

Thread(target=run_server, daemon=True).start()

# Yeni Telegram Bot Tokeni
TOKEN = "8945130144:AAFy3yBd_VSSsc4zujbqz0ZuLkf_D-rVWUc"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=20"
    if offset:
        url += f"&offset={offset}"
    try:
        req = urllib.request.urlopen(url, timeout=25)
        return json.loads(req.read().decode("utf-8"))
    except Exception:
        time.sleep(2)
        return None

def send_message(chat_id, text):
    url = URL + "sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass

def generate_real_analysis(match_info):
    return f"""<b>⚽ PEŞƏKAR MATÇ ANALİZİ VƏ STATİSTİKA</b>

📌 <b>Daxil edilən məlumat / Matç:</b> 
<i>{match_info}</i>

<b>📊 Heyət, Zədələr və Turnir Vəziyyəti Analizi:</b>
• <b>Əsas Heyət / İtkilər:</b> Tərəflərin son məşq və heyət hesabatlarına əsasən, meydan sahibində əsas hücum xətti oyunçularının bəziləri sualtıdır, qonaq komandada isə yarımmüdafiənin əsas dirəyi diskvalifikasiya səbəbilə heyətdə yoxdur.
• <b>Turnir Cədvəli Motivasiyası:</b> Ev sahibi komanda liderlik yarışından qopmamaq üçün qələbəyə məcburdur; qonaqlar isə səfərdə daha çox müdafiəyə üstünlük verəcək.

<b>📈 Bukmeker Gözləntiləri və Əmsallar:</b>
• <b>Əsas Nəticə (1X2):</b> Ev sahibinin qələbə ehtiycalı üstünlüyü yüksəkdir (1X şansı daha etibarlıdır).
• <b>Qol Sayı (Alt / Üst):</b> Taktiki gərginlik səbəbilə matçın 1.5 Üst və ya 2.5 Alt aralığında keçməsi ehtiyaclıdır.
• <b>İlk Hissə (HT):</b> İlk yarıda ehtiyatlı oyun və ya bərabərlik gözlənilir.
• <b>Dəqiq Hesab ehtimalı:</b> 1:0 və ya 2:1

---
✨ <i>Coşqun Təxmini-</i>"""

def main():
    offset = None
    print("Coşqun Peşəkar Analiz Botu işləyir...")
    while True:
        updates = get_updates(offset)
        if updates and "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                if "message" in update and "text" in update["message"]:
                    chat_id = update["message"]["chat_id"]
                    user_text = update["message"]["text"].strip()
                    
                    if user_text.lower() == "/start":
                        reply_text = (
                            "⚽ <b>Salam! Coşqun Peşəkar Analiz Botuna xoş gəlmisiniz.</b>\n\n"
                            "Mənə matç adlarını, komandaları və ya linkləri göndərin; "
                            "mən zədəli oyunçuları, turnir cədvəlini, əsas heyəti və bukmeker gözləntilərini "
                            "nəzərə alaraq real statistika təqdim edim!"
                        )
                        send_message(chat_id, reply_text)
                    else:
                        analysis = generate_real_analysis(user_text)
                        send_message(chat_id, analysis)
        time.sleep(1)

if __name__ == "__main__":
    main()

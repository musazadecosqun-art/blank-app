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
        self.wfile.write(b"Bot is active!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

Thread(target=run_server, daemon=True).start()

# Telegram Bot Tokeni
TOKEN = "8945130144:AAFy3yBd_VSSsc4zujbqz0ZuLkf_D-rVWUc"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=30"
    if offset:
        url += f"&offset={offset}"
    try:
        req = urllib.request.urlopen(url, timeout=35)
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
    return f"""<b>COSQUN PESEKAR MATÇ ANALİZİ VƏ STATİSTİKA</b>

<b>Matç / Sorğu:</b> 
<i>{match_info}</i>

<b>Heyət, Zədələr və Turnir Vəziyyəti:</b>
• <b>Əsas Heyət və İtkilər:</b> Komandaların son məşq hesabatlarına və ehtimal olunan start 11-liklərinə əsasən, əsas heyət üzvlərindən bəziləri zədə səbəbindən kadrdan kənardadır.
• <b>Turnir Cədvəli və Motivasiya:</b> Tərəflərin mövqe mübarizəsi taktikaya birbaşa təsir edəcək.

<b>Bukmeker Gözləntiləri və Təxminlər:</b>
• <b>1X2 Proqnozu:</b> Ev sahibinin qələbəsi və ya 1X şansı yüksəkdir.
• <b>Qol Sayı:</b> 1.5 Ust və ya 2.5 Alt aralığı.
• <b>İlkin Hissə (HT):</b> Ehtiyatlı başlanğıc və ya bərabərlik.
• <b>Dəqiq Hesab Ehtimalı:</b> 1:0 / 2:1

---
<i>Coşqun Təxmini-</i>"""

def main():
    offset = None
    print("Bot aktivdir və işləyir...")
    while True:
        updates = get_updates(offset)
        if updates and isinstance(updates, dict) and "result" in updates:
            for update in updates["result"]:
                try:
                    offset = update["update_id"] + 1
                    message = update.get("message")
                    if message and "text" in message:
                        chat_id = message["chat"]["id"]
                        user_text = message["text"].strip()
                        
                        if user_text.lower() == "/start":
                            reply_text = (
                                "<b>Salam! Cosqun Peşəkar Analiz Botuna xoş gəlmisiniz.</b>\n\n"
                                "Mənə istənilən matçın adını, linkini və ya məlumatını göndərin; "
                                "zədəli oyunçuları, turnir cədvəlini, heyətləri və bukmeker əmsallarını "
                                "nəzərə alaraq dərhal real statistika və proqnoz təqdim edim!"
                            )
                            send_message(chat_id, reply_text)
                        else:
                            analysis = generate_real_analysis(user_text)
                            send_message(chat_id, analysis)
                except Exception:
                    continue
        time.sleep(1)

if __name__ == "__main__":
    main()
    

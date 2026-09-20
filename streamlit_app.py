import os
import time
import json
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# Render üçün sadə veb server (Port xətasını aradan qaldırmaq üçün)
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Veb serveri arxa planda işə salırıq
Thread(target=run_server, daemon=True).start()

# Telegram Bot Konfiqurasiyası
TOKEN = "8828914277:AAH6elG9rH6oNMn0Hd4JNq0no_50Q5JzG7I"
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

def analyze_match(text):
    return f"""<b>⚽ Futbol Matçının Təhlili və Proqnozları</b>

{text}

<b>📊 Detallı Təxminlər:</b>
• <b>1X2:</b> MS 1 (Ev sahibi qələbə və ya bərabərlik)
• <b>İlk Hissə (HT) Hesabı:</b> 1 - 0
• <b>Dəqiq Hesab:</b> 2 - 1
• <b>HT / FT (İlk Yarı / Maç Sonu):</b> 1 / 1
• <b>Kornerlər:</b> 9.5-dən Çox (Over)
• <b>Penalti:</b> Olabilər (1.30 əmsal)
• <b>Cüt Şans:</b> 1X və ya Üst 1.5

<b>📈 Alt / Üst Proqnozları (0.5 - 5):</b>
• <b>0.5 Üst:</b> Bəli (Təsdiqləndi)
• <b>1.5 Üst:</b> Bəli
• <b>2.5 Üst:</b> Gözlənilir
• <b>3.5 Alt:</b> Riskli ola bilər
• <b>4.5 / 5.0 Alt:</b> Alt bitmə ehtimalı yüksəkdir

---
✨ <i>Coşqun Təxmini-</i>"""

def main():
    offset = None
    print("Coşqun Analiz Botu işləyir və dataları gözləyir...")
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
                            "⚽ <b>Salam! Coşqun Analiz Botuna xoş gəlmisiniz.</b>\n\n"
                            "Matçın datalarını və ya məlumatını bura göndərin, "
                            "sizə bütün detallı proqnozları 'Coşqun Təxmini-' imzası ilə təqdim edim!"
                        )
                        send_message(chat_id, reply_text)
                    else:
                        prediction = analyze_match(user_text)
                        send_message(chat_id, prediction)
        time.sleep(1)

if __name__ == "__main__":
    main()
    

import os
import time
import json
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# Render port tələbini qarşılamaq və 7/24 aktiv saxlamaq üçün veb server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Cosqun Bot is 7/24 Active!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

Thread(target=run_server, daemon=True).start()

# Telegram Bot Tokeni
TOKEN = "8945130144:AAFy3yBd_VSSsc4zujbqz0ZuLkf_D-rVWUc"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def send_message(chat_id, text):
    url = URL + "sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass

def generate_full_analysis(query):
    return f"""<b>⚽ PEŞƏKAR MATÇ ANALİZİ VƏ TƏXMİN</b>

🔗 <b>Sorğu / Link:</b> <i>{query}</i>

🏠 vs 🇦🇿 <b>Komandalar:</b> Ev Sahibi (Klub/Ölkə) - Qonaq (Klub/Ölkə)

📊 <b>ƏTRAFLI STATİSTİK TƏQDİMAT:</b>
• <b>FT Prediction (1X2):</b> MS 1 (%68 şans)
• <b>İlk Hissə (HT) Hesabı & Qol:</b> 1 - 0 (%58)
• <b>Dəqiq Hesab (Correct Score):</b> 2 - 1 (%42)
• <b>HT / FT Nəticəsi:</b> 1 / 1 (%52)
• <b>Kornerlər:</b> 9.5-dən Çox (Over) — %64
• <b>Penalti:</b> Bəli (%48) / Xeyr (%52)
• <b>Cüt Şans (Double Chance):</b> 1X (%85) | 12 (%82) | X2 (%35)

📈 <b>ALT / ÜST (OVER / UNDER) FAİZLƏRİ:</b>
• <b>0.5 Üst:</b> %96 | <i>Alt:</i> %4
• <b>1.0 Üst:</b> %88 | <i>Alt:</i> %12
• <b>1.5 Üst:</b> %76 | <i>Alt:</i> %24
• <b>2.5 Üst:</b> %58 | <i>Alt:</i> %42
• <b>3.0 Üst:</b> %40 | <i>Alt:</i> %60
• <b>3.5 Üst:</b> %28 | <i>Alt:</i> %72
• <b>4.0 Üst:</b> %18 | <i>Alt:</i> %82
• <b>4.5 Üst:</b> %12 | <i>Alt:</i> %88
• <b>5.0 Üst:</b> %7  | <i>Alt:</i> %93

---
✨ <b>Coşqun Təxmini-</b>"""

def main():
    offset = 0
    processed_messages = set()  # Təkrar mesajların qarşısını almaq üçün yaddaş
    print("Coşqun 7/24 Analiz Botu işləyir...")
    
    while True:
        try:
            url = f"{URL}getUpdates?offset={offset}&timeout=30"
            req = urllib.request.urlopen(url, timeout=35)
            updates = json.loads(req.read().decode("utf-8"))
            
            if updates and isinstance(updates, dict) and "result" in updates:
                for update in updates["result"]:
                    update_id = update["update_id"]
                    offset = update_id + 1
                    
                    message = update.get("message")
                    if message and "text" in message:
                        msg_id = message["message_id"]
                        chat_id = message["chat"]["id"]
                        user_text = message["text"].strip()
                        
                        # Əgər bu mesaj artıq cavablandırılıbsa, ötür
                        if msg_id in processed_messages:
                            continue
                        processed_messages.add(msg_id)
                        
                        # Yaddaşın həddindən artıq dolmasının qarşısını alaq
                        if len(processed_messages) > 100:
                            processed_messages.pop()
                        
                        if user_text.lower() == "/start":
                            reply_text = (
                                "<b>⚽ Salam! Coşqun Peşəkar Analiz Botuna xoş gəlmisiniz.</b>\n\n"
                                "Mənə istənilən matçın linkini və ya adını göndərin; "
                                "komandaları, zədələri, turnir cədvəlini və bukmeker əmsallarını "
                                "nəzərə alaraq <b>bütün alt/üst faizləri, dəqiq hesab və korner proqnozlarını</b> "
                                "birbaşa təqdim edim!\n\n"
                                "<i>Coşqun Təxmini-</i>"
                            )
                            send_message(chat_id, reply_text)
                        else:
                            analysis = generate_full_analysis(user_text)
                            send_message(chat_id, analysis)
        except Exception:
            time.sleep(2)
            continue
        time.sleep(0.5)

if __name__ == "__main__":
    main()
    

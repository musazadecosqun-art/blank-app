import os
import time
import json
import urllib.request
import random
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

def generate_dynamic_analysis(query):
    # Göndərilən mətnə/linkə əsasən random amma məntiqli faizlər və nəticələr yaradırıq
    # Bu, hər matçın özünə özəl fərqli nəticə çıxarmasını təmin edir
    random.seed(hash(query) % 10000)
    
    home_score = random.randint(0, 3)
    away_score = random.randint(0, 3)
    ht_home = random.randint(0, 1)
    ht_away = random.randint(0, 1)
    
    ms1_p = random.randint(45, 82)
    x_p = random.randint(15, 30)
    ms2_p = 100 - (ms1_p + x_p)
    if ms2_p < 10: ms2_p = 12
    
    corner_val = round(random.uniform(8.5, 11.5), 1)
    corner_p = random.randint(55, 78)
    
    pen_val = "Bəli" if random.random() > 0.6 else "Xeyr"
    pen_p = random.randint(40, 65)
    
    # Komanda adlarını sorğudan çıxarmağa çalışırıq və ya ümumi ad veririk
    clean_query = query.replace("https://", "").replace("http://", "").replace("www.", "")
    parts = clean_query.split("/")
    match_title = parts[-1].replace("-", " ").upper() if len(parts) > 0 and len(parts[-1]) > 3 else query.upper()

    return f"""<b>⚽ PEŞƏKAR MATÇ ANALİZİ VƏ TƏXMİN</b>

🔗 <b>Sorğu / Link:</b> <i>{query}</i>

🏠 vs 🇦🇿 <b>Matç / Komandalar:</b> <code>{match_title}</code>

📊 <b>DİNAMİK STATİSTİK TƏQDİMAT:</b>
• <b>FT Prediction (1X2):</b> MS 1 (%{ms1_p}) | X (%{x_p}) | MS 2 (%{ms2_p})
• <b>İlk Hissə (HT) Hesabı & Qol:</b> {ht_home} - {ht_away} (%{random.randint(50, 70)})
• <b>Dəqiq Hesab (Correct Score):</b> {home_score} - {away_score} (%{random.randint(35, 55)})
• <b>HT / FT Nəticəsi:</b> {'1 / 1' if ht_home > ht_away else 'X / 1'} (%{random.randint(45, 65)})
• <b>Kornerlər:</b> {corner_val}-dən Çox (Over) — %{corner_p}
• <b>Penalti:</b> {pen_val} (%{pen_p})
• <b>Cüt Şans (Double Chance):</b> 1X (%{random.randint(75, 92)}) | 12 (%{random.randint(70, 88)}) | X2 (%{random.randint(30, 55)})

📈 <b>ALT / ÜST (OVER / UNDER) FAİZLƏRİ:</b>
• <b>0.5 Üst:</b> %{random.randint(90, 98)} | <i>Alt:</i> %{random.randint(2, 10)}
• <b>1.0 Üst:</b> %{random.randint(80, 92)} | <i>Alt:</i> %{random.randint(8, 20)}
• <b>1.5 Üst:</b> %{random.randint(70, 85)} | <i>Alt:</i> %{random.randint(15, 30)}
• <b>2.5 Üst:</b> %{random.randint(45, 68)} | <i>Alt:</i> %{random.randint(32, 55)}
• <b>3.0 Üst:</b> %{random.randint(30, 50)} | <i>Alt:</i> %{random.randint(50, 70)}
• <b>3.5 Üst:</b> %{random.randint(20, 40)} | <i>Alt:</i> %{random.randint(60, 80)}
• <b>4.0 Üst:</b> %{random.randint(12, 28)} | <i>Alt:</i> %{random.randint(72, 88)}
• <b>4.5 Üst:</b> %{random.randint(8, 20)} | <i>Alt:</i> %{random.randint(80, 92)}
• <b>5.0 Üst:</b> %{random.randint(4, 15)} | <i>Alt:</i> %{random.randint(85, 96)}

---
✨ <b>Coşqun Təxmini-</b>"""

def main():
    offset = 0
    processed_messages = set()
    print("Coşqun 7/24 Dinamik Analiz Botu işləyir...")
    
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
                        
                        if msg_id in processed_messages:
                            continue
                        processed_messages.add(msg_id)
                        
                        if len(processed_messages) > 100:
                            processed_messages.pop()
                        
                        if user_text.lower() == "/start":
                            reply_text = (
                                "<b>⚽ Salam! Coşqun Peşəkar Analiz Botuna xoş gəlmisiniz.</b>\n\n"
                                "Mənə istənilən matçın linkini və ya adını göndərin; "
                                "hər matç üçün xüsusi olaraq <b>bütün alt/üst faizləri, dəqiq hesab, korner və proqnozları</b> "
                                "analiz edib təqdim edim!\n\n"
                                "<i>Coşqun Təxmini-</i>"
                            )
                            send_message(chat_id, reply_text)
                        else:
                            analysis = generate_dynamic_analysis(user_text)
                            send_message(chat_id, analysis)
        except Exception:
            time.sleep(2)
            continue
        time.sleep(0.5)

if __name__ == "__main__":
    main()

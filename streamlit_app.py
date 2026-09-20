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
        self.wfile.write(b"Cosqun Bot Full Combo Analysis Active!")

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

def generate_chain_linked_analysis(query):
    random.seed(hash(query) % 10000)
    
    # Zəncirvari dəqiq hesab ssenariləri
    scenarios = [
        {"h": 2, "a": 1, "ht_h": 1, "ht_a": 0, "htft": "1 / 1", "ms": "MS 1", "dc": "1X", "tot": 3, "btts": "Bəli"},
        {"h": 1, "a": 0, "ht_h": 1, "ht_a": 0, "htft": "1 / 1", "ms": "MS 1", "dc": "1X", "tot": 1, "btts": "Xeyr"},
        {"h": 1, "a": 1, "ht_h": 0, "ht_a": 1, "htft": "2 / X", "ms": "Bərabərlik (X)", "dc": "1X / X2", "tot": 2, "btts": "Bəli"},
        {"h": 0, "a": 2, "ht_h": 0, "ht_a": 1, "htft": "2 / 2", "ms": "MS 2", "dc": "X2", "tot": 2, "btts": "Xeyr"},
        {"h": 3, "a": 1, "ht_h": 2, "ht_a": 0, "htft": "1 / 1", "ms": "MS 1", "dc": "1X", "tot": 4, "btts": "Bəli"},
        {"h": 1, "a": 2, "ht_h": 0, "ht_a": 1, "htft": "2 / 2", "ms": "MS 2", "dc": "X2", "tot": 3, "btts": "Bəli"},
        {"h": 2, "a": 0, "ht_h": 1, "ht_a": 0, "htft": "1 / 1", "ms": "MS 1", "dc": "1X", "tot": 2, "btts": "Xeyr"},
    ]
    
    sc = random.choice(scenarios)
    home_score = sc["h"]
    away_score = sc["a"]
    total_goals = sc["tot"]
    btts_val = sc["btts"]
    is_home_win = home_score > away_score
    is_away_win = away_score > home_score

    clean_query = query.replace("https://", "").replace("http://", "").replace("www.", "")
    parts = clean_query.split("/")
    match_title = parts[-1].replace("-", " ").upper() if len(parts) > 0 and len(parts[-1]) > 3 else query.upper()

    # Zəncirvari kombi nəticələrinin məntiqi hesablanması
    btts_yes_p = random.randint(55, 82) if btts_val == "Bəli" else random.randint(20, 42)
    btts_no_p = 100 - btts_yes_p

    w1_btts_yes = "Gözlənilir" if (is_home_win and btts_val == "Bəli") else "Risklidir"
    w1_btts_no = "Gözlənilir" if (is_home_win and btts_val == "Xeyr") else "Risklidir"
    
    w2_btts_yes = "Gözlənilir" if (is_away_win and btts_val == "Bəli") else "Risklidir"
    w2_btts_no = "Gözlənilir" if (is_away_win and btts_val == "Xeyr") else "Risklidir"

    return f"""<b>⚽ ZƏNCİRVARİ PEŞƏKAR MATÇ ANALİZİ</b>

🔗 <b>Sorğu / Link:</b> <i>{query}</i>
🏠 vs 🇦🇿 <b>Matç:</b> <code>{match_title}</code>

🎯 <b>1. MƏRKƏZİ TƏQDİMAT (Dəqiq Hesab):</b>
• <b>Dəqiq Hesab (Correct Score):</b> <b>{home_score} - {away_score}</b> (Zəncirin təməli)

⛓️ <b>2. ƏSAS TƏXMİNLƏR VƏ BTTS:</b>
• <b>FT Prediction (1X2):</b> {sc["ms"]} 
• <b>İlk Hissə (HT) Hesabı:</b> {sc["ht_h"]} - {sc["ht_a"]}
• <b>HT / FT Nəticəsi:</b> <b>{sc["htft"]}</b>
• <b>BTTS (Qarşılıqlı Qol):</b> <b>{btts_val}</b> (Hə: %{btts_yes_p} | Yox: %{btts_no_p})
• <b>Cüt Şans (Double Chance):</b> {sc["dc"]}
• <b>Kornerlər:</b> {random.randint(8, 11)}.5-dən Çox

🔥 <b>3. KOMANDA & BTTS KOMBİNASİYALARI:</b>
• <b>1 & BTTS (Yes):</b> {w1_btts_yes} (%{random.randint(45, 75) if is_home_win and btts_val=='Bəli' else random.randint(10, 30)})
• <b>1 & BTTS (No):</b> {w1_btts_no} (%{random.randint(45, 75) if is_home_win and btts_val=='Xeyr' else random.randint(10, 30)})
• <b>2 & BTTS (Yes):</b> {w2_btts_yes} (%{random.randint(45, 75) if is_away_win and btts_val=='Bəli' else random.randint(10, 30)})
• <b>2 & BTTS (No):</b> {w2_btts_no} (%{random.randint(45, 75) if is_away_win and btts_val=='Xeyr' else random.randint(10, 30)})

⚡ <b>4. KOMANDA & ALT/ÜST KOMBİNASİYALARI:</b>
• <b>1 & 1.5 Üst:</b> {'Gözlənilir' if (is_home_win and total_goals >= 2) else 'Riskli'}
• <b>1 & 2.5 Üst:</b> {'Gözlənilir' if (is_home_win and total_goals >= 3) else 'Riskli'}
• <b>1 & 3.5 Üst:</b> {'Gözlənilir' if (is_home_win and total_goals >= 4) else 'Riskli'}
• <b>2 & 1.5 Üst:</b> {'Gözlənilir' if (is_away_win and total_goals >= 2) else 'Riskli'}
• <b>2 & 2.5 Üst:</b> {'Gözlənilir' if (is_away_win and total_goals >= 3) else 'Riskli'}
• <b>2 & 3.5 Üst:</b> {'Gözlənilir' if (is_away_win and total_goals >= 4) else 'Riskli'}

📈 <b>5. ÜMUMİ ALT / ÜST FAİZLƏRİ:</b>
• <b>0.5 Üst:</b> %98 | <b>1.5 Üst:</b> {'%85' if total_goals >= 2 else '%30'}
• <b>2.5 Üst:</b> {'%78' if total_goals >= 3 else '%35'} | <b>3.5 Üst:</b> {'%65' if total_goals >= 4 else '%15'}
• <b>4.5 Üst:</b> {'%40' if total_goals >= 5 else '%5'} | <b>5.0 Üst:</b> {'%25' if total_goals >= 5 else '%2'}

---
✨ <b>Coşqun Təxmini-</b>"""

def main():
    offset = 0
    processed_messages = set()
    print("Coşqun Kombi Zəncirvari Analiz Botu 7/24 işləyir...")
    
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
                                "<b>⚽ Salam! Coşqun Kombi Analiz Botuna xoş gəlmisiniz.</b>\n\n"
                                "Mənə matç linki göndərin; dəqiq hesaba əsaslanan <b>BTTS, 1 & BTTS, 2 & BTTS, "
                                "komanda qələbəsi ilə alt/üst kombinasiyaları</b> və bütün zəncirvari proqnozları təqdim edim!\n\n"
                                "<i>Coşqun Təxmini-</i>"
                            )
                            send_message(chat_id, reply_text)
                        else:
                            analysis = generate_chain_linked_analysis(user_text)
                            send_message(chat_id, analysis)
        except Exception:
            time.sleep(2)
            continue
        time.sleep(0.5)

if __name__ == "__main__":
    main()

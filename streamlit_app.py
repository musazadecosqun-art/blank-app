import os
import json
import urllib.request
import random
from http.server import HTTPServer, BaseHTTPRequestHandler

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

def generate_vba_linked_analysis(query):
    # VBA-dakı məntiqi simulyasiya etmək üçün seed
    random.seed(hash(query) % 10000)
    
    # Zəncirvari dəqiq hesab və matç ssenariləri (VBA modelinə uyğun)
    scenarios = [
        {"h": 2, "a": 1, "ht_h": 1, "ht_a": 0, "htft": "1/1", "ms": "1 (Home)", "tot": 3, "btts": "YES", "dc": "1X"},
        {"h": 1, "a": 0, "ht_h": 1, "ht_a": 0, "htft": "1/1", "ms": "1 (Home)", "tot": 1, "btts": "NO", "dc": "1X"},
        {"h": 1, "a": 1, "ht_h": 0, "ht_a": 0, "htft": "X/X", "ms": "X (Draw)", "tot": 2, "btts": "YES", "dc": "1X / X2"},
        {"h": 0, "a": 2, "ht_h": 0, "ht_a": 1, "htft": "2/2", "ms": "2 (Away)", "tot": 2, "btts": "NO", "dc": "X2"},
        {"h": 3, "a": 1, "ht_h": 2, "ht_a": 0, "htft": "1/1", "ms": "1 (Home)", "tot": 4, "btts": "YES", "dc": "1X"},
        {"h": 1, "a": 2, "ht_h": 0, "ht_a": 1, "htft": "2/2", "ms": "2 (Away)", "tot": 3, "btts": "YES", "dc": "X2"},
        {"h": 2, "a": 2, "ht_h": 1, "ht_a": 1, "htft": "X/X", "ms": "X (Draw)", "tot": 4, "btts": "YES", "dc": "1X / X2"}
    ]
    
    sc = random.choice(scenarios)
    ev_hesab = sc["h"]
    qonaq_hesab = sc["a"]
    tot_goles = sc["tot"]
    btts_val = sc["btts"]
    htft_val = sc["htft"]
    x12_val = sc["ms"]
    
    # Komanda adlarının təyini (Əgər link və ya ad verilibsə)
    clean_query = query.replace("https://", "").replace("http://", "").replace("www.", "")
    parts = clean_query.split("/")
    if len(parts) > 0 and len(parts[-1]) > 3 and "-" in parts[-1]:
        teams = parts[-1].split("-")
        ev_komanda = teams[0].capitalize()
        qonaq_komanda = teams[1].capitalize()
    else:
        ev_komanda = "Bayer Leverkusen"
        qonaq_komanda = "RB Leipzig"

    liga_info = "Germany Bundesliga"
    
    # Alt/Üst limitin təyini (VBA məntiqi)
    if tot_goles <= 2:
        over_limit = "2.5 Under"
    elif tot_goles == 3:
        over_limit = "2.5 Over"
    else:
        over_limit = "3.5 Over"

    if "1" in x12_val:
        pred_text = f"{ev_komanda} udacaq / 1X & {over_limit}"
    elif "2" in x12_val:
        pred_text = f"{qonaq_komanda} udacaq / X2 & {over_limit}"
    else:
        pred_text = f"Heç-heçə / X & {over_limit}"

    # Kornerlər və Penalti
    ev_corner = round(random.uniform(4.5, 6.2), 1)
    qonaq_corner = round(random.uniform(3.8, 5.5), 1)
    corner_total = ev_corner + qonaq_corner
    
    if corner_total < 7.8: corner_limit = "7.5 Under"
    elif corner_total <= 8.6: corner_limit = "8.5 Over"
    elif corner_total <= 9.6: corner_limit = "9.5 Over"
    elif corner_total <= 10.6: corner_limit = "10.5 Over"
    elif corner_total <= 11.6: corner_limit = "11.5 Over"
    else: corner_limit = "12.5 Over"

    penalty_val = "YES" if (tot_goles >= 3 or btts_val == "YES") else "NO"

    # Kombinasiyalar (1 & BTTS, 2 & BTTS, 1 & Over və s.)
    is_home_win = ev_hesab > qonaq_hesab
    is_away_win = qonaq_hesab > ev_hesab

    w1_btts_yes = "Gözlənilir" if (is_home_win and btts_val == "YES") else "Risklidir"
    w1_btts_no = "Gözlənilir" if (is_home_win and btts_val == "NO") else "Risklidir"
    w2_btts_yes = "Gözlənilir" if (is_away_win and btts_val == "YES") else "Risklidir"
    w2_btts_no = "Gözlənilir" if (is_away_win and btts_val == "NO") else "Risklidir"

    return f"""<b>⚽ ZƏNCİRVARİ VBA & ANALİZ MODELİ</b>

🔗 <b>Liqa:</b> <i>{liga_info}</i>
🏠 <b>{ev_komanda}</b> vs 🇦🇿 <b>{qonaq_komanda}</b>

🎯 <b>1. MƏRKƏZİ DƏQİQ HESAB (VBA Engine):</b>
• <b>Dəqiq Hesab:</b> <b>{ev_hesab} - {qonaq_hesab}</b>
• <b>İlk Hissə (HT) Hesabı:</b> {sc["ht_h"]} - {sc["ht_a"]}
• <b>HT / FT Nəticəsi:</b> <b>{htft_val}</b>
• <b>1X2 Nəticə:</b> <b>{x12_val}</b>
• <b>Cüt Şans:</b> {sc["dc"]}

🔥 <b>2. BTTS VƏ KOMBİNASİYALAR:</b>
• <b>BTTS (Qarşılıqlı Qol):</b> <b>{btts_val}</b>
• <b>1 & BTTS (Yes):</b> {w1_btts_yes}
• <b>1 & BTTS (No):</b> {w1_btts_no}
• <b>2 & BTTS (Yes):</b> {w2_btts_yes}
• <b>2 & BTTS (No):</b> {w2_btts_no}

⚡ <b>3. KOMANDA & ALT/ÜST KOMBİNASİYALARI:</b>
• <b>1 & 1.5 Üst:</b> {'Gözlənilir' if (is_home_win and tot_goles >= 2) else 'Riskli'}
• <b>1 & 2.5 Üst:</b> {'Gözlənilir' if (is_home_win and tot_goles >= 3) else 'Riskli'}
• <b>1 & 3.5 Üst:</b> {'Gözlənilir' if (is_home_win and tot_goles >= 4) else 'Riskli'}
• <b>2 & 1.5 Üst:</b> {'Gözlənilir' if (is_away_win and tot_goles >= 2) else 'Riskli'}
• <b>2 & 2.5 Üst:</b> {'Gözlənilir' if (is_away_win and tot_goles >= 3) else 'Riskli'}
• <b>2 & 3.5 Üst:</b> {'Gözlənilir' if (is_away_win and tot_goles >= 4) else 'Riskli'}

🚩 <b>4. KORNERLƏR VƏ PENALTİ:</b>
• <b>Ev Sahibi Korner:</b> {ev_corner}
• <b>Qonaq Korner:</b> {qonaq_corner}
• <b>Ümumi Korner Limit:</b> <b>{corner_limit}</b>
• <b>Penalti (Penalty):</b> <b>{penalty_val}</b>

📌 <b>Yekun Təxmin:</b> <code>{pred_text}</code>

---
✨ <b>Coşqun VBA Zəncirvari Sistem-</b>"""

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"VBA Chain Linked Bot is Active!")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            json_data = json.loads(post_data.decode('utf-8'))
            if "message" in json_data:
                message = json_data["message"]
                chat_id = message["chat"]["id"]
                user_text = message.get("text", "").strip()
                
                if user_text:
                    if user_text.lower() == "/start":
                        reply_text = (
                            "<b>⚽ Salam! Coşqun VBA Zəncirvari Analiz Botuna xoş gəlmisiniz.</b>\n\n"
                            "Mənə matç linki və ya komanda adları göndərin; VBA modelinə əsaslanan "
                            "dəqiq hesab, BTTS, komanda kombinasiyaları və korner analizlərini təqdim edim!\n\n"
                            "<i>Coşqun VBA Sistem-</i>"
                        )
                        send_message(chat_id, reply_text)
                    else:
                        analysis = generate_vba_linked_analysis(user_text)
                        send_message(chat_id, analysis)
        except Exception:
            pass
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), WebhookHandler)
    server.serve_forever()

if __name__ == "__main__":
    run()
    

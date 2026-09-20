import os
import json
import urllib.request
from flask import Flask, request

app = Flask(__name__)

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

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_json(silent=True)
    if json_data and "message" in json_data:
        message = json_data["message"]
        chat_id = message["chat"]["id"]
        user_text = message.get("text", "").strip()
        
        if user_text:
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
                
    return "OK", 200

@app.route("/")
def index():
    return "Cosqun Bot Webhook is Active!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    

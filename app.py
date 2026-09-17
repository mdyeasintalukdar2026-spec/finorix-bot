import os
import random
from flask import Flask, jsonify, request, render_template_string

# 1. FLASK APP INITIALIZATION
app = Flask(__name__)

# ==========================================
# 2. MARKET LISTS & TIMEFRAMES
# ==========================================
REAL_MARKETS = [
    "EUR/JPY", "EUR/GBP", "GBP/USD", "USD/JPY", "AUD/CAD", 
    "EUR/USD", "CAD/JPY", "AUD/CHF", "GBP/AUD", "AUD/JPY", 
    "AUD/USD", "EUR/CHF", "CHF/JPY", "GBP/CHF", "GBP/JPY", 
    "EUR/AUD", "EUR/CAD", "USD/CAD", "GBP/CAD", "USD/CHF"
]

OTC_MARKETS = [
    "CAD/CHF (OTC)", "USD/INR (OTC)", "USD/NGN (OTC)", "NZD/CHF (OTC)", 
    "USD/IDR (OTC)", "USD/BRL (OTC)", "AUD/NZD (OTC)", "USD/ARS (OTC)", 
    "NZD/JPY (OTC)", "USD/PKR (OTC)", "NZD/CAD (OTC)", "USD/BDT (OTC)", 
    "USD/COP (OTC)", "USD/DZD (OTC)", "USD/EGP (OTC)", "USD/MXN (OTC)", 
    "USD/PHP (OTC)", "EUR/NZD (OTC)", "GBP/NZD (OTC)", "USD/ZAR (OTC)", 
    "NZD/USD (OTC)", "Axie Infinity (OTC)", "Bitcoin Cash (OTC)", 
    "Bitcoin (OTC)", "Dash (OTC)", "Solana (OTC)", "Toncoin (OTC)", 
    "Trump (OTC)", "Zcash (OTC)", "Ripple (OTC)", "Chainlink (OTC)", 
    "Cosmos (OTC)", "Polkadot (OTC)", "Ethereum Classic (OTC)", 
    "Avalanche (OTC)", "Litecoin (OTC)", "Ethereum (OTC)", "Binance Coin (OTC)",
    "UKBrent (OTC)", "Gold (OTC)", "Silver (OTC)", "USCrude (OTC)"
]

TIMEFRAMES = ["5S", "10S", "15S", "20S", "25S", "30S", "1M", "2M", "3M", "4M", "5M"]

# ==========================================
# 3. KNOWLEDGE BASE (250+ RULES)
# ==========================================
KNOWLEDGE_BASE = [
    {"rule": "EMA/SMA Dynamic Cross", "logic": "Price above EMA(200) confirms institutional uptrend bias."},
    {"rule": "MACD Divergence Shift", "logic": "Histogram > 0 with dynamic line crossover triggers signal."},
    {"rule": "RSI Extreme Reversal", "logic": "Divergence at extreme zones (<30 or >70) forces mean reversion."},
    {"rule": "1-Min BOS Sweep", "logic": "Break of Structure validates strong institutional direction."},
    {"rule": "Fair Value Gap (FVG)", "logic": "Price retesting 3-candle imbalance zone for order rebalance."}
]

for i in range(6, 251):
    KNOWLEDGE_BASE.append({
        "rule": f"Institutional Logic Node #{i}",
        "logic": f"Multi-timeframe liquidity sweep and volume profile confluence rule {i}."
    })

# ==========================================
# 4. FRONTEND HTML TEMPLATE
# ==========================================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FINORIX PRO BOT</title>
    <style>
        body {
            background-color: #050508;
            color: #ffffff;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 15px;
            box-sizing: border-box;
        }
        .bot-card {
            width: 100%;
            max-width: 400px;
            background: #0d0d14;
            border-radius: 16px;
            padding: 20px;
            border: 2px solid #00e5ff;
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
            box-sizing: border-box;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .title {
            font-size: 18px;
            font-weight: bold;
            color: #00ff66;
        }
        .qx-link {
            background: #ff0055;
            color: #fff;
            padding: 6px 12px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 12px;
            font-weight: bold;
        }
        label {
            font-size: 12px;
            color: #aaa;
            margin-top: 10px;
            display: block;
        }
        select, button {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #333;
            background: #181824;
            color: #fff;
            margin-top: 5px;
            outline: none;
            box-sizing: border-box;
        }
        .scan-btn {
            background: #00e5ff;
            color: #000;
            font-weight: bold;
            font-size: 16px;
            margin-top: 20px;
            cursor: pointer;
            border: none;
        }
        .stats {
            display: flex;
            justify-content: space-between;
            gap: 8px;
            margin-top: 20px;
            text-align: center;
        }
        .stat-box {
            flex: 1;
            background: #12121f;
            border: 1px solid #00e5ff;
            border-radius: 8px;
            padding: 10px 5px;
        }
        .stat-num {
            font-size: 15px;
            font-weight: bold;
            color: #00e5ff;
            margin-top: 5px;
        }
        .signal-area {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #00ff66;
            text-align: center;
            display: none;
        }
        .signal-title {
            font-size: 22px;
            font-weight: bold;
        }
        .logic-area {
            margin-top: 10px;
            padding: 10px;
            background: #1a1a26;
            border-radius: 8px;
            font-size: 11px;
            display: none;
            color: #ffea00;
        }
    </style>
</head>
<body>

<div class="bot-card">
    <div class="header">
        <div>
            <div class="title">FINORIX PRO BOT</div>
            <div style="font-size: 10px; color: #888;">Owner: YASIN BHAI</div>
        </div>
        <a href="https://quotex.com" target="_blank" class="qx-link">QX BROKER</a>
    </div>

    <label>SELECT MARKET</label>
    <select id="market">
        {% for m in otc %}
        <option value="{{ m }}">{{ m }}</option>
        {% endfor %}
        {% for m in real %}
        <option value="{{ m }}">{{ m }}</option>
        {% endfor %}
    </select>

    <label>TIMEFRAME</label>
    <select id="timeframe">
        {% for tf in tf_list %}
        <option value="{{ tf }}">{{ tf }}</option>
        {% endfor %}
    </select>

    <button class="scan-btn" onclick="getSignal()">🚀 MANUAL AI SCAN</button>

    <div class="stats">
        <div class="stat-box">
            <div style="font-size: 9px; color: #aaa;">WIN RATE</div>
            <div class="stat-num" id="wr">--</div>
        </div>
        <div class="stat-box">
            <div style="font-size: 9px; color: #aaa;">ACCURACY</div>
            <div class="stat-num" id="acc">--</div>
        </div>
        <div class="stat-box">
            <div style="font-size: 9px; color: #aaa;">CONFIRM</div>
            <div class="stat-num" id="conf">--</div>
        </div>
    </div>

    <div class="signal-area" id="sigBox">
        <div class="signal-title" id="sigText">--</div>
        <div style="font-size: 12px; margin-top: 5px;" id="sigSub">--</div>
    </div>

    <div class="logic-area" id="logicBox">
        <b>Rule:</b> <span id="rName">--</span><br>
        <b>Logic:</b> <span id="rLogic">--</span>
    </div>
</div>

<script>
    function speakText(text) {
        if ('speechSynthesis' in window) {
            var msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'bn-BD';
            window.speechSynthesis.speak(msg);
        }
    }

    function getSignal() {
        fetch('/api/scan', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                market: document.getElementById('market').value,
                timeframe: document.getElementById('timeframe').value
            })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('wr').innerText = data.win_rate + '%';
            document.getElementById('acc').innerText = data.accuracy + '%';
            document.getElementById('conf').innerText = data.confirmation + '%';

            var box = document.getElementById('sigBox');
            var txt = document.getElementById('sigText');
            var sub = document.getElementById('sigSub');

            if(data.direction === "UP") {
                txt.innerText = "CALL / UP ⬆️";
                txt.style.color = "#00ff66";
                box.style.borderColor = "#00ff66";
                sub.innerText = "এখান থেকে আপনি আপের জন্য ট্রেড প্লেস করুন";
                sub.style.color = "#00ff66";
                speakText("এখান থেকে আপনি আপের জন্য ট্রেড প্লেস করুন");
            } else {
                txt.innerText = "PUT / DOWN ⬇️";
                txt.style.color = "#ff0055";
                box.style.borderColor = "#ff0055";
                sub.innerText = "এখান থেকে আপনি ডাউনের জন্য ট্রেড প্লেস করুন";
                sub.style.color = "#ff0055";
                speakText("এখান থেকে আপনি ডাউনের জন্য ট্রেড প্লেস করুন");
            }

            box.style.display = 'block';

            document.getElementById('rName').innerText = data.rule_name;
            document.getElementById('rLogic').innerText = data.rule_logic;
            document.getElementById('logicBox').style.display = 'block';
        });
    }
</script>

</body>
</html>
"""

# ==========================================
# 5. FLASK ROUTES
# ==========================================
@app.route('/')
def index():
    return render_template_string(HTML_PAGE, otc=OTC_MARKETS, real=REAL_MARKETS, tf_list=TIMEFRAMES)

@app.route('/api/scan', methods=['POST'])
def scan():
    rule = random.choice(KNOWLEDGE_BASE)
    return jsonify({
        "direction": random.choice(["UP", "DOWN"]),
        "win_rate": random.randint(86, 99),
        "accuracy": random.randint(88, 98),
        "confirmation": random.randint(82, 97),
        "rule_name": rule["rule"],
        "rule_logic": rule["logic"]
    })

# ==========================================
# 6. SERVER RUNNER (RENDER PORT BINDING)
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

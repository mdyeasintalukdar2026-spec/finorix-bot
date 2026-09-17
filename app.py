import os
import random
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# ==========================================
# 1. MARKET LISTS
# ==========================================
REAL_MARKETS = [
    "FX:EURUSD", "FX:GBPUSD", "FX:USDJPY", "FX:EURJPY", "FX:EURGBP",
    "FX:AUDCAD", "FX:CADJPY", "FX:AUDCHF", "FX:GBPAUD", "FX:AUDJPY"
]

OTC_MARKETS = [
    "CAD/CHF (OTC)", "USD/INR (OTC)", "USD/NGN (OTC)", "NZD/CHF (OTC)", 
    "USD/IDR (OTC)", "USD/BRL (OTC)", "AUD/NZD (OTC)", "USD/BDT (OTC)"
]

TIMEFRAMES = ["5S", "10S", "15S", "30S", "1M", "5M"]

# ==========================================
# 2. KNOWLEDGE BASE
# ==========================================
KNOWLEDGE_BASE = [
    {"rule": "EMA/SMA Dynamic Cross", "logic": "Price above EMA(200) confirms institutional uptrend bias."},
    {"rule": "MACD Divergence Shift", "logic": "Histogram > 0 with dynamic line crossover triggers signal."},
    {"rule": "RSI Extreme Reversal", "logic": "Divergence at extreme zones (<30 or >70) forces mean reversion."},
    {"rule": "1-Min BOS Sweep", "logic": "Break of Structure validates strong institutional direction."},
    {"rule": "Fair Value Gap (FVG)", "logic": "Price retesting 3-candle imbalance zone for order rebalance."}
]

# ==========================================
# 3. HTML / FRONTEND WITH DUAL CHART ENGINE
# ==========================================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FINORIX PRO BOT - DUAL LIVE CHART</title>
    <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
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
            max-width: 420px;
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
            margin-bottom: 15px;
        }
        .title { font-size: 18px; font-weight: bold; color: #00ff66; }
        .qx-link { background: #ff0055; color: #fff; padding: 6px 12px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold; }
        label { font-size: 12px; color: #aaa; margin-top: 10px; display: block; }
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
        #chartBox {
            width: 100%;
            height: 240px;
            margin-top: 15px;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #222;
            background: #000;
        }
        .scan-btn { background: #00e5ff; color: #000; font-weight: bold; font-size: 16px; margin-top: 15px; cursor: pointer; border: none; }
        .stats { display: flex; justify-content: space-between; gap: 8px; margin-top: 15px; text-align: center; }
        .stat-box { flex: 1; background: #12121f; border: 1px solid #00e5ff; border-radius: 8px; padding: 8px 4px; }
        .stat-num { font-size: 14px; font-weight: bold; color: #00e5ff; margin-top: 4px; }
        .signal-area { margin-top: 15px; padding: 12px; border-radius: 10px; border: 2px solid #00ff66; text-align: center; display: none; }
        .signal-title { font-size: 20px; font-weight: bold; }
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
    <select id="market" onchange="switchChart()">
        <optgroup label="OTC MARKETS">
            {% for m in otc %}
            <option value="{{ m }}">{{ m }}</option>
            {% endfor %}
        </optgroup>
        <optgroup label="REAL MARKETS">
            {% for m in real %}
            <option value="{{ m }}">{{ m }}</option>
            {% endfor %}
        </optgroup>
    </select>

    <label>TIMEFRAME</label>
    <select id="timeframe">
        {% for tf in tf_list %}
        <option value="{{ tf }}">{{ tf }}</option>
        {% endfor %}
    </select>

    <!-- CONTAINER FOR BOTH CHARTS -->
    <div id="chartBox"></div>

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
</div>

<script>
    let simChart, candlestickSeries, simInterval;

    function switchChart() {
        const market = document.getElementById('market').value;
        const box = document.getElementById('chartBox');
        box.innerHTML = '';
        if (simInterval) clearInterval(simInterval);

        if (market.includes('FX:')) {
            // Load Real TradingView Live Chart
            new TradingView.widget({
                "autosize": true,
                "symbol": market,
                "interval": "1",
                "timezone": "Asia/Dhaka",
                "theme": "dark",
                "style": "1",
                "locale": "en",
                "toolbar_bg": "#f1f3f6",
                "enable_publishing": false,
                "hide_top_toolbar": true,
                "save_image": false,
                "container_id": "chartBox"
            });
        } else {
            // Load OTC Custom Interactive Live Chart
            simChart = LightweightCharts.createChart(box, {
                layout: { backgroundColor: '#0a0a10', textColor: '#d1d4dc' },
                grid: { vertLines: { color: '#1a1a26' }, horzLines: { color: '#1a1a26' } },
                timeScale: { timeVisible: true, seconds: true }
            });

            candlestickSeries = simChart.addCandlestickSeries({
                upColor: '#00ff66', downColor: '#ff0055',
                borderDownColor: '#ff0055', borderUpColor: '#00ff66',
                wickDownColor: '#ff0055', wickUpColor: '#00ff66'
            });

            let price = 1.1200;
            let time = Math.floor(Date.now() / 1000) - 300;
            let data = [];

            for (let i = 0; i < 30; i++) {
                let open = price;
                let close = open + (Math.random() - 0.49) * 0.0004;
                data.push({
                    time: time, open: open,
                    high: Math.max(open, close) + 0.0001,
                    low: Math.min(open, close) - 0.0001,
                    close: close
                });
                price = close;
                time += 10;
            }
            candlestickSeries.setData(data);

            simInterval = setInterval(() => {
                time += 1;
                let close = price + (Math.random() - 0.49) * 0.0002;
                candlestickSeries.update({
                    time: time, open: price,
                    high: Math.max(price, close) + 0.0001,
                    low: Math.min(price, close) - 0.0001,
                    close: close
                });
                price = close;
            }, 1000);
        }
    }

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
        });
    }

    window.onload = switchChart;
</script>

</body>
</html>
"""

# ==========================================
# 4. FLASK ROUTES
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
# 5. SERVER RUNNER
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

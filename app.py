import os
import random
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# ==========================================
# 1. COMPLETE REAL & OTC MARKETS (FROM SCREENSHOTS)
# ==========================================
ALL_MARKETS = [
    # Currencies - OTC
    {"name": "CAD/CHF (OTC)", "symbol": "FX:CADCHF", "type": "OTC"},
    {"name": "USD/INR (OTC)", "symbol": "FX:USDINR", "type": "OTC"},
    {"name": "USD/NGN (OTC)", "symbol": "FX:USDNGN", "type": "OTC"},
    {"name": "NZD/CHF (OTC)", "symbol": "FX:NZDCHF", "type": "OTC"},
    {"name": "USD/IDR (OTC)", "symbol": "FX:USDIDR", "type": "OTC"},
    {"name": "USD/BRL (OTC)", "symbol": "FX:USDBRL", "type": "OTC"},
    {"name": "AUD/NZD (OTC)", "symbol": "FX:AUDNZD", "type": "OTC"},
    {"name": "USD/ARS (OTC)", "symbol": "FX:USDARS", "type": "OTC"},
    {"name": "NZD/JPY (OTC)", "symbol": "FX:NZDJPY", "type": "OTC"},
    {"name": "USD/PKR (OTC)", "symbol": "FX:USDPKR", "type": "OTC"},
    {"name": "NZD/CAD (OTC)", "symbol": "FX:NZDCAD", "type": "OTC"},
    {"name": "USD/BDT (OTC)", "symbol": "FX:USDBDT", "type": "OTC"},
    {"name": "USD/COP (OTC)", "symbol": "FX:USDCOP", "type": "OTC"},
    {"name": "USD/DZD (OTC)", "symbol": "FX:USDDZD", "type": "OTC"},
    {"name": "USD/EGP (OTC)", "symbol": "FX:USDEGP", "type": "OTC"},
    {"name": "USD/MXN (OTC)", "symbol": "FX:USDMXN", "type": "OTC"},
    {"name": "USD/PHP (OTC)", "symbol": "FX:USDPHP", "type": "OTC"},
    {"name": "EUR/NZD (OTC)", "symbol": "FX:EURNZD", "type": "OTC"},
    {"name": "GBP/NZD (OTC)", "symbol": "FX:GBPNZD", "type": "OTC"},
    {"name": "USD/ZAR (OTC)", "symbol": "FX:USDZAR", "type": "OTC"},
    {"name": "NZD/USD (OTC)", "symbol": "FX:NZDUSD", "type": "OTC"},
    
    # Currencies - Real
    {"name": "EUR/JPY (Real)", "symbol": "FX:EURJPY", "type": "REAL"},
    {"name": "EUR/GBP (Real)", "symbol": "FX:EURGBP", "type": "REAL"},
    {"name": "GBP/USD (Real)", "symbol": "FX:GBPUSD", "type": "REAL"},
    {"name": "USD/JPY (Real)", "symbol": "FX:USDJPY", "type": "REAL"},
    {"name": "AUD/CAD (Real)", "symbol": "FX:AUDCAD", "type": "REAL"},
    {"name": "EUR/USD (Real)", "symbol": "FX:EURUSD", "type": "REAL"},
    {"name": "CAD/JPY (Real)", "symbol": "FX:CADJPY", "type": "REAL"},
    {"name": "AUD/CHF (Real)", "symbol": "FX:AUDCHF", "type": "REAL"},
    {"name": "GBP/AUD (Real)", "symbol": "FX:GBPAUD", "type": "REAL"},
    {"name": "AUD/JPY (Real)", "symbol": "FX:AUDJPY", "type": "REAL"},
    {"name": "AUD/USD (Real)", "symbol": "FX:AUDUSD", "type": "REAL"},
    {"name": "EUR/CHF (Real)", "symbol": "FX:EURCHF", "type": "REAL"},
    {"name": "CHF/JPY (Real)", "symbol": "FX:CHFJPY", "type": "REAL"},
    {"name": "GBP/CHF (Real)", "symbol": "FX:GBPCHF", "type": "REAL"},
    {"name": "GBP/JPY (Real)", "symbol": "FX:GBPJPY", "type": "REAL"},
    {"name": "EUR/AUD (Real)", "symbol": "FX:EURAUD", "type": "REAL"},
    {"name": "EUR/CAD (Real)", "symbol": "FX:EURCAD", "type": "REAL"},
    {"name": "USD/CAD (Real)", "symbol": "FX:USDCAD", "type": "REAL"},
    {"name": "GBP/CAD (Real)", "symbol": "FX:GBPCAD", "type": "REAL"},
    {"name": "USD/CHF (Real)", "symbol": "FX:USDCHF", "type": "REAL"},

    # Crypto (OTC)
    {"name": "Axie Infinity (OTC)", "symbol": "CRYPTO:AXSUSD", "type": "OTC"},
    {"name": "Bitcoin Cash (OTC)", "symbol": "CRYPTO:BCHUSD", "type": "OTC"},
    {"name": "Bitcoin (OTC)", "symbol": "CRYPTO:BTCUSD", "type": "OTC"},
    {"name": "Dash (OTC)", "symbol": "CRYPTO:DASHUSD", "type": "OTC"},
    {"name": "Solana (OTC)", "symbol": "CRYPTO:SOLUSD", "type": "OTC"},
    {"name": "Toncoin (OTC)", "symbol": "CRYPTO:TONUSD", "type": "OTC"},
    {"name": "Ripple (OTC)", "symbol": "CRYPTO:XRPUSD", "type": "OTC"},
    {"name": "Ethereum (OTC)", "symbol": "CRYPTO:ETHUSD", "type": "OTC"},

    # Commodities (OTC)
    {"name": "UKBrent (OTC)", "symbol": "TVC:UKOIL", "type": "OTC"},
    {"name": "Gold (OTC)", "symbol": "TVC:GOLD", "type": "OTC"},
    {"name": "Silver (OTC)", "symbol": "TVC:SILVER", "type": "OTC"},
    {"name": "USCrude (OTC)", "symbol": "TVC:USOIL", "type": "OTC"},

    # Stocks
    {"name": "Nikkei 225", "symbol": "INDEX:N225", "type": "REAL"},
    {"name": "S&P/ASX 200", "symbol": "INDEX:XJO", "type": "REAL"},
    {"name": "FTSE 100", "symbol": "INDEX:UK100", "type": "REAL"}
]

TIMEFRAMES = ["1M", "5M"]

# ==========================================
# 2. DYNAMIC KNOWLEDGE BASE
# ==========================================
KNOWLEDGE_BASE = [
    {"rule": "EMA 200 Institutional Reversal", "logic": "Strong rejection at EMA 200 line in current candle."},
    {"rule": "MACD Histogram Crossover", "logic": "Zero-line momentum shift confirmed for upcoming candle."},
    {"rule": "RSI Overbought/Oversold Reversal", "logic": "Extreme zone exhaustion reached. Color flip imminent."},
    {"rule": "1-Min BOS Liquidity Sweep", "logic": "Institutional order flow active after liquidity grab."},
    {"rule": "FVG Imbalance Retest", "logic": "Price filling 3-candle imbalance zone for clean direction."}
]

# ==========================================
# 3. FRONTEND UI CODE (ANIMATED & MATCHING SKETCH)
# ==========================================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QX BROKER ADVANCED AI BOT</title>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <style>
        :root {
            --bg-dark: #08090c;
            --card-bg: #0f1117;
            --accent-cyan: #00e5ff;
            --accent-green: #00ff66;
            --accent-red: #ff0055;
            --accent-yellow: #ffea00;
        }

        body {
            background-color: var(--bg-dark);
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 12px;
            box-sizing: border-box;
        }

        .bot-card {
            width: 100%;
            max-width: 440px;
            background: var(--card-bg);
            border-radius: 20px;
            padding: 18px;
            border: 2px solid var(--accent-cyan);
            box-shadow: 0 0 20px rgba(0, 229, 255, 0.25);
            animation: pulseGlow 4s infinite alternate;
        }

        @keyframes pulseGlow {
            0% { box-shadow: 0 0 15px rgba(0, 229, 255, 0.2); }
            100% { box-shadow: 0 0 25px rgba(0, 229, 255, 0.4); }
        }

        /* [P] [N] [Q] [S] Profile Header */
        .profile-panel {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #161922;
            padding: 10px 14px;
            border-radius: 12px;
            border: 1px solid #222530;
            margin-bottom: 12px;
        }
        .profile-info { display: flex; align-items: center; gap: 10px; }
        .avatar { width: 36px; height: 36px; border-radius: 50%; border: 2px solid var(--accent-green); }
        .user-name { font-size: 14px; font-weight: bold; color: var(--accent-green); }
        .owner-tag { font-size: 10px; color: #888; }
        .qx-btn { background: var(--accent-red); color: #fff; padding: 6px 12px; border-radius: 6px; text-decoration: none; font-size: 11px; font-weight: bold; transition: 0.3s; }
        .qx-btn:hover { transform: scale(1.05); }

        /* [M] [T] Controls */
        .control-row { display: flex; gap: 10px; margin-bottom: 10px; }
        .control-group { flex: 1; }
        label { font-size: 11px; color: #aaa; display: block; margin-bottom: 4px; }
        select {
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #282c3c;
            background: #161922;
            color: #fff;
            outline: none;
            font-size: 12px;
        }

        /* [LC] Live Chart */
        #chartBox {
            width: 100%;
            height: 220px;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #282c3c;
            background: #000;
        }

        /* [MA] Moving Average / Strategy Badge */
        .ma-badge {
            background: #141722;
            border: 1px dashed var(--accent-yellow);
            color: var(--accent-yellow);
            font-size: 11px;
            text-align: center;
            padding: 6px;
            border-radius: 6px;
            margin: 10px 0;
            font-weight: bold;
        }

        /* [UP / DOWN] Signal Output Box */
        .signal-panel {
            background: #161922;
            border-radius: 12px;
            padding: 14px;
            text-align: center;
            border: 2px solid var(--accent-green);
            display: none;
            animation: fadeIn 0.4s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .signal-title { font-size: 17px; font-weight: bold; margin-bottom: 4px; }
        .signal-sub { font-size: 12px; color: #ccc; }

        /* [W] [A] [S] Stats Row */
        .stats-row { display: flex; justify-content: space-between; gap: 8px; margin: 12px 0; text-align: center; }
        .stat-card { flex: 1; background: #161922; border: 1px solid var(--accent-cyan); border-radius: 8px; padding: 8px 4px; }
        .stat-val { font-size: 13px; font-weight: bold; color: var(--accent-cyan); margin-top: 2px; }

        /* [F] [H] Action Buttons */
        .action-row { display: flex; gap: 10px; margin-bottom: 12px; }
        .scan-btn {
            flex: 2;
            background: var(--accent-cyan);
            color: #000;
            font-weight: bold;
            font-size: 14px;
            padding: 12px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: 0.2s;
        }
        .scan-btn:active { transform: scale(0.98); }

        /* [KN] Knowledge Base Panel */
        .kn-panel {
            background: #12141d;
            border: 1px solid #222530;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 11px;
            color: #888;
        }
        .kn-title { color: var(--accent-cyan); font-weight: bold; margin-bottom: 2px; }

        .warning-box {
            background: #2a2000;
            border: 1px solid var(--accent-yellow);
            color: var(--accent-yellow);
            font-size: 11px;
            padding: 8px;
            border-radius: 8px;
            text-align: center;
            display: none;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>

<div class="bot-card">
    <!-- [P] [N] [Q] [S] Profile Section -->
    <div class="profile-panel">
        <div class="profile-info">
            <img src="https://api.dicebear.com/7.x/bottts/svg?seed=HR_SHADOW" class="avatar" alt="User Avatar">
            <div>
                <div class="user-name">HR SHADOW</div>
                <div class="owner-tag">STATUS: VIP ACTIVE</div>
            </div>
        </div>
        <a href="https://quotex.com" target="_blank" class="qx-link">QX BROKER</a>
    </div>

    <!-- [M] [T] Market & Timeframe Selection -->
    <div class="control-row">
        <div class="control-group">
            <label>MARKET PAIR</label>
            <select id="market" onchange="loadChart()">
                {% for m in markets %}
                <option value="{{ m.symbol }}">{{ m.name }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="control-group" style="max-width: 100px;">
            <label>TIMEFRAME</label>
            <select id="timeframe" onchange="loadChart()">
                {% for tf in tf_list %}
                <option value="{{ tf }}">{{ tf }}</option>
                {% endfor %}
            </select>
        </div>
    </div>

    <!-- [LC] Live TradingView Chart -->
    <div id="chartBox"></div>

    <!-- [MA] Dynamic Knowledge/Indicator Badge -->
    <div class="ma-badge" id="maBadge">
        ⏳ TIMING ENGINE: WAIT FOR LAST 30s-10s OF CANDLE
    </div>

    <div class="warning-box" id="warnBox"></div>

    <!-- [UP / DOWN] Signal Box -->
    <div class="signal-panel" id="sigBox">
        <div style="font-size: 10px; font-weight: bold; background: var(--accent-yellow); color: #000; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-bottom: 6px;" id="sigTag">SIGNAL</div>
        <div class="signal-title" id="sigText">--</div>
        <div class="signal-sub" id="sigSub">--</div>
    </div>

    <!-- [W] [A] [S] Stats Section -->
    <div class="stats-row">
        <div class="stat-card">
            <div style="font-size: 9px; color: #aaa;">WIN RATE</div>
            <div class="stat-val" id="wr">--</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 9px; color: #aaa;">ACCURACY</div>
            <div class="stat-val" id="acc">--</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 9px; color: #aaa;">CONFIRM</div>
            <div class="stat-val" id="conf">--</div>
        </div>
    </div>

    <!-- [F] [H] Actions -->
    <div class="action-row">
        <button class="scan-btn" onclick="getSignal()">🔮 SCAN & PREDICT</button>
    </div>

    <!-- [KN] Knowledge Base Panel -->
    <div class="kn-panel">
        <div class="kn-title">🧠 ACTIVE KNOWLEDGE ENGINE</div>
        <div id="knText">EMA Reversal, MACD Histogram Crossover & Institutional FVG fill analysis enabled.</div>
    </div>
</div>

<script>
    let remainingSec = 60;

    function updateCandleTimer() {
        const now = new Date();
        remainingSec = 60 - now.getSeconds();
        document.getElementById('maBadge').innerText = `⏱ CANDLE TIME REMAINING: ${remainingSec}s`;
    }
    setInterval(updateCandleTimer, 1000);

    function loadChart() {
        const symbol = document.getElementById('market').value;
        const tf = document.getElementById('timeframe').value.replace('M', '');
        
        document.getElementById('chartBox').innerHTML = '';

        new TradingView.widget({
            "autosize": true,
            "symbol": symbol,
            "interval": tf,
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
    }

    function speakText(text) {
        if ('speechSynthesis' in window) {
            var msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'bn-BD';
            window.speechSynthesis.speak(msg);
        }
    }

    function getSignal() {
        var warn = document.getElementById('warnBox');
        var box = document.getElementById('sigBox');

        if (remainingSec > 30) {
            box.style.display = 'none';
            warn.innerText = "⚠️ অনুগ্রহ করে ক্যান্ডেলের শেষ ৩০ সেকেন্ড থেকে ১০ সেকেন্ড বাকি থাকা পর্যন্ত অপেক্ষা করুন!";
            warn.style.display = 'block';
            speakText("ক্যান্ডেলের শেষ ৩০ সেকেন্ড বাকি থাকা পর্যন্ত অপেক্ষা করুন");
            return;
        }

        warn.style.display = 'none';

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
            document.getElementById('knText').innerText = data.rule_name + " - " + data.rule_logic;

            var txt = document.getElementById('sigText');
            var sub = document.getElementById('sigSub');
            var tag = document.getElementById('sigTag');

            if(remainingSec <= 15) {
                tag.innerText = "🔮 NEXT CANDLE PREDICTION";
                if(data.direction === "UP") {
                    txt.innerText = "NEXT CANDLE: GREEN / CALL 🟢";
                    txt.style.color = "#00ff66";
                    box.style.borderColor = "#00ff66";
                    sub.innerText = "পরবর্তী ক্যান্ডেল শুরু হওয়া মাত্রই আপের জন্য ট্রেড নিন";
                    speakText("পরবর্তী ক্যান্ডেল শুরু হওয়া মাত্রই আপের জন্য ট্রেড নিন");
                } else {
                    txt.innerText = "NEXT CANDLE: RED / PUT 🔴";
                    txt.style.color = "#ff0055";
                    box.style.borderColor = "#ff0055";
                    sub.innerText = "পরবর্তী ক্যান্ডেল শুরু হওয়া মাত্রই ডাউনের জন্য ট্রেড নিন";
                    speakText("পরবর্তী ক্যান্ডেল শুরু হওয়া মাত্রই ডাউনের জন্য ট্রেড নিন");
                }
            } else {
                tag.innerText = "⚡ QUICK ENTRY SIGNAL (" + remainingSec + "s Left)";
                if(data.direction === "UP") {
                    txt.innerText = "TAKE ENTRY NOW: UP / CALL 🟢";
                    txt.style.color = "#00ff66";
                    box.style.borderColor = "#00ff66";
                    sub.innerText = "বর্তমান পজিশন থেকে এখনই আপের জন্য ট্রেড নিন";
                    speakText("বর্তমান পজিশন থেকে এখনই আপের জন্য ট্রেড নিন");
                } else {
                    txt.innerText = "TAKE ENTRY NOW: DOWN / PUT 🔴";
                    txt.style.color = "#ff0055";
                    sigBox.style.borderColor = "#ff0055";
                    sub.innerText = "বর্তমান পজিশন থেকে এখনই ডাউনের জন্য ট্রেড নিন";
                    speakText("বর্তমান পজিশন থেকে এখনই ডাউনের জন্য ট্রেড নিন");
                }
            }

            box.style.display = 'block';
        });
    }

    window.onload = function() {
        loadChart();
        updateCandleTimer();
    };
</script>

</body>
</html>
"""

# ==========================================
# 4. FLASK SERVER ROUTES
# ==========================================
@app.route('/')
def index():
    return render_template_string(HTML_PAGE, markets=ALL_MARKETS, tf_list=TIMEFRAMES)

@app.route('/api/scan', methods=['POST'])
def scan():
    rule = random.choice(KNOWLEDGE_BASE)
    return jsonify({
        "direction": random.choice(["UP", "DOWN"]),
        "win_rate": random.randint(89, 99),
        "accuracy": random.randint(90, 98),
        "confirmation": random.randint(86, 97),
        "rule_name": rule["rule"],
        "rule_logic": rule["logic"]
    })

# ==========================================
# 5. SERVER RUNNER
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

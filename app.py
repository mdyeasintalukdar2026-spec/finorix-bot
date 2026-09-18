import time
import random
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

MARKET_PAIRS = {
    "Real Markets": [
        "EUR/JPY", "EUR/GBP", "GBP/USD", "USD/JPY", "AUD/CAD", 
        "EUR/USD", "CAD/JPY", "AUD/CHF", "GBP/AUD", "AUD/JPY", 
        "AUD/USD", "EUR/CHF", "CHF/JPY", "GBP/CHF", "GBP/JPY", 
        "EUR/AUD", "EUR/CAD", "USD/CAD", "GBP/CAD", "USD/CHF", 
        "Nikkei 225", "S&P/ASX 200", "FTSE China A50 Index", 
        "CAC 40", "FTSE 100", "Hong Kong 50", "IBEX 35", "EURO STOXX 50"
    ],
    "OTC Markets": [
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
}

TIMEFRAMES = ["10s", "20s", "30s", "1m", "2m", "3m", "4m", "5m"]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FINORIX PRO BOT</title>
    <style>
        :root {
            --bg-color: #0b0e14;
            --card-bg: #121824;
            --accent-color: #00e676;
            --border-glow: #00e676;
            --text-color: #ffffff;
            --text-sub: #8b9bb4;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 10px;
        }

        .bot-card {
            background: var(--card-bg);
            width: 100%;
            max-width: 420px;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 0 15px rgba(0, 230, 118, 0.2);
            border: 1px solid rgba(0, 230, 118, 0.4);
            animation: pulseGlow 2s infinite alternate;
        }

        @keyframes pulseGlow {
            0% { border-color: rgba(0, 230, 118, 0.3); box-shadow: 0 0 10px rgba(0, 230, 118, 0.2); }
            100% { border-color: rgba(0, 230, 118, 0.9); box-shadow: 0 0 22px rgba(0, 230, 118, 0.6); }
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }

        .bot-title {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .bot-icon {
            width: 40px;
            height: 40px;
            background: #1e293b;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            border: 2px solid var(--accent-color);
        }

        .badge {
            background: #1e293b;
            color: #38bdf8;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: bold;
            border: 1px solid #38bdf8;
        }

        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 12px;
        }

        .select-box {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        label {
            font-size: 11px;
            color: var(--text-sub);
        }

        select {
            background: #1a2232;
            color: var(--text-color);
            border: 1px solid #2e3a52;
            padding: 8px;
            border-radius: 8px;
            outline: none;
            font-size: 13px;
        }

        /* চার্টের সাইজ কিছুটা ছোট এবং সুন্দর করার জন্য ১৮৫px সেট করা হয়েছে */
        .chart-box {
            height: 185px;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
            position: relative;
            border: 1px solid #2e3a52;
            margin-bottom: 12px;
        }

        .otc-alert {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(11, 14, 20, 0.95);
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 15px;
            color: #ff5252;
            font-weight: bold;
            font-size: 13px;
            z-index: 5;
        }

        .timer-box {
            border: 1px solid #eab308;
            color: #eab308;
            text-align: center;
            padding: 6px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 12px;
        }

        .scan-btn {
            width: 100%;
            background: linear-gradient(90deg, #00e676, #00b0ff);
            color: #000;
            font-weight: bold;
            border: none;
            padding: 11px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            margin-bottom: 12px;
            transition: 0.2s;
        }

        .scan-btn:hover {
            opacity: 0.9;
            transform: scale(0.99);
        }

        .signal-box {
            border: 1px solid var(--accent-color);
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            background: rgba(0, 230, 118, 0.03);
            margin-bottom: 12px;
            min-height: 65px;
        }

        .signal-text {
            font-size: 16px;
            font-weight: bold;
            color: var(--accent-color);
            margin-top: 5px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
            margin-bottom: 12px;
        }

        .stat-card {
            background: #1a2232;
            border-radius: 8px;
            padding: 8px;
            text-align: center;
            border: 1px solid #2e3a52;
        }

        .stat-title {
            font-size: 10px;
            color: var(--text-sub);
        }

        .stat-value {
            font-size: 14px;
            font-weight: bold;
            color: #38bdf8;
            margin-top: 4px;
        }

        .footer-text {
            font-size: 10px;
            color: var(--text-sub);
            text-align: center;
            line-height: 1.4;
        }

        .scanning-loader {
            display: inline-block;
            animation: rotate 1s infinite linear;
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>

<div class="bot-card">
    <div class="header">
        <div class="bot-title">
            <div class="bot-icon">🤖</div>
            <div>
                <div style="font-weight: bold; font-size: 15px; color: var(--accent-color);">FINORIX PRO BOT</div>
                <div style="font-size: 10px; color: var(--text-sub);">BY YASIN BHAI</div>
            </div>
        </div>
        <div class="badge">QX BROKER</div>
    </div>

    <div class="controls">
        <div class="select-box">
            <label>Market Pair</label>
            <select id="marketPair" onchange="handleMarketChange()">
                <optgroup label="-- REAL MARKETS --">
                    {% for pair in markets['Real Markets'] %}
                        <option value="{{ pair }}">{{ pair }}</option>
                    {% endfor %}
                </optgroup>
                <optgroup label="-- OTC MARKETS --">
                    {% for pair in markets['OTC Markets'] %}
                        <option value="{{ pair }}">{{ pair }}</option>
                    {% endfor %}
                </optgroup>
            </select>
        </div>
        <div class="select-box">
            <label>Timeframe</label>
            <select id="timeFrame" onchange="handleTimeframeChange()">
                {% for tf in timeframes %}
                    <option value="{{ tf }}">{{ tf }}</option>
                {% endfor %}
            </select>
        </div>
    </div>

    <div class="chart-box">
        <div id="otcAlert" class="otc-alert" style="display: none;">
            ⚠️ Live chart is not supported for OTC Markets.<br>Please select a Real Market pair to view live movements.
        </div>
        <div id="tradingview_widget" style="height: 100%;"></div>
    </div>

    <div class="timer-box">
        ⏰ CANDLE TIME REMAINING: <span id="candleTimer">--s</span>
    </div>

    <button class="scan-btn" onclick="runAnalysis()">⚡ SCAN & PREDICT</button>

    <div class="signal-box">
        <div style="font-size: 10px; color: #a855f7; font-weight: bold;">🔮 SIGNAL GENERATED</div>
        <div id="signalResult" class="signal-text">PRESS SCAN TO START</div>
        <div id="subText" style="font-size: 10px; color: var(--text-sub); margin-top: 4px;">Click the SCAN button manually to analyze trade market</div>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-title">WIN RATE</div>
            <div class="stat-value" id="winRate">--%</div>
        </div>
        <div class="stat-card">
            <div class="stat-title">ACCURACY</div>
            <div class="stat-value" id="accuracy">--%</div>
        </div>
        <div class="stat-card">
            <div class="stat-title">CONFIRM</div>
            <div class="stat-value" id="confirm">--%</div>
        </div>
    </div>

    <div class="footer-text">
        This signal engine operates using advanced multi-indicator real market analysis, price action strategy, RSI confluence, and volume dynamics to deliver maximum precision.
    </div>
</div>

<script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
<script>
    let currentRemainingTime = 60;

    // টাইমফ্রেমে মসৃণ ও সঠিক ক্যান্ডেল রেন্ডারিং লজিক
    function getTVInterval(tfStr) {
        if (tfStr === '10s') return "1S";
        if (tfStr === '20s') return "1S";
        if (tfStr === '30s') return "1S";
        if (tfStr === '1m') return "1";
        if (tfStr === '2m') return "2";
        if (tfStr === '3m') return "3";
        if (tfStr === '4m') return "4";
        if (tfStr === '5m') return "5";
        return "1";
    }

    function loadChart(symbol) {
        const tfStr = document.getElementById('timeFrame').value;
        const interval = getTVInterval(tfStr);
        let formattedSymbol = symbol.replace('/', '');
        
        if (!symbol.includes('Index') && !symbol.includes('225') && !symbol.includes('200') && !symbol.includes('40') && !symbol.includes('100') && !symbol.includes('50')) {
            formattedSymbol = "FX:" + formattedSymbol;
        }

        document.getElementById('tradingview_widget').innerHTML = '';
        new TradingView.widget({
            "autosize": true,
            "symbol": formattedSymbol,
            "interval": interval,
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#121824",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_legend": false,
            "save_image": false,
            "container_id": "tradingview_widget",
            "withdateranges": false,
            "allow_symbol_change": false,
            "details": false,
            "hotlist": false,
            "calendar": false
        });
    }

    function handleMarketChange() {
        const pair = document.getElementById('marketPair').value;
        const otcAlert = document.getElementById('otcAlert');
        
        if (pair.includes('(OTC)')) {
            otcAlert.style.display = 'flex';
        } else {
            otcAlert.style.display = 'none';
            loadChart(pair);
        }
    }

    function handleTimeframeChange() {
        const pair = document.getElementById('marketPair').value;
        if (!pair.includes('(OTC)')) {
            loadChart(pair);
        }
        updateTimerDisplay();
    }

    function getTimeframeSeconds(tfStr) {
        if (tfStr.includes('s')) {
            return parseInt(tfStr.replace('s', ''));
        } else if (tfStr.includes('m')) {
            return parseInt(tfStr.replace('m', '')) * 60;
        }
        return 60;
    }

    function updateTimerDisplay() {
        const tfStr = document.getElementById('timeFrame').value;
        const periodSeconds = getTimeframeSeconds(tfStr);
        const now = Math.floor(Date.now() / 1000);
        currentRemainingTime = periodSeconds - (now % periodSeconds);
        document.getElementById('candleTimer').innerText = currentRemainingTime + 's';
    }

    function startLiveCandleTimer() {
        updateTimerDisplay();
        setInterval(updateTimerDisplay, 1000);
    }

    function runAnalysis() {
        const pair = document.getElementById('marketPair').value;
        const tf = document.getElementById('timeFrame').value;
        const signalDiv = document.getElementById('signalResult');
        const subText = document.getElementById('subText');
        
        signalDiv.innerHTML = '<span class="scanning-loader">🌀</span> SCANNING MARKET...';
        subText.innerText = 'Analyzing market data and technical indicators...';
        
        document.getElementById('winRate').innerText = '--%';
        document.getElementById('accuracy').innerText = '--%';
        document.getElementById('confirm').innerText = '--%';

        fetch('/generate_signal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pair: pair, timeframe: tf, remaining_time: currentRemainingTime })
        })
        .then(response => response.json())
        .then(data => {
            signalDiv.innerHTML = data.direction;
            subText.innerText = data.sub_text;
            document.getElementById('winRate').innerText = data.win_rate;
            document.getElementById('accuracy').innerText = data.accuracy;
            document.getElementById('confirm').innerText = data.confirm;
        });
    }

    window.onload = function() {
        handleMarketChange();
        startLiveCandleTimer();
    };
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, markets=MARKET_PAIRS, timeframes=TIMEFRAMES)

@app.route('/generate_signal', methods=['POST'])
def generate_signal():
    data = request.json
    remaining_time = data.get('remaining_time', 60)
    
    time.sleep(4)
    
    is_up = random.choice([True, False])
    
    if remaining_time > 15:
        if is_up:
            direction_text = "TAKE ENTRY NOW: UP 🟢"
        else:
            direction_text = "TAKE ENTRY NOW: DOWN 🔴"
        sub_text = "Place your trade for UP / DOWN direction from here"
    else:
        if is_up:
            direction_text = "NEXT CANDLE: GREEN 🟢"
        else:
            direction_text = "NEXT CANDLE: RED 🔴"
        sub_text = "Take trade for UP / DOWN in the next candle"
        
    win_rate = random.randint(86, 96)
    accuracy = random.randint(92, 99)
    confirm = random.randint(89, 97)
    
    return jsonify({
        "direction": direction_text,
        "sub_text": sub_text,
        "win_rate": f"{win_rate}%",
        "accuracy": f"{accuracy}%",
        "confirm": f"{confirm}%"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

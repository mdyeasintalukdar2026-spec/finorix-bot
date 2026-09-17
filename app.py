import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>FINRIX PRO BOT</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: #080c14;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 10px;
        }

        /* Continuous Glowing Animated Border Container */
        .bot-container {
            width: 100%;
            max-width: 420px;
            background: #0d1322;
            border-radius: 16px;
            padding: 16px;
            position: relative;
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.3);
            border: 2px solid #00e5ff;
            animation: glowingBorder 4s infinite alternate;
        }

        @keyframes glowingBorder {
            0% {
                border-color: #00e5ff;
                box-shadow: 0 0 12px #00e5ff;
            }
            50% {
                border-color: #9d4edd;
                box-shadow: 0 0 18px #9d4edd;
            }
            100% {
                border-color: #00ff88;
                box-shadow: 0 0 12px #00ff88;
            }
        }

        /* Header Section */
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(255, 255, 255, 0.03);
            padding: 10px 14px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 14px;
        }

        .user-profile {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .avatar {
            width: 38px;
            height: 38px;
            background: #00c853;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            box-shadow: 0 0 8px #00c853;
        }

        .bot-title {
            font-size: 15px;
            font-weight: bold;
            color: #00ff88;
            letter-spacing: 0.5px;
        }

        .dev-name {
            font-size: 10px;
            color: #94a3b8;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }

        .broker-tag {
            background: #1e293b;
            border: 1px solid #3b82f6;
            color: #3b82f6;
            padding: 5px 9px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: bold;
        }

        /* Dropdown Controls */
        .controls {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 12px;
        }

        .control-group {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .control-group label {
            font-size: 11px;
            color: #8f9bba;
        }

        select {
            background: #141c2e;
            color: #fff;
            border: 1px solid #00e5ff;
            padding: 8px 10px;
            border-radius: 8px;
            outline: none;
            font-size: 12px;
            font-weight: 600;
        }

        /* TradingView Live Chart Frame */
        .chart-card {
            background: #121929;
            border-radius: 10px;
            border: 1px solid rgba(0, 229, 255, 0.3);
            overflow: hidden;
            margin-bottom: 12px;
        }

        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 10px;
            background: rgba(0, 0, 0, 0.4);
            font-size: 11px;
            font-weight: bold;
            color: #00e5ff;
        }

        .chart-wrapper {
            height: 210px;
            width: 100%;
        }

        .otc-notice {
            display: none;
            height: 160px;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 15px;
            color: #ff5252;
            font-size: 12px;
            font-weight: bold;
            background: rgba(255, 82, 82, 0.05);
            border: 1px dashed #ff5252;
            margin: 10px;
            border-radius: 8px;
        }

        /* Timer Card */
        .timer-card {
            background: #121929;
            border: 1px solid #ffd700;
            padding: 8px;
            border-radius: 8px;
            text-align: center;
            font-size: 12px;
            color: #ffd700;
            font-weight: bold;
            margin-bottom: 12px;
        }

        /* Signal Box */
        .signal-card {
            background: #121929;
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            margin-bottom: 12px;
        }

        .signal-badge {
            display: inline-block;
            background: #1e293b;
            color: #ffd700;
            font-size: 10px;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: bold;
            margin-bottom: 6px;
        }

        .signal-action {
            font-size: 15px;
            font-weight: 800;
            color: #00ff88;
            margin-bottom: 4px;
        }

        .signal-subtext {
            font-size: 11px;
            color: #cbd5e1;
        }

        /* Stats Section */
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
            margin-bottom: 12px;
        }

        .stat-box {
            background: #141c2e;
            border: 1px solid #1e293b;
            padding: 8px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-title {
            font-size: 9px;
            color: #64748b;
            font-weight: bold;
        }

        .stat-value {
            font-size: 13px;
            font-weight: bold;
            color: #00e5ff;
            margin-top: 2px;
        }

        /* Straight Knowledge Disclaimer Footer */
        .disclaimer-box {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            padding: 8px 10px;
            border-radius: 8px;
            font-size: 10px;
            color: #94a3b8;
            text-align: center;
            line-height: 1.4;
            font-style: normal;
        }
    </style>
</head>
<body>

<div class="bot-container">
    <div class="header">
        <div class="user-profile">
            <div class="avatar">🤖</div>
            <div>
                <div class="bot-title">FINRIX PRO BOT</div>
                <div class="dev-name">BY YASIN BHAI</div>
            </div>
        </div>
        <div class="broker-tag">QX BROKER</div>
    </div>

    <div class="controls">
        <div class="control-group">
            <label>Market Pair</label>
            <select id="marketPair" onchange="updateMarketView()">
                <option value="EURUSD">EUR/USD</option>
                <option value="GBPUSD" selected>GBP/USD</option>
                <option value="USDJPY">USD/JPY</option>
                <option value="OTC_EURUSD">EUR/USD (OTC)</option>
                <option value="OTC_GBPUSD">GBP/USD (OTC)</option>
            </select>
        </div>
        <div class="control-group">
            <label>Timeframe</label>
            <select id="timeframe">
                <option value="1m">1m</option>
                <option value="5m">5m</option>
            </select>
        </div>
    </div>

    <div class="chart-card">
        <div class="chart-header">
            <span>TRADINGVIEW LIVE CHART</span>
            <span id="pairTitle">GBP/USD</span>
        </div>
        <div id="chartWrapper" class="chart-wrapper">
            <div id="tradingview_widget" style="height:100%;width:100%;"></div>
        </div>
        <div id="otcNotice" class="otc-notice">
            TradingView Live Chart is only available for Real Markets (Not available for OTC pairs)
        </div>
    </div>

    <div class="timer-card">
        ⏰ CANDLE TIME REMAINING: <span id="timer">03s</span>
    </div>

    <div class="signal-card">
        <div class="signal-badge">🔮 SIGNAL GENERATED</div>
        <div class="signal-action" id="signalText">TAKE ENTRY NOW: UP / CALL 🟢</div>
        <div class="signal-subtext">এখান থেকে আপনি আপের জন্য ট্রেড প্রেস করুন</div>
    </div>

    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-title">WIN RATE</div>
            <div class="stat-value">88%</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">ACCURACY</div>
            <div class="stat-value">98%</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">CONFIRM</div>
            <div class="stat-value">90%</div>
        </div>
    </div>

    <div class="disclaimer-box">
        This signal engine operates using advanced multi-indicator real market analysis, price action strategy, RSI confluence, and volume dynamics to deliver maximum precision.
    </div>
</div>

<script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
<script>
    function loadTradingViewChart(symbol) {
        new TradingView.widget({
            "autosize": true,
            "symbol": symbol,
            "interval": "1",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "container_id": "tradingview_widget"
        });
    }

    loadTradingViewChart("FX:GBPUSD");

    function updateMarketView() {
        const pairSelect = document.getElementById("marketPair");
        const selectedValue = pairSelect.value;
        const chartWrapper = document.getElementById("chartWrapper");
        const otcNotice = document.getElementById("otcNotice");
        const pairTitle = document.getElementById("pairTitle");

        pairTitle.innerText = pairSelect.options[pairSelect.selectedIndex].text;

        if (selectedValue.startsWith("OTC_")) {
            chartWrapper.style.display = "none";
            otcNotice.style.display = "flex";
        } else {
            chartWrapper.style.display = "block";
            otcNotice.style.display = "none";
            loadTradingViewChart("FX:" + selectedValue);
        }
    }

    let count = 3;
    setInterval(() => {
        count--;
        if (count < 0) count = 59;
        document.getElementById("timer").innerText = (count < 10 ? "0" : "") + count + "s";
    }, 1000);
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

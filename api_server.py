from flask import Flask, jsonify, request, render_template_string
import os
from sharesansarscraper import scrapesharesarstock    }

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ShareSansar Stock API</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background-color: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }
        h1 { color: #333; text-align: center; }
        .input-group { margin: 20px 0; }
        input { width: 70%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 5px; }
        button { width: 25%; padding: 10px; font-size: 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; margin-left: 10px; }
        button:hover { background-color: #45a049; }
        .output { background-color: #f9f9f9; padding: 20px; border-radius: 5px; border-left: 4px solid #4CAF50; margin-top: 20px; overflow-x: auto; max-height: 500px; overflow-y: auto; }
        pre { margin: 0; white-space: pre-wrap; word-wrap: break-word; font-size: 12px; }
        .api-docs { margin-top: 30px; padding: 20px; background-color: #e8f5e9; border-radius: 5px; }
        .endpoint { background-color: #fff; padding: 10px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #2196F3; }
        code { background-color: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: monospace; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>ShareSansar Stock API</h1>
        <div class="input-group">
            <input type="text" id="ticker" placeholder="Enter stock ticker (e.g., ghl, nabil, trh)">
            <button onclick="fetchStock()">Get Data</button>
        </div>
        <div id="output" class="output" style="display:none">
            <pre id="result"></pre>
        </div>
        <div class="api-docs">
            <h3>API Endpoints</h3>
            <div class="endpoint">
                <strong>GET /api/stock/&lt;ticker&gt;</strong>
                <p>Get stock data for a specific ticker</p>
                <p>Example: <code>GET /api/stock/ghl</code></p>
            </div>
            <div class="endpoint">
                <strong>GET /api/stock?ticker=&lt;ticker&gt;</strong>
                <p>Alternative way to get stock data</p>
                <p>Example: <code>GET /api/stock?ticker=nabil</code></p>
            </div>
            <div class="endpoint">
                <strong>GET /</strong>
                <p>This web interface</p>
            </div>
        </div>
    </div>
    <script>
        function fetchStock() {
            const ticker = document.getElementById('ticker').value.trim();
            if (!ticker) { alert('Please enter a ticker symbol'); return; }
            fetch('/api/stock/' + ticker)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').textContent = JSON.stringify(data, null, 2);
                    document.getElementById('output').style.display = 'block';
                })
                .catch(error => {
                    document.getElementById('result').textContent = 'Error: ' + error;
                    document.getElementById('output').style.display = 'block';
                });
        }
        // Allow Enter key to submit
        document.getElementById('ticker').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') fetchStock();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page with web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock_by_path(ticker):
    """Get stock data via URL path parameter"""
    try:
        data = scrapesharesarstock(ticker)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stock', methods=['GET'])
def get_stock_by_query():
    """Get stock data via query parameter"""
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Ticker parameter is required"}), 400
    try:
        data = scrapesharesarstock(ticker)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print('=' * 60)
    print('ShareSansar Stock API Server Starting...')
    print('=' * 60)
    print('Server running at http://localhost:5000')
    print('Available endpoints:')
    print('  Web Interface: http://localhost:5000/')
    print('  API Endpoint: http://localhost:5000/api/stock/<ticker>')
    print('  Example API calls:')
    print('    http://localhost:5000/api/stock/ghl')
    print('    http://localhost:5000/api/stock/nabil')
    print('    http://localhost:5000/api/stock?ticker=trh')
    print('Press CTRL+C to stop the server')
    print('=' * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

DATA_FILE = 'portfolio.json'

# Load portfolio from file if exists
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        portfolio = json.load(f)
else:
    portfolio = {}

# Helper to save portfolio to file

def save_portfolio():
    with open(DATA_FILE, 'w') as f:
        json.dump(portfolio, f)

@app.route('/')
def index():
    return render_template_string("""
    <h1>Finfily Portfolio</h1>
    <p>Add assets via /add endpoint (POST JSON)</p>
    <p>Update prices via /update endpoint (POST JSON)</p>
    <p>View portfolio: <a href='/portfolio'>/portfolio</a></p>
    """)

@app.route('/portfolio')
def get_portfolio():
    items = []
    for name, data in portfolio.items():
        qty = data['quantity']
        buy = data['buy_price']
        current = data.get('current_price', buy)
        pnl = (current - buy) * qty
        items.append({'name': name, 'quantity': qty, 'buy_price': buy,
                      'current_price': current, 'profit_loss': pnl})
    return jsonify(items)

@app.route('/add', methods=['POST'])
def add_asset():
    data = request.get_json()
    name = data['name']
    qty = float(data['quantity'])
    price = float(data["buy_price"])
    portfolio[name] = {
        "quantity": qty,
        "buy_price": price,
        "current_price": price
    }
    save_portfolio()
    return jsonify({"status": "added", "asset": name})

@app.route('/update', methods=['POST'])
def update_price():
    data = request.get_json()
    name = data['name']
    price = float(data['current_price'])
    if name in portfolio:
        portfolio[name]['current_price'] = price
        save_portfolio()
        return jsonify({'status': 'updated', 'asset': name})
    return jsonify({'error': 'asset not found'}), 404

@app.route('/remove', methods=['POST'])
def remove_asset():
    data = request.get_json()
    name = data['name']
    if name in portfolio:
        removed = portfolio.pop(name)
        save_portfolio()
        return jsonify({'status': 'removed', 'asset': name, 'data': removed})
    return jsonify({'error': 'asset not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

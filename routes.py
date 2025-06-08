from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime, timedelta

chatbot_bp = Blueprint('chatbot_bp', __name__, url_prefix='/api')

DB_PATH = 'db/products.db'

def query_products(keyword=None, max_price=None, min_rating=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if keyword:
        query += " AND (name LIKE ? OR brand LIKE ? OR category LIKE ?)"
        kw = f"%{keyword}%"
        params.extend([kw, kw, kw])

    if max_price:
        query += " AND price <= ?"
        params.append(max_price)

    if min_rating:
        query += " AND rating >= ?"
        params.append(min_rating)

    c.execute(query, params)
    rows = c.fetchall()
    conn.close()

    products = []
    for row in rows:
        prod = {
            "product_id": row[0],
            "name": row[1],
            "category": row[2],
            "brand": row[3],
            "price": row[4],
            "rating": row[5],
            "stock": row[6],
            "description": row[7],
            "image_url": row[8]
        }
        products.append(prod)

    return products

def log_chat(username, message, sender):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        INSERT INTO chat_logs (username, message, sender)
        VALUES (?, ?, ?)
    ''', (username, message, sender))

    conn.commit()
    conn.close()

@chatbot_bp.route('/products', methods=['GET'])
def get_products():
    keyword = request.args.get('keyword')
    max_price = request.args.get('max_price', type=int)
    min_rating = request.args.get('min_rating', type=float)

    products = query_products(keyword, max_price, min_rating)
    return jsonify({"products": products})

@chatbot_bp.route('/chat', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_msg = data.get('message', '').lower()
    username = data.get('username', 'guest')

    log_chat(username, user_msg, 'user')

    # Basic keyword logic
    if any(x in user_msg for x in ["show", "find", "search"]):
        keyword = None
        max_price = None
        min_rating = None

        words = user_msg.split()
        for i, w in enumerate(words):
            if w.isdigit() and i > 0 and words[i-1] == "under":
                max_price = int(w)
            if w == "rating" and i + 2 < len(words):
                if words[i + 1] in ['above', 'over', 'greater']:
                    try:
                        min_rating = float(words[i + 2])
                    except:
                        pass
        for word in ['show', 'find', 'search']:
            if word in words:
                idx = words.index(word)
                if idx + 1 < len(words):
                    keyword = words[idx + 1]

        products = query_products(keyword, max_price, min_rating)

        if products:
            reply = f"I found {len(products)} products matching your search."
        else:
            reply = "Sorry, no products matched your search."

        log_chat(username, reply, 'bot')
        return jsonify({"reply": reply, "products": products})

    elif "help" in user_msg:
        reply = ("You can ask me to search products like 'show Samsung phones under 50000', "
                 "'find laptops with rating above 4' or 'search headphones'.")
        log_chat(username, reply, 'bot')
        return jsonify({"reply": reply})

    else:
        reply = "Sorry, I didn't understand that. Try asking me to 'show' or 'find' products."
        log_chat(username, reply, 'bot')
        return jsonify({"reply": reply})

@chatbot_bp.route('/history', methods=['GET'])
def get_chat_history():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username required"}), 400

    since = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        SELECT message, sender, timestamp FROM chat_logs 
        WHERE username = ? AND timestamp >= ?
        ORDER BY timestamp ASC
    ''', (username, since))

    logs = [{"message": msg, "sender": sender, "timestamp": ts} for msg, sender, ts in c.fetchall()]
    conn.close()

    return jsonify({"username": username, "history": logs})

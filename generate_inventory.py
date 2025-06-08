import sqlite3
import random
import os

DB_DIR = 'db'
DB_PATH = os.path.join(DB_DIR, 'products.db')

os.makedirs(DB_DIR, exist_ok=True)

brands = ['Samsung', 'Apple', 'Sony', 'Dell', 'HP', 'Lenovo', 'Asus', 'Bose', 'JBL', 'Canon']
categories = ['Smartphones', 'Laptops', 'Headphones', 'Cameras', 'Speakers', 'Monitors']

descriptions = {
    'Smartphones': 'Latest generation smartphone with advanced features and sleek design.',
    'Laptops': 'High performance laptop suitable for gaming and professional work.',
    'Headphones': 'Noise-cancelling headphones delivering crystal clear sound quality.',
    'Cameras': 'High resolution camera perfect for photography enthusiasts.',
    'Speakers': 'Portable speakers with deep bass and clear sound.',
    'Monitors': 'Full HD monitor with vibrant colors and wide viewing angles.'
}

def create_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            brand TEXT,
            price INTEGER,
            rating REAL,
            stock INTEGER,
            description TEXT,
            image_url TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_mock_data(num=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for _ in range(num):
        category = random.choice(categories)
        brand = random.choice(brands)
        name = f"{brand} {category[:-1]} Model {random.randint(100,999)}"
        price = random.randint(5000, 150000)
        rating = round(random.uniform(3.0, 5.0), 1)
        stock = random.randint(0, 50)
        description = descriptions[category]
        image_url = f"https://dummyimage.com/200x200/000/fff&text={brand}+{category[:-1]}"

        c.execute('''
            INSERT INTO products (name, category, brand, price, rating, stock, description, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, brand, price, rating, stock, description, image_url))

    conn.commit()
    conn.close()

def create_user_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def create_chat_log_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT,
            sender TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    create_user_table()
    create_chat_log_table()
    insert_mock_data()
    print(f"✅ All tables created and inserted 100 mock products into {DB_PATH}")

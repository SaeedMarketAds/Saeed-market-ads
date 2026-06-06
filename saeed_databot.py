# saeed_databot.py - نظام سعيد داتابوت المتكامل مع إدارة المنتجات

import streamlit as st
import os
import json
import hashlib
from datetime import datetime

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# ==================== تحميل الإعدادات ====================
def load_config():
    config_path = "saeed_databot_config.json"
    default_config = {
        "bot_name": "سعيد داتابوت",
        "owner_name": "سعيد المسوري",
        "model_name": "gemini-1.5-flash",
        "max_history": 15,
        "temperature": 0.7,
        "top_p": 0.9,
        "voice_enabled": True,
        "markets": ["aliexpress", "noon", "shein", "yemen"],
        "admin_password": "saeed2024",
        "admin_username": "admin"
    }
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            default_config.update(config)
    else:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
    
    return default_config

CONFIG = load_config()

# ==================== قاعدة بيانات المنتجات ====================
PRODUCTS_FILE = "products_db.json"

def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    default_products = {
        "aliexpress": [
            {"id": 1, "name": "هاتف ذكي 5G", "price": "$199", "icon": "📱", "link": "https://www.aliexpress.com", "stock": 50},
            {"id": 2, "name": "ساعة رياضية", "price": "$45", "icon": "⌚", "link": "https://www.aliexpress.com", "stock": 30},
        ],
        "noon": [
            {"id": 3, "name": "لابتوب ألعاب", "price": "899 درهم", "icon": "💻", "link": "https://www.noon.com", "stock": 10},
            {"id": 4, "name": "شاحن سريع", "price": "49 درهم", "icon": "⚡", "link": "https://www.noon.com", "stock": 200},
        ],
        "shein": [
            {"id": 5, "name": "فستان سهرة", "price": "$32", "icon": "👗", "link": "https://www.shein.com", "stock": 60},
            {"id": 6, "name": "حقيبة يد", "price": "$18", "icon": "👜", "link": "https://www.shein.com", "stock": 80},
        ],
        "yemen": [
            {"id": 7, "name": "عسل سدر يمني", "price": "15,000 ريال", "icon": "🍯", "link": "#", "stock": 25},
            {"id": 8, "name": "قهوة يمنية", "price": "10,000 ريال", "icon": "☕", "link": "#", "stock": 30},
        ]
    }
    
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_products, f, ensure_ascii=False, indent=2)
    return default_products

def save_products(products):
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def add_product(market, name, price, icon, link, stock):
    products = load_products()
    all_ids = [p["id"] for m in products.values() for p in m]
    new_id = max(all_ids) + 1 if all_ids else 1
    
    new_product = {
        "id": new_id,
        "name": name,
        "price": price,
        "icon": icon,
        "link": link,
        "stock": stock
    }
    
    if market not in products:
        products[market] = []
    products[market].append(new_product)
    save_products(products)
    return True

def update_product(market, product_id, updates):
    products = load_products()
    for i, product in enumerate(products.get(market, [])):
        if product["id"] == product_id:
            products[market][i].update(updates)
            save_products(products)
            return True
    return False

def delete_product(market, product_id):
    products = load_products()
    products[market] = [p for p in products.get(market, []) if p["id"] != product_id]
    save_products(products)
    return True

def get_market_products(market_name):
    products = load_products()
    return products.get(market_name, [])

# ==================== دوال البوت الذكي ====================
def get_bot_response(user_message, chat_history, is_avatar_mode=False):
    msg = user_message.lower()
    
    if any(word in msg for word in ['هاتف', 'جوال', 'موبايل']):
        return "📱 **سعيد داتابوت:** كم ميزانيتك للهاتف؟ وما هي أهم ميزة تبحث فيها؟"
    
    elif any(word in msg for word in ['كاميرا', 'تصوير']):
        return "📷 أنصحك بهواتف شاومي أو سامسونج. كاميراتهم ممتازة مقابل السعر. كم ميزانيتك؟"
    
    elif any(word in msg for word in ['aliexpress', 'علي']):
        return "🛒 AliExpress: أسعار ممتازة لكن الشحن يطول. هل تريد مساعدة في البحث؟"
    
    elif any(word in msg for word in ['noon', 'نون']):
        return "🇦🇪 Noon: توصيل سريع وضمان أفضل. ما المنتج الذي تبحث عنه؟"
    
    else:
        return f"🎯 **{CONFIG['bot_name']}:** كيف يمكنني مساعدتك اليوم؟ يمكنني مساعدتك في شراء هاتف، أو إيجاد عروض في AliExpress أو Noon."

def speak_response(text):
    try:
        clean_text = text.replace("**", "").replace("*", "").replace("\n", " ").replace('"', '\\"')
        js_code = f"""
        <script>
            var utterance = new SpeechSynthesisUtterance("{clean_text}");
            utterance.lang = "ar-SA";
            utterance.rate = 0.9;
            window.speechSynthesis.speak(utterance);
        </script>
        """
        import streamlit as st
        st.components.v1.html(js_code, height=0)
    except:
        pass

def get_market_advice():
    return "نصائح التسوق: AliExpress للأسعار المنخفضة، Noon للتوصيل السريع"

# ==================== تصدير الدوال ====================
__all__ = [
    'load_products',
    'save_products', 
    'add_product',
    'update_product',
    'delete_product',
    'get_market_products',
    'get_bot_response',
    'speak_response',
    'get_market_advice',
    'CONFIG'
]

here# saeed_databot.py - النسخة المطورة مع نظام إدارة المنتجات والأدمن
import streamlit as st
import os
import base64
import json
import hashlib
from datetime import datetime
import google.generativeai as genai

# ==================== تحميل الإعدادات ====================
def load_config():
    """تحميل إعدادات البوت من ملف الإعدادات"""
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
        # حفظ الإعدادات الافتراضية
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
    
    return default_config

CONFIG = load_config()

# ==================== نظام إدارة المنتجات ====================
PRODUCTS_FILE = "products_db.json"

def load_products():
    """تحميل المنتجات من قاعدة البيانات"""
    default_products = {
        "aliexpress": [
            {"id": 1, "name": "هاتف ذكي 5G", "price": "$199", "icon": "📱", "link": "https://www.aliexpress.com", "stock": 50},
            {"id": 2, "name": "ساعة رياضية", "price": "$45", "icon": "⌚", "link": "https://www.aliexpress.com", "stock": 30},
            {"id": 3, "name": "سماعات لاسلكية", "price": "$25", "icon": "🎧", "link": "https://www.aliexpress.com", "stock": 100},
            {"id": 4, "name": "باور بانك 20000mAh", "price": "$30", "icon": "🔋", "link": "https://www.aliexpress.com", "stock": 25},
            {"id": 5, "name": "كاميرا مراقبة", "price": "$50", "icon": "📷", "link": "https://www.aliexpress.com", "stock": 15}
        ],
        "noon": [
            {"id": 6, "name": "لابتوب ألعاب", "price": "899 درهم", "icon": "💻", "link": "https://www.noon.com", "stock": 10},
            {"id": 7, "name": "شاحن سريع", "price": "49 درهم", "icon": "⚡", "link": "https://www.noon.com", "stock": 200},
            {"id": 8, "name": "سماعة رأس", "price": "89 درهم", "icon": "🎮", "link": "https://www.noon.com", "stock": 45},
            {"id": 9, "name": "تابلت", "price": "399 درهم", "icon": "📟", "link": "https://www.noon.com", "stock": 20},
            {"id": 10, "name": "ساعة ذكية", "price": "199 درهم", "icon": "⌚", "link": "https://www.noon.com", "stock": 35}
        ],
        "shein": [
            {"id": 11, "name": "فستان سهرة", "price": "$32", "icon": "👗", "link": "https://www.shein.com", "stock": 60},
            {"id": 12, "name": "حقيبة يد", "price": "$18", "icon": "👜", "link": "https://www.shein.com", "stock": 80},
            {"id": 13, "name": "حذاء رياضي", "price": "$25", "icon": "👟", "link": "https://www.shein.com", "stock": 40},
            {"id": 14, "name": "نظارة شمسية", "price": "$15", "icon": "🕶️", "link": "https://www.shein.com", "stock": 120},
            {"id": 15, "name": "ساعة أنيقة", "price": "$22", "icon": "⌚", "link": "https://www.shein.com", "stock": 55}
        ],
        "yemen": [
            {"id": 16, "name": "عسل سدر يمني", "price": "15,000 ريال", "icon": "🍯", "link": "#", "stock": 25},
            {"id": 17, "name": "مصنوعات فضية", "price": "25,000 ريال", "icon": "💍", "link": "#", "stock": 12},
            {"id": 18, "name": "بخور يمني", "price": "8,000 ريال", "icon": "🪔", "link": "#", "stock": 45},
            {"id": 19, "name": "ملابس تراثية", "price": "12,000 ريال", "icon": "👘", "link": "#", "stock": 18},
            {"id": 20, "name": "قهوة يمنية", "price": "10,000 ريال", "icon": "☕", "link": "#", "stock": 30}
        ]
    }
    
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_products, f, ensure_ascii=False, indent=2)
        return default_products

def save_products(products):
    """حفظ المنتجات إلى قاعدة البيانات"""
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def add_product(market, name, price, icon, link, stock):
    """إضافة منتج جديد"""
    products = load_products()
    new_id = max([p["id"] for market_products in products.values() for p in market_products]) + 1 if any(products.values()) else 1
    
    new_product = {
        "id": new_id,
        "name": name,
        "price": price,
        "icon": icon,
        "link": link,
        "stock": stock
    }
    
    if market in products:
        products[market].append(new_product)
    else:
        products[market] = [new_product]
    
    save_products(products)
    return True

def update_product(market, product_id, updates):
    """تحديث بيانات منتج"""
    products = load_products()
    for i, product in enumerate(products.get(market, [])):
        if product["id"] == product_id:
            products[market][i].update(updates)
            save_products(products)
            return True
    return False

def delete_product(market, product_id):
    """حذف منتج"""
    products = load_products()
    products[market] = [p for p in products.get(market, []) if p["id"] != product_id]
    save_products(products)
    return True

# ==================== النص التوجيهي المتقدم ====================
SAEED_DATABOT_SYSTEM_PROMPT = """
أنت **سعيد داتابوت (Saeed DataBot)**، مساعد ذكي متخصص في التسويق الذكي واختيار الهواتف المناسبة للمستهلكين. تم تصميمك وبرمجتك بواسطة **سعيد المسوري**، المطور الخبير.

## شخصيتك:
ودود، محترف، ذكي، تقدم نصائح مبنية على خبرة واقعية. تتحدث كخبير تقني مع صديق.

## مهامك الأساسية:
1. **اختيار الهواتف:** اسأل عن الميزانية، الاستخدام، المواصفات المفضلة
2. **نصائح الأسواق:** اعرف الفروقات بين AliExpress، Noon، Shein، والسوق اليمني
3. **استخدام الذاكرة:** تذكر آخر 15 رسالة ولا تكرر الأسئلة

## أسلوب الرد:
- مختصر ومقنع (2-4 جمل)
- استخدم الرموز التعبيرية 📱💰🎯
- انهي بسؤال لمتابعة المحادثة
"""

# ==================== إعداد Gemini API ====================
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        GEMINI_AVAILABLE = True
    else:
        GEMINI_AVAILABLE = False
except Exception as e:
    GEMINI_AVAILABLE = False

def get_gemini_model():
    """الحصول على نموذج Gemini"""
    if not GEMINI_AVAILABLE:
        return None
    return genai.GenerativeModel(
        model_name=CONFIG["model_name"],
        system_instruction=SAEED_DATABOT_SYSTEM_PROMPT,
        generation_config={"temperature": CONFIG["temperature"], "top_p": CONFIG["top_p"]}
    )

def get_bot_response(user_message, chat_history, is_avatar_mode=False):
    """توليد رد ذكي"""
    # ردود سريعة للهواتف
    msg = user_message.lower()
    
    if any(word in msg for word in ['هاتف', 'جوال', 'موبايل', 'شراء هاتف']):
        return "📱 **سعيد داتابوت:** ممتاز! كم ميزانيتك للهاتف؟ وما هي أهم ميزة تبحث فيها (كاميرا، بطارية، شاشة)؟"
    
    elif any(word in msg for word in ['كاميرا', 'تصوير']):
        return "📷 أنصحك بهواتف شاومي (سلسلة Redmi Note) أو سامسونج (سلسلة A). كاميراتهم ممتازة مقابل السعر. كم ميزانيتك؟"
    
    elif any(word in msg for word in ['بطارية', 'شحن']):
        return "🔋 هواتف شاومي وسامسونج الفئة المتوسطة تقدم بطاريات 5000mAh. أنصحك بـ Xiaomi Redmi Note 12 أو Samsung A14."
    
    elif not GEMINI_AVAILABLE:
        return f"🎯 **{CONFIG['bot_name']}:** في خدمتك! أخبرني ما الذي تبحث عن شرائه وسأساعدك في اختيار الأفضل."
    
    else:
        try:
            model = get_gemini_model()
            if model:
                chat = model.start_chat(history=[])
                recent = chat_history[-10:] if len(chat_history) > 10 else chat_history
                for msg in recent:
                    if msg.get("role") == "user":
                        chat.send_message(msg.get("content", ""))
                response = chat.send_message(user_message)
                return response.text
        except Exception as e:
            return f"🎯 **{CONFIG['bot_name']}:** عذراً حدث خطأ. كيف يمكنني مساعدتك اليوم؟"
    
    return "🎯 كيف يمكنني مساعدتك اليوم؟"

# ==================== دوال الصوت ====================
def text_to_speech_js(text):
    """تحويل النص إلى كلام"""
    clean_text = text.replace("**", "").replace("*", "").replace("\n", " ").replace('"', '\\"')
    return f"""
    <script>
        var utterance = new SpeechSynthesisUtterance("{clean_text}");
        utterance.lang = "ar-SA";
        utterance.rate = 0.9;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
    </script>
    """

def speak_response(text):
    """تشغيل الرد صوتياً"""
    if CONFIG["voice_enabled"]:
        st.components.v1.html(text_to_speech_js(text), height=0)

# ==================== دوال الأسواق ====================
def get_market_products(market_name):
    """جلب منتجات حسب السوق"""
    products = load_products()
    return products.get(market_name, [])

def get_market_advice():
    """تقديم نصائح الأسواق"""
    return """
    📊 **نصائح سعيد داتابوت:**
    - 🛒 AliExpress: أسعار تنافسية، شحن 15-30 يوم
    - 🇦🇪 Noon: توصيل سريع، ضمان أفضل
    - 👗 Shein: الأفضل للأزياء
    - 🇾🇪 السوق اليمني: دعم المنتجات المحلية
    """

# تصدير الدوال
__all__ = [
    'get_bot_response',
    'speak_response',
    'get_market_products',
    'get_market_advice',
    'load_products',
    'add_product',
    'update_product',
    'delete_product',
    'CONFIG'
]

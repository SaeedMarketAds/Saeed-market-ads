import streamlit as st
import google.generativeai as genai
import requests
import io
import os
import base64
import re
import streamlit.components.v1 as components

# ============================================================
# 1. إعدادات الصفحة
# ============================================================
st.set_page_config(
    page_title="سوق سعيد | متاجر SHEIN - نون - علي اكسبرس",
    page_icon="🛍️",
    layout="wide"
)

# ============================================================
# 2. الخلفية والتصميم (CSS)
# ============================================================
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0.2);
}
.stMarkdown {
    color: #fff;
}
.stButton > button {
    background: linear-gradient(90deg, #ff6b6b, #feca57);
    color: white;
    border: none;
    border-radius: 30px;
    padding: 12px 28px;
    font-weight: bold;
    font-size: 16px;
    transition: all 0.3s ease;
    width: 100%;
}
.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #feca57, #ff6b6b);
    box-shadow: 0 5px 20px rgba(0,0,0,0.3);
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.1);
    color: white;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.2);
    padding: 12px 20px;
}
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.1);
    color: white;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.2);
}
.product-card {
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(250,250,255,0.95));
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
}
.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.25);
}
.product-code {
    position: absolute;
    top: 10px;
    right: 15px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: bold;
    direction: ltr;
}
.product-name {
    font-size: 16px;
    font-weight: bold;
    color: #1e293b;
    margin-bottom: 12px;
    min-height: 50px;
    padding-right: 60px;
}
.product-price {
    color: #ff4757;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;
}
.old-price {
    color: #999;
    font-size: 14px;
    text-decoration: line-through;
    margin-right: 10px;
}
.product-sales {
    color: #2ecc71;
    font-weight: bold;
    font-size: 13px;
    margin-bottom: 10px;
}
.product-discount {
    background: #ff6b6b;
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    display: inline-block;
}
.product-btn {
    background: linear-gradient(90deg, #667eea, #764ba2);
    border-radius: 40px;
    padding: 12px;
    text-align: center;
    cursor: pointer;
    font-weight: bold;
    color: white;
    transition: all 0.3s ease;
    margin-top: 15px;
    border: none;
}
.product-btn:hover {
    background: linear-gradient(90deg, #764ba2, #667eea);
    transform: scale(1.02);
}
.store-section {
    background: rgba(255,255,255,0.05);
    border-radius: 30px;
    padding: 25px;
    margin-bottom: 40px;
    backdrop-filter: blur(5px);
}
.store-header-shein {
    background: linear-gradient(135deg, #ff6b6b, #feca57);
    text-align: center;
    padding: 20px;
    border-radius: 25px;
    margin-bottom: 30px;
}
.store-header-noon {
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    text-align: center;
    padding: 20px;
    border-radius: 25px;
    margin-bottom: 30px;
}
.store-header-aliexpress {
    background: linear-gradient(135deg, #ff4757, #ff6b81);
    text-align: center;
    padding: 20px;
    border-radius: 25px;
    margin-bottom: 30px;
}
hr {
    border-color: rgba(255,255,255,0.1);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ============================================================
# 3. دالة تشغيل الصوت (تعمل 100% في السحابة)
# ============================================================
def play_voice(filename="new_voice.mp3"):
    """
    تشغيل الصوت: يحاول قراءة الملف المحلي، وإذا لم يجد يستخدم رابط GitHub Raw
    """
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        paths_to_try = [
            os.path.join(base_path, filename),
            os.path.join(os.getcwd(), filename),
            "./" + filename,
            "/mount/src/Saeed-market-ads/" + filename,
            "/app/Saeed-market-ads/" + filename,
        ]
        
        for path in paths_to_try:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                audio_html = f'''
                <audio autoplay="true" style="display:none;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                '''
                st.markdown(audio_html, unsafe_allow_html=True)
                return True
        
        audio_url = "https://raw.githubusercontent.com/SaeedMarketAds/Saeed-market-ads/main/new_voice.mp3"
        audio_html = f'''
        <audio autoplay="true" style="display:none;">
            <source src="{audio_url}" type="audio/mp3">
        </audio>
        '''
        st.markdown(audio_html, unsafe_allow_html=True)
        return True
        
    except Exception as e:
        st.error(f"Error playing voice: {str(e)}")
        return False

# ============================================================
# 4. قراءة المفاتيح والتعليمات
# ============================================================
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API"]
except:
    GEMINI_API_KEY = None

try:
    with open('Instructions.txt', 'r', encoding='utf-8') as f:
        instructions = f.read()
except FileNotFoundError:
    instructions = "You are a smart shopping assistant named Saeed DaTaBoT."
    st.warning("Instructions.txt not found, using defaults.")

# ============================================================
# 5. إعداد موديل Gemini
# ============================================================
try:
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-3.5-flash",
            system_instruction=instructions
        )
    else:
        model = None
        st.error("API key not found. Please add it to secrets.toml")
except Exception as e:
    model = None
    st.error(f"Error setting up model: {str(e)}")

# ============================================================
# 6. الوظائف المساعدة
# ============================================================
@st.cache_data(ttl=3600)
def is_product_available(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, timeout=8, headers=headers)
        unavailable_indicators = ["sold out", "out of stock", "غير متوفر", "نفدت الكمية", "unavailable"]
        response_lower = response.text.lower()
        for indicator in unavailable_indicators:
            if indicator in response_lower:
                return False
        return response.status_code == 200
    except:
        return True

def quick_response(question):
    q = question.lower()
    if "كود الخصم" in q or "خصم" in q or "كود" in q:
        return "🎁 **SHEIN Discount Code** 🎁\n\n🏷️ **Code: WL7KA**\n\n🔥 Up to 60% off on first order\n✅ Valid on all SHEIN products"
    elif "من أنت" in q:
        return "🤖 I am **Saeed DaTaBoT**, your smart shopping assistant.\n\nSpecialized in:\n• Link analysis\n• Product availability check\n• Shopping help from SHEIN - Noon - AliExpress"
    elif "السلام" in q or "مرحبا" in q:
        return "🌹 Peace be upon you 🌹\n\nWelcome to **Saeed Market**! I am **Saeed DaTaBoT** at your service."
    return None

def render_custom_banner():
    html_code = """
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        body { font-family: 'Cairo', sans-serif; background: transparent; }
        .glass { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
    <div class="glass w-full max-w-4xl rounded-3xl p-8 shadow-2xl mx-auto">
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-white mb-2">Saeed Market 🛍️</h1>
            <p class="text-blue-300 text-lg">AI that changes global shopping rules</p>
        </header>
        <div class="grid md:grid-cols-2 gap-8 items-center">
            <div class="space-y-4">
                <div class="bg-blue-600 p-6 rounded-2xl text-white">
                    <h2 class="text-xl font-bold mb-2">Unique Shopping Experience</h2>
                    <p class="opacity-90">Real-time price analysis, exclusive discount codes, and smart integration with major stores.</p>
                </div>
                <div class="bg-pink-500 p-6 rounded-2xl text-white">
                    <h2 class="text-xl font-bold mb-2">Global Reach in an Hour</h2>
                    <p class="opacity-90">With Saeed DataBot, shop smart and fast, trusted by thousands.</p>
                </div>
            </div>
            <div class="glass p-6 rounded-3xl text-center">
                <div class="text-5xl mb-4">🚀</div>
                <h3 class="text-2xl font-bold text-white mb-2">Code: WL7KA</h3>
                <p class="text-white mb-4">Up to 60% off on first order!</p>
            </div>
        </div>
    </div>
    """
    components.html(html_code, height=550)

# ============================================================
# 7. واجهة المستخدم الرئيسية
# ============================================================
render_custom_banner()

try:
    if os.path.exists("Saeed_DataBot_Avatar.jpg"):
        st.image("Saeed_DataBot_Avatar.jpg", width=200)
    else:
        st.warning("Saeed_DataBot_Avatar.jpg not found")
except Exception as e:
    st.warning(f"Cannot display image: {str(e)}")

st.markdown("""
<div style='text-align: center; padding: 50px 20px; background: linear-gradient(135deg, rgba(26,26,46,0.9), rgba(22,33,62,0.9)); border-radius: 50px; margin-bottom: 30px;'>
    <h1 style='color: #fff; font-size: 55px; margin-bottom: 10px;'>Saeed Market 🛍️</h1>
    <p style='color: #feca57; font-size: 24px;'>SHEIN | Noon | AliExpress</p>
    <p style='color: #aaa; font-size: 16px;'>Shop with the best prices and exclusive discount codes</p>
    <p style='color: #ff6b6b; font-size: 18px; margin-top: 10px;'>🤖 Your smart assistant Saeed DaTaBoT</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background: linear-gradient(135deg, #ff0844, #ffb199); padding: 45px 25px; border-radius: 55px; text-align: center; margin-bottom: 40px;'>
    <h2 style='color: #fff; margin-bottom: 15px; font-size: 32px;'>Special offer for new users 🎁</h2>
    <div style='background: white; display: inline-block; padding: 20px 60px; border-radius: 80px; margin: 15px 0;'>
        <h1 style='color: #ff0844; margin: 0; font-size: 55px; letter-spacing: 5px;'>WL7KA 🏷️</h1>
    </div>
    <p style='color: #fff; font-size: 26px; margin: 10px 0 0 0; font-weight: bold;'>🔥 Up to 60% off on first order 🔥</p>
    <p style='color: #fff; font-size: 18px; margin-top: 10px;'>✨ Use the code at checkout and save more ✨</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🎙️ Listen to welcome message from Saeed DaTaBoT")
play_voice()

# ============================================================
# 8. تحليل الروابط
# ============================================================
st.markdown("<h2 style='color: #feca57; text-align: center; font-size: 32px; margin-bottom: 20px;'>🔗 Link Analysis with Saeed DaTaBoT</h2>", unsafe_allow_html=True)

url_input = st.text_input("📎 Paste product link here (SHEIN, Noon, AliExpress):", placeholder="https://...")

if url_input:
    with st.spinner("🤖 Saeed DaTaBoT is analyzing the link..."):
        is_available = is_product_available(url_input)
        if model:
            try:
                response = model.generate_content(f"Analyze this link briefly: {url_input}")
                status = "✅ Available" if is_available else "❌ Currently unavailable"
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #feca57; margin-bottom: 20px;'>
                    <h4 style='color: #feca57;'>🤖 Saeed DaTaBoT responds:</h4>
                    <p style='color: #e2e8f0;'>{response.text}</p>
                    <hr>
                    <p style='color: #2ecc71;'><strong>📦 Product status:</strong> {status}</p>
                </div>
                """, unsafe_allow_html=True)
                play_voice()
            except Exception as e:
                st.info(f"Cannot analyze link: {str(e)}")
        else:
            st.info("Analysis service is currently unavailable")

st.markdown("---")

# ============================================================
# 9. منتجات SHEIN
# ============================================================
st.markdown("""
<div class='store-section'>
    <div class='store-header-shein'>
        <h2 style='color: white; font-size: 36px; margin: 0;'>SHEIN Store 🛍️</h2>
        <p style='color: white; font-size: 18px; margin: 5px 0 0 0;'>51 products at amazing prices</p>
    </div>
</div>
""", unsafe_allow_html=True)

SHEIN_PRODUCTS = [
    {"code": "SH001", "name": "Quilted Coat with Hood for Girls", "price": 19.39, "discount": 43, "link": "https://onelink.shein.com/38/5shrzfcizjmg", "sales": "150+"},
    {"code": "SH002", "name": "Elegant Hong Kong Design Shirt", "price": 14.18, "discount": 37, "link": "https://onelink.shein.com/38/5shune7n90yf", "sales": "200+"},
    {"code": "SH003", "name": "Printed Party Glasses 6pcs", "price": 2.70, "discount": 0, "link": "https://onelink.shein.com/38/5shujg5f2ywk", "sales": "300+"},
    {"code": "SH004", "name": "Waterproof Travel Organizer Bag", "price": 3.90, "discount": 17, "link": "https://onelink.shein.com/38/5shuimjyfjt7", "sales": "100+"},
    {"code": "SH005", "name": "Men's Casual Plain Coat", "price": 25.67, "discount": 24, "link": "https://onelink.shein.com/38/5shui8qqn60h", "sales": "200+"},
    {"code": "SH006", "name": "Floral Design Earrings", "price": 1.44, "discount": 4, "link": "https://onelink.shein.com/38/5shtox57cemc", "sales": "300+"},
    {"code": "SH007", "name": "Colorful Hair Ties 5pcs", "price": 1.50, "discount": 38, "link": "https://onelink.shein.com/38/5shtobfv3sxn", "sales": "800+"},
    {"code": "SH008", "name": "Women's Casual Sports Shoes", "price": 5.00, "discount": 82, "link": "https://onelink.shein.com/38/5shtl502kmcf", "sales": "200+"},
    {"code": "SH009", "name": "Pink Flower Ring Set", "price": 2.16, "discount": 6, "link": "https://onelink.shein.com/38/5shtkl9rhh8f", "sales": "500+"},
    {"code": "SH010", "name": "Rice Bucket with Measuring Cup", "price": 8.84, "discount": 70, "link": "https://onelink.shein.com/38/5shtjtnbwphj", "sales": "200+"},
]

cols = st.columns(4)
for i, product in enumerate(SHEIN_PRODUCTS):
    with cols[i % 4]:
        final_price = product['price'] * (1 - product['discount']/100) if product['discount'] > 0 else product['price']
        old_price = product['price'] if product['discount'] > 0 else None
        st.markdown(f"""
        <div class='product-card'>
            <div class='product-code'>📦 {product['code']}</div>
            <div class='product-name'>{product['name']}</div>
            <div class='product-price'>
                ${final_price:.2f}
                {f"<span class='old-price'>${old_price:.2f}</span>" if old_price else ""}
            </div>
            <div class='product-sales'>📊 Sold: {product['sales']}</div>
            <div class='product-discount'>{'🔥 ' + str(product['discount']) + '% off' if product['discount'] > 0 else ''}</div>
            <a href='{product['link']}' target='_blank' style='text-decoration: none;'>
                <div class='product-btn'>🛒 Shop Now</div>
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# 10. بوت الدردشة
# ============================================================
st.markdown("<h2 style='color: #feca57; text-align: center; font-size: 32px; margin-bottom: 20px;'>💬 Chat with Saeed DaTaBoT</h2>", unsafe_allow_html=True)

chat_question = st.text_area("📝 Write your question here:", placeholder="What would you like to ask Saeed DaTaBoT?", height=100)

if st.button("💬 Send", use_container_width=True):
    if chat_question:
        quick_ans = quick_response(chat_question)
        if quick_ans:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71; margin-bottom: 20px;'>
                <h4 style='color: #feca57;'>🤖 Saeed DaTaBoT responds:</h4>
                <p style='color: #e2e8f0;'>{quick_ans}</p>
            </div>
            """, unsafe_allow_html=True)
            play_voice()
        elif model:
            try:
                response = model.generate_content(f"Respond briefly and confidently as Saeed DaTaBoT: {chat_question}")
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'>
                    <h4 style='color: #feca57;'>🤖 Saeed DaTaBoT responds:</h4>
                    <p style='color: #e2e8f0;'>{response.text}</p>
                </div>
                """, unsafe_allow_html=True)
                play_voice()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please write your question first")

st.markdown("---")

# ============================================================
# 11. السايدبار
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 30px; margin-bottom: 20px;'>
        <h2 style='color: #feca57; margin-bottom: 10px;'>🤖 Saeed DaTaBoT</h2>
        <p style='color: #aaa;'>Your smart shopping assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Saeed DaTaBoT Services:")
    st.markdown("""
    - ✅ Link analysis
    - ✅ Product availability check
    - ✅ SHEIN exclusive offers
    - ✅ Noon featured offers
    - ✅ AliExpress coming soon
    - ✅ Smart chat
    """)

    st.markdown("---")
    st.markdown("### 📞 Contact:")
    st.markdown("- [@SaeedMarketAds](https://t.me/SaeedMarketAds)")
    st.markdown("- [@SaeedDataBot](https://t.me/SaeedDataBot)")

    st.markdown("---")
    st.markdown("### 📊 Statistics:")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🛍️ SHEIN Products", "51")
    with col2:
        st.metric("⭐ Noon Products", "12+")

    st.markdown("---")
    st.caption("© 2026 Saeed Market - All Rights Reserved")
    st.caption("Developed by: Saeed Al-Masouri")

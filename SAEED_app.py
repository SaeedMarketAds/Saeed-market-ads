# SAEED_app.py - الملف الرئيسي المعدل
import streamlit as st
import os
import base64
from saeed_databot import (
    get_bot_response, speak_response, get_market_products, 
    get_market_advice, CONFIG
)

# ==================== إعداد الصفحة ====================
st.set_page_config(
    page_title="SaeedMarketAds - سوق سعيد",
    page_icon="🛍️",
    layout="wide"
)

# تنسيق CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    * { font-family: 'Tajawal', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }
    .main-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .product-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }
    .bot-message { background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; text-align: right; }
    .user-message { background: linear-gradient(135deg, #11998e, #38ef7d); color: white; text-align: left; }
    </style>
""", unsafe_allow_html=True)

# ==================== رأس الصفحة ====================
if os.path.exists("ROBOT.jpg"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("ROBOT.jpg", width=150)

st.markdown(f'<div class="main-header"><h1>🤖 {CONFIG["bot_name"]}</h1><p>مساعدك الذكي للتسوق العالمي</p></div>', unsafe_allow_html=True)

# ==================== الأسواق ====================
st.markdown("### 🏪 الأسواق العالمية")
col1, col2, col3, col4 = st.columns(4)

markets = {
    "aliexpress": ("🛒 AliExpress", "عروض حصرية"),
    "noon": ("🇦🇪 Noon", "توصيل سريع"),
    "shein": ("👗 Shein", "أزياء وموضة"),
    "yemen": ("🇾🇪 السوق اليمني", "دعم المحلي")
}

for i, (market, (name, desc)) in enumerate(markets.items()):
    with [col1, col2, col3, col4][i]:
        if st.button(f"**{name}**\n{desc}", use_container_width=True):
            st.session_state.selected_market = market

# ==================== عرض المنتجات ====================
if "selected_market" in st.session_state:
    st.markdown("---")
    st.markdown(f"### 🛍️ منتجات {st.session_state.selected_market}")
    
    products = get_market_products(st.session_state.selected_market)
    
    for i in range(0, len(products), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(products):
                p = products[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="product-card">
                        <div style="font-size: 3rem;">{p['icon']}</div>
                        <h4>{p['name']}</h4>
                        <p style="color: #f5576c;">{p['price']}</p>
                        <small>📦 المخزون: {p.get('stock', 'متوفر')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🛒 شراء", key=f"buy_{p['id']}"):
                        if p.get('link') and p['link'] != "#":
                            st.markdown(f'<meta http-equiv="refresh" content="0; url={p["link"]}">', unsafe_allow_html=True)

# ==================== المحادثة ====================
st.markdown("---")
st.markdown("## 💬 دردش مع المساعد الذكي")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": f"🎙️ أهلاً بك! أنا {CONFIG['bot_name']}. كيف أخدمك اليوم؟"}]

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-message user-message">🗣️ {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

user_input = st.text_input("", placeholder="اكتب سؤالك هنا...", key="user_input", label_visibility="collapsed")
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("📤 إرسال", use_container_width=True) and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        reply = get_bot_response(user_input, st.session_state.chat_history[:-1], is_avatar_mode=False)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        speak_response(reply)
        st.rerun()

# ==================== رابط لوحة الأدمن ====================
st.markdown("---")
st.markdown(f'<p style="text-align: center;">🔐 <a href="/admin_panel" target="_blank">لوحة تحكم الأدمن</a> | © 2025 {CONFIG["owner_name"]}</p>', unsafe_allow_html=True)

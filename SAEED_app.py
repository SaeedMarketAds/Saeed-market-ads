import streamlit as st
import os
import base64
from pathlib import Path
from saeed_databot import SaeedDataBot
from saeed_market import SaeedMarket

# إعداد الصفحة
st.set_page_config(
    page_title="SaeedMarktAds - سوق سعيد",
    page_icon="🛍️",
    layout="wide"
)

# تهيئة البوت
bot = SaeedDataBot()
market = SaeedMarket()

# تنسيق CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    * { font-family: 'Tajawal', 'Cairo', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }
    .main-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 { color: white; font-size: 2rem; margin: 0; }
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }
    .bot-message {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        text-align: right;
    }
    .user-message {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# رأس الصفحة
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("saeed.jpg"):
        st.image("saeed.jpg", width=120)
    st.markdown('<div class="main-header"><h1>🛍️ سوق سعيد | SaeedMarktAds</h1><p>🤖 SaeedDataBot - مساعدك الذكي</p></div>', unsafe_allow_html=True)

# تشغيل صوت المؤسس عند فتح الصفحة
if "voice_played" not in st.session_state:
    voice_html = bot.get_voice_html()
    if voice_html:
        st.components.v1.html(voice_html, height=0)
    st.session_state.voice_played = True

# تهيئة سجل المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history.append({"role": "bot", "content": bot.get_welcome_message()})

# عرض الأسواق
st.markdown("### 📊 الأسواق العالمية")
col1, col2, col3, col4 = st.columns(4)
markets_list = [
    ("🛒 AliExpress", "aliexpress"),
    ("🇦🇪 Noon", "noon"),
    ("👗 Shein", "shein"),
    ("🇾🇪 السوق اليمني", "yemen")
]

for i, (name, key) in enumerate(markets_list):
    with [col1, col2, col3, col4][i]:
        if st.button(name, use_container_width=True):
            st.session_state.selected_market = key
            reply = market.get_products(key) if hasattr(market, 'get_products') else f"مرحباً بك في {name}"
            st.session_state.chat_history.append({"role": "bot", "content": reply})

# عرض المنتجات
if "selected_market" in st.session_state:
    st.markdown("---")
    st.markdown(f"### 🛍️ المنتجات")
    
    products_data = {
        "aliexpress": [("📱 هاتف ذكي", "$199"), ("⌚ ساعة رياضية", "$45"), ("🎧 سماعات", "$25")],
        "noon": [("💻 لابتوب", "899 درهم"), ("⚡ شاحن سريع", "49 درهم"), ("🎮 سماعة رأس", "89 درهم")],
        "shein": [("👗 فستان سهرة", "$32"), ("👜 حقيبة يد", "$18"), ("👟 حذاء رياضي", "$25")],
        "yemen": [("🍯 عسل سدر", "15,000 ريال"), ("💍 فضة", "25,000 ريال"), ("🪔 بخور", "8,000 ريال")]
    }
    
    products = products_data.get(st.session_state.selected_market, [])
    cols = st.columns(3)
    for i, (name, price) in enumerate(products):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); border-radius: 15px; padding: 1rem; text-align: center;">
                <div style="font-size: 3rem;">{name.split()[0]}</div>
                <h4>{name}</h4>
                <p>{price}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"شراء {name}", key=f"buy_{i}"):
                st.success(f"تم إضافة {name} إلى السلة")

# عرض المحادثة
st.markdown("---")
st.markdown("## 💬 تحدث مع SaeedDataBot")

for msg in st.session_state.chat_history:
    if msg["role"] == "bot":
        st.markdown(f'<div class="chat-message bot-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message user-message">🗣️ {msg["content"]}</div>', unsafe_allow_html=True)

# إدخال المستخدم
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("اكتب رسالتك هنا...", key="user_input", label_visibility="collapsed")
with col2:
    send_button = st.button("📤 إرسال", use_container_width=True)

if send_button and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    reply = bot.generate_response(user_input)
    st.session_state.chat_history.append({"role": "bot", "content": reply})
    st.rerun()

# زر تشغيل صوت المؤسس
st.markdown("---")
if st.button("🎙️ استمع لصوت المؤسس سعيد المسوري", use_container_width=True):
    voice_html = bot.get_voice_html()
    if voice_html:
        st.components.v1.html(voice_html, height=0)
    else:
        st.warning("⚠️ ملف الصوت غير موجود، تأكد من وجود Saeed_Voice_01.m4a")

# التذييل
st.markdown("---")
st.markdown('<p style="text-align: center;">© 2025 SaeedMarktAds - SaeedDataBot | قريباً: دعم المحافظ اليمنية</p>', unsafe_allow_html=True)

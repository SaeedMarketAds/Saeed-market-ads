import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
import pandas as pd
import nest_asyncio
from streamlit_chat import message
import asyncio

# تطبيق nest_asyncio لحل مشاكل الحلقات المتزامنة
nest_asyncio.apply()

# إعداد الصفحة
st.set_page_config(
    page_title="Saeed Market AI",
    page_icon="🤖",
    layout="wide"
)

# CSS المخصص للتدرج اللوني (الطريقة الصحيحة)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 50%, #fad0c4 100%);
    }
    .main-header {
        background: linear-gradient(135deg, #2c3e50, #1a1a2e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# عنوان التطبيق
st.markdown('<h1 class="main-header">🤖 Saeed Market AI | محرك 3.5 Flash + صوت</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center">تسريع فائق بالذكاء الاصطناعي | صورة ناطقة | كود SHEIN: WL7KA</p>', unsafe_allow_html=True)

# تهيئة نموذج Gemini
try:
    # ضع مفتاح API الخاص بك هنا
    API_KEY = st.secrets.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.success("✅ تم توصيل محرك Gemini 3.5 Flash بنجاح!")
except Exception as e:
    st.error(f"❌ خطأ في توصيل Gemini: {e}")

# واجهة الدردشة
st.subheader("💬 الدردشة مع المساعد الذكي")

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "مرحباً بك في متجري! كيف يمكنني مساعدتك اليوم؟"}]

# عرض سجل المحادثة
for msg in st.session_state.messages:
    message(msg["content"], is_user=(msg["role"] == "user"), key=str(hash(msg["content"] + str(msg["role"]))))

# إدخال المستخدم
user_input = st.chat_input("اكتب سؤالك هنا...")

if user_input:
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True)
    
    with st.spinner("🤔 جاري التفكير..."):
        try:
            # إرسال الطلب إلى Gemini
            response = model.generate_content(user_input)
            bot_response = response.text
            
            # إضافة رد البوت
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            message(bot_response, is_user=False)
            
            # تحويل النص إلى صوت
            tts = gTTS(text=bot_response[:500], lang="ar")
            tts.save("response.mp3")
            st.audio("response.mp3", format="audio/mp3")
            
        except Exception as e:
            st.error(f"حدث خطأ: {e}")

# عرض المنتجات
st.subheader("🛍️ منتجات SHEIN")
shein_products = [
    {"name": "SHEIN Playful Pals Coat", "price": "$19.39", "link": "https://onelink.shein.com/38/5shrzfcizjmg"},
    {"name": "Elegant Design Shirt", "price": "$14.18", "link": "https://onelink.shein.com/38/5shune7n90yf"},
]

for product in shein_products:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.write(f"**{product['name']}**")
    with col2:
        st.write(product['price'])
    with col3:
        st.link_button("شراء", product['link'])

# معلومات إضافية
with st.sidebar:
    st.header("🎁 كود الخصم")
    st.code("WL7KA", language="text")
    st.markdown("خصم 60% للمستخدمين الجدد")
    
    st.header("📦 المكتبات المستخدمة")
    libraries = ["streamlit", "google-generativeai", "gtts", "requests", 
                 "beautifulsoup4", "pandas", "python-telegram-bot", 
                 "streamlit_chat", "nest_asyncio"]
    for lib in libraries:
        st.write(f"- {lib}")

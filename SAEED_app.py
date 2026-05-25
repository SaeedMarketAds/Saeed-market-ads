import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
import requests
import os

# --- إعدادات الصفحة الرسمية للمنظومة ---
st.set_page_config(page_title="Saeed DataBot 2026", layout="wide")

# --- 1. إعداد مفاتيحك السرية ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"] 
except Exception as e:
    st.error("تنبيه: تأكد من ضبط مفاتيح (Secrets) في منصة Streamlit")

# --- 2. تهيئة مخزن الحالة ---
if "bot_response" not in st.session_state:
    st.session_state.bot_response = ""

# --- الواجهة الرئيسية ---
st.title("Saeed MarketAds - المنظومة الذكية 🎙️🤖")

col_avatar, col_chat = st.columns([1, 1.2])

with col_avatar:
    st.subheader("🤖 الكيان: Saeed DataBot")
    st.image("saeed.jpg", use_container_width=True)
    st.write("🎵 **هوية المطور الصوتية (سعيد المسوري)**")
    st.audio("saeed_voice.mp3")

with col_chat:
    st.subheader("💬 حوار تفاعلي")
    audio = mic_recorder(start_prompt="🎤 ابدأ التحدث", stop_prompt="🛑 أوقف التسجيل", key='saeed_voice_recorder')
    conversation_box = st.empty()

# دالة التليجرام
def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    return requests.post(url, json=payload).json()

# --- 3. المعالجة ---
if audio:
    with conversation_box.container():
        st.info("⏳ جاري المعالجة بصوت سعيد المسوري...")
        try:
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            response = model.generate_content(["أنت سعيد داتابوت، أجب باحترافية تسويقية بلسان سعيد المسوري", {"mime_type": "audio/wav", "data": audio['bytes']}])
            
            st.session_state.bot_response = response.text
            st.success("✨ تم صياغة المخرج البرمجي!")
            send_to_telegram(response.text)
        except Exception as e:
            st.error(f"خطأ: {e}")

# --- 4. العرض الصوتي ---
if st.session_state.bot_response:
    with conversation_box.container():
        st.subheader("📝 النص:")
        st.markdown(st.session_state.bot_response)
        
        # هنا التعديل الجوهري: تشغيل ملفك الخاص بدلاً من gTTS
        st.subheader("🔊 الرد بصوت سعيد المسوري:")
        if os.path.exists("saeed_voice.mp3"):
            st.audio("saeed_voice.mp3", format="audio/mp3", autoplay=True)
        else:
            st.warning("⚠️ ملف saeed_voice.mp3 غير موجود في المجلد!")

# --- 5. زر البث ---
if st.button("نشر المنشور"):
    send_to_telegram(st.session_state.bot_response)
    st.success("تم النشر!")

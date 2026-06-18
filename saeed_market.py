import streamlit as st
import base64
import os
from saeed_databot import SaeedDataBot

# إعدادات الصفحة
st.set_page_config(
    page_title="SaeedMarketAds",
    page_icon="🛒",
    layout="centered"
)

# تهيئة البوت
@st.cache_resource
def load_bot():
    return SaeedDataBot()

bot = load_bot()

# عرض الصورة الرمزية
avatar_path = "Saeed_DataBot_Avatar.jpg"
if os.path.exists(avatar_path):
    st.image(avatar_path, width=150)
else:
    st.warning("⚠️ الصورة الرمزية غير موجودة")

# العنوان
st.title("🛒 SaeedMarketAds")
st.caption("ذكاء اصطناعي عابر للحدود")

# دالة تشغيل الصوت
def play_voice(text):
    voice_path = "new_voice.mp3"  # أو Saeed_DataBot_Voice.mp3
    
    # محاولة تشغيل الصوت مباشرة
    if os.path.exists(voice_path):
        with open(voice_path, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_html = f'''
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        '''
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.warning("⚠️ ملف الصوت غير موجود، جارٍ استخدام TTS بديل")
        # استخدام pyttsx3 أو gTTS كبديل
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except:
            st.info("🔇 لا يمكن تشغيل الصوت")

# واجهة الدردشة
st.subheader("💬 تحدث مع البوت")

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "السلام عليكم ورحمة الله وبركاته، كيف أخدمك اليوم؟"}
    ]

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# إدخال المستخدم
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # الحصول على رد البوت
    with st.chat_message("assistant"):
        response = bot.get_response(prompt)
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # تشغيل الصوت
        play_voice(response)

# زر إعادة تعيين المحادثة
if st.button("🔄 بدء محادثة جديدة"):
    st.session_state.messages = [
        {"role": "assistant", "content": "السلام عليكم ورحمة الله وبركاته، كيف أخدمك اليوم؟"}
    ]
    st.rerun()

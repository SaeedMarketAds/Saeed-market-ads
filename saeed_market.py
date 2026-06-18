import streamlit as st
import base64
import os

# إعدادات الصفحة
st.set_page_config(
    page_title="SaeedMarketAds",
    page_icon="🛒",
    layout="centered"
)

# عرض الصورة الرمزية
avatar_path = "Saeed_DataBot_Avatar.jpg"
if os.path.exists(avatar_path):
    st.image(avatar_path, width=150)
else:
    st.warning("⚠️ الصورة (Saeed_DataBot_Avatar.jpg) غير موجودة في المجلد")

st.title("🛒 SaeedMarketAds")
st.caption("ذكاء اصطناعي عابر للحدود")

# دالة تشغيل الصوت
def get_audio_player(audio_path):
    if os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        return f'''
            <audio controls>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        '''
    return None

# --- تعديل اسم الملف هنا ---
voice_file = "new_voice.mp3" 

# عرض مشغل الصوت
st.subheader("🎵 استمع إلى البوت")
audio_html = get_audio_player(voice_file)
if audio_html:
    st.markdown(audio_html, unsafe_allow_html=True)
else:
    st.warning(f"⚠️ ملف الصوت '{voice_file}' غير موجود، تأكد من رفعه في المجلد الرئيسي")

# واجهة الدردشة
st.subheader("💬 تحدث مع البوت")

# رسالة ترحيبية
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
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # رد البوت
    response = "وعليكم السلام ورحمة الله وبركاته، كيف أخدمك اليوم؟"
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)

# زر مسح المحادثة
if st.button("🔄 بدء من جديد"):
    st.session_state.messages = [
        {"role": "assistant", "content": "السلام عليكم ورحمة الله وبركاته، كيف أخدمك اليوم؟"}
    ]
    st.rerun()

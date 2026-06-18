import streamlit as st
import base64
import os

# إعدادات الصفحة
st.set_page_config(
    page_title="SaeedMarketAds",
    page_icon="🛒",
    layout="centered"
)

# ============================================
# ضع الدالة هنا (بعد الاستيرادات)
# ============================================

def get_audio_autoplay(audio_path):
    if os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        return f'''
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        '''
    return None

# ============================================
# بقية الكود
# ============================================

# عرض الصورة الرمزية
avatar_path = "Saeed_DataBot_Avatar.jpg"
if os.path.exists(avatar_path):
    st.image(avatar_path, width=150)
else:
    st.warning("⚠️ الصورة غير موجودة")

st.title("🛒 SaeedMarketAds")
st.caption("ذكاء اصطناعي عابر للحدود")

# استخدام الدالة
voice_file = "new_voice.mp3"
audio_html = get_audio_autoplay(voice_file)
if audio_html:
    st.markdown(audio_html, unsafe_allow_html=True)
else:
    st.warning(f"⚠️ ملف الصوت '{voice_file}' غير موجود")

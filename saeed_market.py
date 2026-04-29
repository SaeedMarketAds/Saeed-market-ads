import streamlit as st
import os

# إعدادات الصفحة
st.set_page_config(page_title="Saeed AI", page_icon="🤖")

# تحديد المسارات (تأكد أن المجلد اسمه assets)
base_path = "assets/"
img_official = os.path.join(base_path, "saeed_ai.jpg")
img_avatar = os.path.join(base_path, "saeed_avatar.jpg")
welcome_audio = os.path.join(base_path, "welcome_voice.mp3")

# تذكر حالة الصورة
if 'current_img' not in st.session_state:
    st.session_state.current_img = img_official

# الواجهة الرئيسية
st.title("🤖 نظام سعيد AI الذكي")

# عرض الصورة في الأعلى
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(st.session_state.current_img, use_container_width=True)

# زر التبديل والترحيب
if st.button("🔄 تبديل الهوية وتشغيل الترحيب", use_container_width=True):
    # تبديل الصورة
    if st.session_state.current_img == img_official:
        st.session_state.current_img = img_avatar
    else:
        st.session_state.current_img = img_official
    
    # تشغيل الصوت إذا كان موجوداً
    if os.path.exists(welcome_audio):
        st.audio(welcome_audio, format="audio/mp3", autoplay=True)
    
    st.rerun()

st.markdown("---")
st.success("أهلاً بك يا مصمم سوق سعيد، الملفات الآن مرتبة والبرمجة جاهزة!")

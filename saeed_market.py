import streamlit as st
import os

# إعداد الصفحة
st.set_page_config(page_title="SaeedMarketAds", page_icon="📦")

# المسارات
base_path = "." # تم التعديل ليتناسب مع المجلد الرئيسي
img_official = os.path.join(base_path, "saeed.jpg")
img_avatar = os.path.join(base_path, "ROBOT.jpg") # تأكد من اسم ملف الروبوت
welcome_audio = os.path.join(base_path, "welcome_voice.mp3")

# تذكر حالة الصورة
if 'current_img' not in st.session_state:
    st.session_state.current_img = img_official

# الواجهة الرئيسية
st.title("📦 نظام SaeedMarketAds الذكي")

# عرض الصورة
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(st.session_state.current_img, use_container_width=True)

# زر التبديل
if st.button("🔄 تبديل الهوية والترحيب"):
    if st.session_state.current_img == img_official:
        st.session_state.current_img = img_avatar
    else:
        st.session_state.current_img = img_official
    
    # تشغيل الصوت
    if os.path.exists(welcome_audio):
        st.audio(welcome_audio, format="audio/mp3", autoplay=True)
    st.rerun()

st.markdown("---")
st.success("أهلاً بك يا سعيد، النظام يعمل والصفحات جاهزة للإضافة في مجلد pages/")

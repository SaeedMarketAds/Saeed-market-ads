
import streamlit as st
import os

# إعداد الصفحة
st.set_page_config(page_title="سعيد ماركت - SaeedMarketAds", page_icon="🚀", layout="centered")

# العنوان الرئيسي
st.title("🚀 إمبراطورية \"سعيد ماركت\" | رؤية مدروسة وذكاء اصطناعي عابر للحدود 🌍")
st.subheader("مرحباً بكم في مستقبل التسويق الرقمي")

# عرض الصورة التعريفية
try:
    st.image("saeed_avatar.jpg", caption="سعيد المسوري - مطور النظام", width=300)
except:
    st.info("... جاري تحميل الهوية البصرية")

st.write("---")

# قسم المساعد الذكي
st.subheader("المساعد الذكي (Saeed DataBot) 🤖")
st.write("يقوم البوت بمهام تحليل البيانات، توليد الردود التفاعلية الصوتية، والإجابة على الاستفسارات.")

# مسارات الملفات الصوتية
welcome_voice_path = "welcome_voice.mp3"
saeed_voice_path = "saeed_voice.mp3"

st.write("### الاستماع إلى المساعد الصوتي")

# عرض مشغل الصوت لملف الترحيب
if os.path.exists(welcome_voice_path):
    st.write("صوت الترحيب:")
    st.audio(welcome_voice_path, format="audio/mp3")
else:
    st.info("جاري تحميل ملف الترحيب (تأكد من وجود الملف welcome_voice.mp3 في المستودع).")

# عرض مشغل الصوت لملف التفاعل
if os.path.exists(saeed_voice_path):
    st.write("صوت التفاعل:")
    st.audio(saeed_voice_path, format="audio/mp3")
else:
    st.info("قم بسؤال البوت ليتم توليد الصوت الخاص به.")

st.write("---")

# قسم الخدمات
st.write("### خدماتنا المتقدمة")
col1, col2 = st.columns(2)
with col1:
    st.success("✅ تسويق ذكي عبر AI")
    st.success("✅ أتمتة إعلانات SHEIN")
with col2:
    st.success("✅ بناء هويات رقمية")
    st.success("✅ استشارات برمجية")

# تذييل الصفحة
st.write("---")
st.info("حقوق التطوير محفوظة © 2026 | SaeedMarketAds")

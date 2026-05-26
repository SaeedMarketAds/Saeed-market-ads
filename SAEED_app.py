import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# إعداد الصفحة
st.set_page_config(page_title="Saeed DataBot", page_icon="🤖")

# تحميل المفتاح السري
# الطريقة الأفضل والأكثر اختصاراً
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# واجهة التطبيق
st.title("🚀 Saeed DataBot")
st.image("saeed.jpg", width=200) # عرض صورتك الموجودة في المجلد
st.subheader("مساعدك الذكي للتفاعل مع السوق")

user_input = st.text_input("اطرح سؤالك هنا:")

if st.button("تفاعل مع البوت"):
    if user_input:
        if not API_KEY:
            st.error("خطأ: مفتاح الـ API غير موجود. تأكد من ملف .env")
        else:
            try:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel('gemini-pro')
                
                with st.spinner('جاري التحليل...'):
                    response = model.generate_content(user_input)
                    
                st.success("الرد:")
                st.write(response.text)
                
                # إضافة خيار لسماع الرد إذا أردت لاحقاً
                st.audio("welcome_voice.mp3") 
                
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
    else:
        st.warning("الرجاء كتابة سؤال!")

# تذييل الصفحة
st.sidebar.info("مشروع SaeedMarketAds - النسخة 1.0")

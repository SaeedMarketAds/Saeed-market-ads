import streamlit as st
import google.generativeai as genai
import os

# إعداد الصفحة
st.set_page_config(page_title="Saeed DataBot", page_icon="🚀")

# تحميل المفتاح السري من Streamlit Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# واجهة التطبيق
st.title("🚀 Saeed DataBot")
if os.path.exists("saeed.jpg"):
    st.image("saeed.jpg", width=200)
st.subheader("مساعدك الذكي للتفاعل مع السوق")

user_input = st.text_input("اطرح سؤالك هنا:")

if st.button("تفاعل مع البوت"):
    if user_input:
        if not API_KEY:
            st.error("مفتاح API غير موجود. تأكد من إضافته في إعدادات Streamlit.")
        else:
            try:
                genai.configure(api_key=API_KEY)
                # تم التعديل هنا لاستخدام النموذج الجديد
                model = genai.GenerativeModel('gemini-3.5-flash')
                
                with st.spinner('جاري التحليل...'):
                    response = model.generate_content(user_input)
                
                st.success("الرد:")
                st.write(response.text)
                
                # التحقق من وجود ملف الصوت قبل تشغيله
                if os.path.exists("welcome_voice.mp3"):
                    st.audio("welcome_voice.mp3")
                    
            except Exception as e:
                st.error(f"حدث خطأ تقني: {e}")
    else:
        st.warning("الرجاء كتابة سؤال!")

# تذييل الصفحة
st.sidebar.info("مشروع saeedmarketads - 1.0")

import streamlit as st
import os
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Saeed MarketAds", layout="wide")

# إعداد API
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

st.title("مرحباً بك في Saeed DataBot")

# إنشاء التبويبات
tab1, tab2 = st.tabs(["🤖 Saeed DataBot", "➕ إضافة منتج جديد"])

# تبويب الذكاء الاصطناعي
with tab1:
    st.subheader("اسأل الذكاء الاصطناعي")
    user_input = st.text_input("اطرح سؤالك عن المنتجات:", key="ai_input")
    if st.button("إرسال السؤال"):
        if user_input and api_key:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(user_input)
                st.write(response.text)
            except Exception as e:
                st.error(f"خطأ في الذكاء الاصطناعي: {e}")
        elif not api_key:
            st.warning("مفتاح API غير موجود في الإعدادات.")

# تبويب إضافة المنتجات (منفصل تماماً)
with tab2:
    st.subheader("نشر منتج جديد")
    with st.form("add_product_form", clear_on_submit=True):
        prod_name = st.text_input("اسم المنتج")
        prod_link = st.text_input("رابط المنتج")
        submitted = st.form_submit_button("نشر المنتج الآن")
        
        if submitted:
            if prod_name and prod_link:
                st.success(f"تم بنجاح نشر المنتج: {prod_name}")
                st.info(f"الرابط: {prod_link}")
            else:
                st.error("يرجى ملء جميع الحقول!")

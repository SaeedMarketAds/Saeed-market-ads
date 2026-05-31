import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Saeed MarketAds", layout="wide")

st.title("🚀 نظام سعيد المتكامل")

# التبديل بين التبويبات
tab1, tab2 = st.tabs(["🤖 Saeed DataBot", "📦 لوحة تحكم المتجر"])

# تبويب البوت
with tab1:
    st.subheader("مساعدك الذكي")
    if os.path.exists("ROBOT.jpg"): # تأكد من الاسم ROBOT.jpg كما طلبت
        st.image("ROBOT.jpg", width=150)
    
    user_input = st.text_input("اطرح سؤالك عن المنتجات:")
    if st.button("تفاعل مع البوت"):
        # هنا يتم استدعاء Gemini (تأكد من إعداد API_KEY)
        st.write("جارٍ المعالجة...")

# تبويب لوحة التحكم
with tab2:
    st.subheader("📦 لوحة تحكم المتجر")
    with st.form("product_form"):
        prod_name = st.text_input("اسم المنتج")
        prod_price = st.number_input("السعر", min_value=0.0)
        prod_desc = st.text_area("وصف المنتج")
        submit = st.form_submit_button("نشر المنتج")
        
        if submit:
            st.success(f"تم إضافة {prod_name} بنجاح!")

st.sidebar.info("مشروع saeedmarketads - 1.0")

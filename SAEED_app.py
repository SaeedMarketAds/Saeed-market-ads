import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Saeed MarketAds", layout="wide")

# إعداد الـ API
API_KEY = st.secrets.get("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

st.title("🚀 نظام سعيد المتكامل")
tab1, tab2 = st.tabs(["🤖 Saeed DataBot", "📦 لوحة تحكم المتجر"])

with tab1:
    st.subheader("مساعدك الذكي")
    if os.path.exists("ROBOT.jpg"):
        st.image("ROBOT.jpg", width=150)
    
    user_input = st.text_input("اطرح سؤالك عن المنتجات:")
    if st.button("تفاعل مع البوت"):
        if user_input:
            try:
                model = genai.GenerativeModel('gemini-3.5-flash')
                response = model.generate_content(user_input)
                st.success("الرد:")
                st.write(response.text)
            except Exception as e:
                st.error(f"خطأ في الاتصال: {e}")
        else:
            st.warning("الرجاء كتابة سؤال!")

with tab2:
    st.subheader("📦 لوحة تحكم المتجر")
    with st.form("product_form"):
        prod_name = st.text_input("اسم المنتج")
        prod_price = st.number_input("السعر", min_value=0.0)
        prod_desc = st.text_area("وصف المنتج")
        hidden_link = st.text_input("رابط المنتج المخفي")
        img_link = st.text_input("رابط صورة المنتج")
        
        submit = st.form_submit_button("نشر المنتج")
        
        if submit:
            st.balloons() # تأثير احتفالي عند النشر
            st.success(f"تم نشر {prod_name} بنجاح في النظام!")
            st.write("---")
            st.write(f"**المنتج:** {prod_name}")
            st.write(f"**السعر:** {prod_price}")
            if img_link: st.image(img_link, width=200)
            st.info(f"الرابط المخفي: {hidden_link}")

st.sidebar.info("مشروع saeedmarketads - 1.0")

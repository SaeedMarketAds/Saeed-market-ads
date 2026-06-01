import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Saeed MarketAds", layout="wide")

api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

st.title("مرحباً بك في Saeed DataBot")
tab1, tab2 = st.tabs(["Saeed DataBot", "إضافة منتج جديد"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("saeed.jpg"):
            st.image("saeed.jpg", width=150)
    with col2:
        if os.path.exists("ROBOT.jpg"):
            st.image("ROBOT.jpg", width=150)

    user_input = st.text_input("اطرح سؤالك:")
    if st.button("إرسال"):
        if user_input:
            try:
                model = genai.GenerativeModel('gemini-3.5-flash')
                response = model.generate_content(user_input)
                st.write(response.text)
            except Exception as e:
                st.error(f"خطأ: {e}")

with tab2:
    st.subheader("إضافة منتج جديد")
    with st.form("product_form"):
        prod_name = st.text_input("اسم المنتج")
        prod_price = st.number_input("السعر", min_value=0.0)
        hidden_link = st.text_input("رابط المنتج")
        submit = st.form_submit_button("نشر")
        
        if submit:
            st.success(f"تمت إضافة {prod_name}")
            st.info(f"الرابط: {hidden_link}")

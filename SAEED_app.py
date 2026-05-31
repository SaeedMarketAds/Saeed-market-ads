import streamlit as st
import os
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Saeed MarketAds", layout="wide")

st.title("🚀 نظام سعيد المتكامل")

# التبديل بين التبويبات
tab1, tab2 = st.tabs(["🤖 Saeed DataBot", "📦 لوحة تحكم المتجر"])

# تبويب البوت
with tab1:
    st.subheader("مساعدك الذكي")
    # عرض الصور الشخصية وصورة الروبوت
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("saeed.jpg"):
            st.image("saeed.jpg", width=150, caption="المؤسس")
    with col2:
        if os.path.exists("ROBOT.jpg"):
            st.image("ROBOT.jpg", width=150, caption="Saeed DataBot")
    
    user_input = st.text_input("اطرح سؤالك عن المنتجات هنا:")
    if st.button("تفاعل مع البوت"):
        if user_input:
            st.write("جارٍ المعالجة بواسطة Saeed DataBot...")
            # هنا يتم وضع منطق استدعاء Gemini الخاص بك
        else:
            st.warning("الرجاء كتابة سؤال!")

# تبويب لوحة التحكم
with tab2:
    st.subheader("📦 لوحة تحكم المتجر")
    with st.form("product_form"):
        prod_name = st.text_input("اسم المنتج")
        prod_price = st.number_input("السعر", min_value=0.0)
        prod_desc = st.text_area("وصف المنتج")
        prod_link = st.text_input("رابط المنتج المخفي")
        prod_img = st.text_input("رابط صورة المنتج")
        
        submit = st.form_submit_button("نشر المنتج")
        
        if submit:
            st.success(f"تم إرسال {prod_name} للنظام بنجاح!")

st.sidebar.info("مشروع saeedmarketads - 1.0")

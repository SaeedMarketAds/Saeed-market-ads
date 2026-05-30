import streamlit as st
import saeed_databot as db  # استيراد ملف البوت الذي يحتوي على دوال قاعدة البيانات

st.title("نظام سعيد المتكامل 🚀")

menu = ["المساعد الذكي (Bot)", "متجر المنتجات (Market)"]
choice = st.sidebar.selectbox("اختر الخدمة:", menu)

if choice == "المساعد الذكي (Bot)":
    st.subheader("تحدث مع سعيد DataBot")
    # ضع كود البوت الخاص بك هنا

elif choice == "متجر المنتجات (Market)":
    st.subheader("لوحة تحكم المتجر")
    # استخدام دوال قاعدة البيانات الموجودة في ملف saeed_databot
    db.init_db() 
    
    with st.form("add_product_form"):
        name = st.text_input("اسم المنتج")
        price = st.number_input("السعر")
        desc = st.text_area("وصف المنتج")
        submit = st.form_submit_button("نشر المنتج")
        if submit:
            db.add_product(name, price, desc)
            st.success("تمت الإضافة!")

    st.write("المنتجات:")
    products = db.get_products()
    st.write(products)

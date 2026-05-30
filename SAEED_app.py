import streamlit as st
import saeed_databot as bot      # وظائف البوت
import saeed_market as market    # وظائف المتجر (تأكد أن هذا هو اسم الملف)

st.title("نظام سعيد المتكامل 🚀")

# القائمة للتنقل بين المشروعين
menu = ["المساعد الذكي (Bot)", "متجر المنتجات (Market)"]
choice = st.sidebar.selectbox("اختر الخدمة:", menu)

if choice == "المساعد الذكي (Bot)":
    st.subheader("تحدث مع سعيد DataBot")
    # هنا تضع كود البوت الذي كنت تعمل عليه
    # ...

elif choice == "متجر المنتجات (Market)":
    st.subheader("لوحة تحكم المتجر")
    # هنا تستدعي وظائف ملف saeed_market.py
    # مثل market.show_products() أو market.add_product_form()

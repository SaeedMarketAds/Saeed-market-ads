import streamlit as st

# 1. القائمة الجانبية للاختيار
option = st.sidebar.selectbox("اختر الخدمة:", ["(Bot) المساعد الذكي", "(Market) متجر المنتجات"])

# 2. عرض المحتوى بناءً على الاختيار
if option == "(Bot) المساعد الذكي":
    st.title("نظام سعيد المتكامل 🚀")
    st.subheader("DataBot تحدث مع سعيد")
    
    # هنا يجب وضع كود المحادثة لكي يظهر مربع النص
    if prompt := st.chat_input("اكتب رسالتك هنا..."):
        st.write(f"سعيد يقول: استلمت رسالتك: {prompt}")
        # هنا تضع المنطق الخاص بك للرد على الرسالة

elif option == "(Market) متجر المنتجات":
    st.title("لوحة تحكم المتجر 📦")
    # ضع هنا كود عرض المنتجات الخاص بك
    name = st.text_input("اسم المنتج")
    price = st.number_input("السعر", min_value=0.0)
    # ... باقي كود المتجر

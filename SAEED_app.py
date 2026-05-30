
import streamlit as st
import saeed_databot as db

db.init_db()
st.title("نظام سعيد المتكامل 🚀")

menu = ["المساعد الذكي (Bot)", "متجر المنتجات (Market)"]
choice = st.sidebar.selectbox("اختر الخدمة:", menu)

if choice == "المساعد الذكي (Bot)":
    st.subheader("تحدث مع سعيد DataBot")
    st.info("جاهز للاستخدام...")

elif choice == "متجر المنتجات (Market)":
    st.subheader("لوحة تحكم المتجر 📦")
    with st.form("add_product_form"):
        name = st.text_input("اسم المنتج")
        price = st.number_input("السعر", min_value=0.0)
        desc = st.text_area("وصف المنتج")
        submit = st.form_submit_button("نشر المنتج")
        if submit:
            db.add_product(name, price, desc)
            st.success("تمت الإضافة!")
            st.rerun()

    st.write("### المنتجات المتاحة:")
    products = db.get_products()
    for p in products:
        col1, col2 = st.columns([0.8, 0.2])
        col1.write(f"✅ **{p[1]}** | السعر: {p[2]}")
        if col2.button("حذف", key=f"del_{p[0]}"):
            db.delete_product(p[0])
            st.rerun()

import streamlit as st
import saeed_databot as db

st.title("لوحة تحكم سعيد ماركت 📦")

# تهيئة قاعدة البيانات
db.init_db()

# إضافة نموذج إدخال بسيط للتجربة
with st.form("add_product_form"):
    name = st.text_input("اسم المنتج")
    price = st.number_input("السعر", min_value=0.0)
    desc = st.text_area("وصف المنتج")
    submit = st.form_submit_button("نشر المنتج")

    if submit:
        db.add_product(name, price, desc)
        st.success("تمت إضافة المنتج بنجاح!")

# عرض المنتجات
st.subheader("قائمة المنتجات الحالية")
products = db.get_products()
if products:
    for p in products:
        st.write(f"المنتج: {p[1]} - السعر: {p[2]}")
else:
    st.write("لا توجد منتجات حالياً")

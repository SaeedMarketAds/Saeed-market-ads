import streamlit as st
import saeed_databot  # استدعاء ملفك

# تهيئة قاعدة البيانات عند بدء التشغيل
saeed_databot.init_db()

st.title("لوحة تحكم سعيد ماركت")

# نموذج إضافة منتج
with st.form("product_form"):
    name = st.text_input("اسم المنتج")
    price = st.number_input("السعر", min_value=0.0)
    description = st.text_area("وصف المنتج")
    submitted = st.form_submit_button("نشر المنتج")
    
    if submitted:
        saeed_databot.add_product(name, price, description)
        st.success("تم إضافة المنتج بنجاح!")

# عرض قائمة المنتجات الحالية
st.subheader("قائمة المنتجات الحالية")
products = saeed_databot.get_products()

if not products:
    st.info("لا توجد منتجات حالياً")
else:
    for p in products:
        st.write(f"### {p[1]} - {p[2]} ريال")
        st.write(f"الوصف: {p[3]}")
        st.markdown("---")

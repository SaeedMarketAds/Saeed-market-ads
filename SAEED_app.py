import streamlit as st
import shein_products  # تأكد أن ملف shein_products.py موجود في نفس المجلد

# إعداد الصفحة
st.set_page_config(page_title="Saeed Market - العروض الموحدة", layout="wide")

# العنوان الرئيسي
st.title("🛍️ Saeed Market | وجهتك الموحدة لأفضل العروض")
st.markdown("---")

# إنشاء الأعمدة للمتاجر
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("SHEIN")
    st.write("أحدث صيحات الموضة العالمية.")
    if st.button("تصفح عروض SHEIN", key="shein"):
        st.session_state.store = "SHEIN"

with col2:
    st.subheader("AliExpress")
    st.write("إلكترونيات ومنتجات مميزة.")
    if st.button("تصفح عروض AliExpress", key="ali"):
        st.session_state.store = "AliExpress"

with col3:
    st.subheader("Noon")
    st.write("عروض محلية وتوصيل سريع.")
    if st.button("تصفح عروض Noon", key="noon"):
        st.session_state.store = "Noon"

st.markdown("---")

# عرض المحتوى بناءً على اختيار المستخدم
if 'store' in st.session_state:
    if st.session_state.store == "SHEIN":
        st.header("أحدث عروض SHEIN")
        for product in shein_products.products:
            st.write(f"### {product['name']}")
            st.write(f"السعر: {product['price']}")
            st.link_button("شراء الآن", product['link'])

    elif st.session_state.store == "AliExpress":
        st.header("أحدث عروض AliExpress")
        st.write("قسم AliExpress قيد التجهيز...")

    elif st.session_state.store == "Noon":
        st.header("أحدث عروض Noon")
        st.write("قسم Noon قيد التجهيز...")
else:
    st.write("يرجى اختيار أحد المتاجر أعلاه للبدء بالتسوق.")

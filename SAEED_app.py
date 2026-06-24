import streamlit as st

st.set_page_config(page_title="Saeed Market - العروض الموحدة", layout="wide")

# العنوان الرئيسي مع لمسة احترافية
st.title("🛍️ Saeed Market | وجهتك الموحدة لأفضل العروض")
st.markdown("---")

# إنشاء أعمدة لعرض المتاجر الثلاثة بشكل متوازي
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
    st.header(f"أنت الآن تتصفح عروض: {st.session_state.store}")
    # هنا سيتم ربط كل متجر بملف البيانات الخاص به (مثل shein_products.py)
    st.info(f"جاري تحميل أحدث المنتجات من {st.session_state.store}...")
else:
    st.write("يرجى اختيار أحد المتاجر أعلاه للبدء بالتسوق.")

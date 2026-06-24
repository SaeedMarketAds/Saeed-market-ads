import streamlit as st
import shein_products  # تأكد من أن ملف shein_products.py موجود في نفس المجلد

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Saeed Market - العروض الموحدة", layout="wide")

# --- دالة التخزين المسرعة ---
@st.cache_data
def get_products(store_name):
    # هنا نقوم بجلب البيانات من الملفات (يمكنك إضافة المزيد من المتاجر لاحقاً)
    if store_name == "SHEIN":
        return shein_products.products
    return []

# --- العنوان الرئيسي ---
st.title("🛍️ Saeed Market | وجهتك الموحدة لأفضل العروض")
st.markdown("---")

# --- واجهة الأزرار (القائمة العلوية) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("SHEIN")
    if st.button("تصفح عروض SHEIN", key="shein"):
        st.session_state.store = "SHEIN"

with col2:
    st.subheader("AliExpress")
    if st.button("تصفح عروض AliExpress", key="ali"):
        st.session_state.store = "AliExpress"

with col3:
    st.subheader("Noon")
    if st.button("تصفح عروض Noon", key="noon"):
        st.session_state.store = "Noon"

st.markdown("---")

# --- منطقة عرض المحتوى ---
if 'store' in st.session_state:
    if st.session_state.store == "SHEIN":
        st.header("أحدث عروض SHEIN")
        products = get_products("SHEIN") 
        for product in products:
            st.write(f"### {product['name']}")
            st.write(f"السعر: {product['price']}")
            st.link_button("شراء الآن", product['link'])
            
    elif st.session_state.store == "AliExpress":
        st.header("أحدث عروض AliExpress")
        st.write("قسم قيد التجهيز...")
        
    elif st.session_state.store == "Noon":
        st.header("أحدث عروض Noon")
        st.write("قسم قيد التجهيز...")
else:
    st.info("مرحباً بك! يرجى اختيار أحد المتاجر أعلاه للبدء بالتسوق.")

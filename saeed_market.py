import streamlit as st
import os
import saeed_databot  # استدعاء ملف الدوال الذي أنشأته

# 1. تهيئة قاعدة البيانات عند بدء التشغيل
saeed_databot.init_db()

# إعداد الصفحة
st.set_page_config(page_title="SaeedMarketAds", page_icon="📦")

# ... (هنا ضع كود الصور والترحيب الخاص بك كما كان في البداية) ...

# 2. إضافة نموذج إدخال المنتجات (من لوحة التحكم)
st.title("📦 لوحة تحكم SaeedMarketAds")

with st.form("product_form", clear_on_submit=True):
    name = st.text_input("اسم المنتج")
    price = st.number_input("السعر", min_value=0.0)
    description = st.text_area("وصف المنتج")
    submitted = st.form_submit_button("نشر المنتج")
    
    if submitted:
        if name:
            saeed_databot.add_product(name, price, description) # استدعاء دالة الإضافة
            st.success("تم إضافة المنتج بنجاح!")
            st.rerun()
        else:
            st.error("يرجى إدخال اسم المنتج")

# 3. عرض المنتجات
st.subheader("📋 المنتجات الحالية")
products = saeed_databot.get_products() # استدعاء دالة القراءة

if not products:
    st.info("لا توجد منتجات حالياً")
else:
    for p in products:
if st.button("نشر المنتج"):
# يجب أن يكون هناك كود هنا بمسافة بادئة (4 مسافات أو Tab)

        st.write(f"**الوصف:** {p[3]}")
        st.markdown("---")

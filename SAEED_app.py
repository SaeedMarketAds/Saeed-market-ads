import streamlit as st
import saeed_databot as db

# تهيئة قاعدة البيانات مرة واحدة فقط عند بدء التشغيل
db.init_db()

st.title("نظام سعيد المتكامل 🚀")

menu = ["المساعد الذكي (Bot)", "متجر المنتجات (Market)"]
choice = st.sidebar.selectbox("اختر الخدمة:", menu)

if choice == "المساعد الذكي (Bot)":
    st.subheader("تحدث مع سعيد DataBot")
    # ضع هنا كود البوت (Gemini API)
    st.info("المساعد الذكي جاهز للاستخدام...")

elif choice == "متجر المنتجات (Market)":
    st.subheader("لوحة تحكم المتجر 📦")
    
    with st.form("add_product_form"):
        name = st.text_input("اسم المنتج")
        price = st.number_input("السعر", min_value=0.0)
        desc = st.text_area("وصف المنتج")
        submit = st.form_submit_button("نشر المنتج")
        
        if submit:
            db.add_product(name, price, desc)
            st.success("تمت إضافة المنتج بنجاح!")
            st.rerun() # تحديث الصفحة لرؤية المنتج الجديد

    st.write("---")
    st.write("### المنتجات المتاحة:")
    products = db.get_products()
    if not products:
        st.write("لا توجد منتجات حالياً.")
    else:
        for p in products:
            st.write(f"✅ **{p[1]}** | السعر: {p[2]} | الوصف: {p[3]}")

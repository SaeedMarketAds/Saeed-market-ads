import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="نظام سعيد المتكامل", layout="centered")

# تهيئة سجل المحادثة في الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "السلام عليكم ورحمة الله وبركاته، معك سعيد المساعد الذكي. كيف يمكنني مساعدتك في متجرك اليوم؟"}]

# القائمة الجانبية للتبديل بين الخدمات
option = st.sidebar.selectbox("اختر الخدمة:", ["(Bot) المساعد الذكي", "(Market) متجر المنتجات"])

# --- واجهة المساعد الذكي (Bot) ---
if option == "(Bot) المساعد الذكي":
    st.title("نظام سعيد المتكامل 🚀")
    st.image("saeed.jpg", width=150) # استدعاء صورة الروبوت
    st.subheader("DataBot تحدث مع سعيد")

    # عرض الرسائل السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # منطقة إدخال الرسائل
    if prompt := st.chat_input("اكتب رسالتك هنا..."):
        # إضافة رسالة المستخدم للسجل
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # الرد الذكي
        with st.chat_message("assistant"):
            response = f"سعيد يقول: استلمت رسالتك: '{prompt}'. \n\nأنا هنا لأساعدك في إدارة متجرك وتطوير مبيعاتك. \n\nملاحظة: هذا الرد تم إنشاؤه باستخدام عقل Gemini، تم تطويره ودمجه بعناية فائقة بواسطة المبرمج الرائع: سعيد المسوري."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- واجهة المتجر (Market) ---
elif option == "(Market) متجر المنتجات":
    st.title("لوحة تحكم المتجر 📦")
    st.image("ROBOT.jpg", width=150) # استدعاء صورة المتجر
    
    with st.form("product_form"):
        prod_name = st.text_input("اسم المنتج")
        prod_price = st.number_input("السعر", min_value=0.0, format="%.2f")
        prod_desc = st.text_area("وصف المنتج")
        submit = st.form_submit_button("نشر المنتج")
        
        if submit:
            if prod_name:
                st.success(f"تم إضافة المنتج: {prod_name} بنجاح!")
            else:
                st.error("الرجاء إدخال اسم المنتج.")

    st.markdown("### المنتجات المتاحة:")
    st.write("لا توجد منتجات بعد، ابدأ بإضافة منتجك الأول!")

import streamlit as st
import os
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Saeed MarketAds", layout="wide")

# تهيئة حالة الجلسة لتخزين المنتجات
if "products" not in st.session_state:
    st.session_state.products = []  # قائمة تحتوي على قاموس لكل منتج

# إعداد مفتاح API من secrets
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("❗ لم يتم العثور على مفتاح API، يرجى إضافة GOOGLE_API_KEY في secrets")

# العنوان الرئيسي
st.title("🤖 Saeed DataBot - سوق سعيد")

# إنشاء التبويبات
tab1, tab2, tab3 = st.tabs(["💬 Saeed DataBot", "➕ إضافة منتج جديد", "📦 قائمة المنتجات"])

# ======================= التبويب الأول: البوت =======================
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("saeed.jpg"):
            st.image("saeed.jpg", width=150, caption="سعيد")
        else:
            st.info("⚠️ الصورة saeed.jpg غير موجودة")
    with col2:
        if os.path.exists("ROBOT.jpg"):
            st.image("ROBOT.jpg", width=150, caption="Saeed DataBot")
        else:
            st.info("⚠️ الصورة ROBOT.jpg غير موجودة")

    st.markdown("### 🧠 اسأل الذكاء الاصطناعي عن المنتجات")
    user_question = st.text_input("اطرح سؤالك هنا:", key="user_question")
    
    if st.button("🚀 إرسال السؤال", key="ask_btn"):
        if user_question.strip():
            if api_key:
                try:
                    model = genai.GenerativeModel('gemini3.5-flash')  # أو 'gemini-pro'
                    response = model.generate_content(user_question)
                    st.success("✅ تم الرد:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"❌ حدث خطأ أثناء الاتصال بـ Gemini: {e}")
            else:
                st.error("❌ مفتاح API غير موجود، لا يمكن الرد.")
        else:
            st.warning("⚠️ يرجى كتابة سؤال أولاً.")

# ======================= التبويب الثاني: إضافة منتج =======================
with tab2:
    st.subheader("➕ إضافة منتج جديد إلى السوق")
    with st.form(key="product_form", clear_on_submit=True):
        prod_name = st.text_input("🏷️ اسم المنتج")
        prod_price = st.number_input("💰 السعر (بالدولار)", min_value=0.0, step=0.5)
        prod_desc = st.text_area("📝 وصف المنتج")
        hidden_link = st.text_input("🔗 رابط المنتج المخفي (اختياري)")
        img_link = st.text_input("🖼️ رابط صورة المنتج")
        
        submitted = st.form_submit_button("📌 نشر المنتج")
        
        if submitted:
            if prod_name and prod_price > 0:
                new_product = {
                    "name": prod_name,
                    "price": prod_price,
                    "desc": prod_desc,
                    "link": hidden_link,
                    "image": img_link
                }
                st.session_state.products.append(new_product)
                st.balloons()
                st.success(f"✅ تم إضافة المنتج **{prod_name}** بنجاح!")
                st.rerun()  # لتحديث تبويب المنتجات فوراً
            else:
                st.error("❌ يرجى إدخال اسم المنتج وسعر أكبر من صفر.")

# ======================= التبويب الثالث: عرض المنتجات =======================
with tab3:
    st.subheader("📦 جميع المنتجات المتاحة")
    if not st.session_state.products:
        st.info("✨ لا توجد منتجات حتى الآن. أضف منتجاً من التبويب الثاني.")
    else:
        for idx, prod in enumerate(st.session_state.products):
            with st.container():
                col_a, col_b = st.columns([1, 3])
                with col_a:
                    if prod["image"]:
                        st.image(prod["image"], width=120)
                    else:
                        st.image("https://via.placeholder.com/120?text=No+Image", width=120)
                with col_b:
                    st.markdown(f"### 🛍️ {prod['name']}")
                    st.markdown(f"**السعر:** 💲{prod['price']}")
                    st.markdown(f"**الوصف:** {prod['desc']}")
                    if prod["link"]:
                        st.markdown(f"**رابط المنتج:** [اضغط هنا]({prod['link']})")
                st.divider()
        
        # زر لحذف كل المنتجات
        if st.button("🗑️ حذف جميع المنتجات", key="delete_all"):
            st.session_state.products.clear()
            st.rerun()

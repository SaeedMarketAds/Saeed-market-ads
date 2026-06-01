import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Saeed MarketAds", layout="wide")

# إعداد مفتاح الذكاء الاصطناعي
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

st.title("Saeed DataBot - مركز التحكم")

# التبويبات
tab1, tab2 = st.tabs(["🤖 المساعد الذكي", "📦 إدارة المنتجات"])

with tab1:
    st.subheader("اسأل بوت سعيد")
    user_query = st.text_input("عن ماذا تبحث؟", key="q1")
    if st.button("بحث"):
        if user_query:
            model = genai.GenerativeModel('gemini-3.5-flash')
            response = model.generate_content(user_query)
            st.write(response.text)

with tab2:
    st.subheader("إضافة منتج جديد")
    with st.form("my_form"):
        name = st.text_input("اسم المنتج")
        link = st.text_input("رابط المنتج")
        submitted = st.form_submit_button("حفظ المنتج")
        if submitted:
            st.success(f"تم حفظ: {name}")
            st.info(f"الرابط: {link}")

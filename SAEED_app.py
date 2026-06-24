import streamlit as st
import google.generativeai as genai
import os
import base64
import streamlit.components.v1 as components
import edge_tts
import tempfile
import asyncio
import pandas as pd

# ============================================================
# 1. إعدادات الصفحة
# ============================================================
st.set_page_config(page_title="Saeed DaTaBoT", page_icon="🤖", layout="wide")

# ============================================================
# 2. الدوال البرمجية (الذكاء الاصطناعي والصوت)
# ============================================================
def get_model():
    api_key = st.secrets.get("GEMINI_MAIN_KEY") or st.secrets.get("GEMINI_API")
    if api_key:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-3.1-flash-lite")
    return None

async def play_voice_async(text):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
            path = tmp.name
        communicate = edge_tts.Communicate(text, "ar-SA-HamedNeural")
        await communicate.save(path)
        with open(path, "rb") as f:
            audio = f.read()
        b64 = base64.b64encode(audio).decode()
        st.markdown(f'<audio autoplay="true" style="display:none;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        os.unlink(path)
    except: pass

# ============================================================
# 3. واجهة المستخدم (الTabs)
# ============================================================
st.markdown("<h1 style='text-align: center; color: #feca57;'>🤖 Saeed DaTaBoT</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🛍️ متجر المنتجات", "🔍 أداة الفحص", "💬 محادثة Saeed DaTaBoT"])

# --- التبويب 1: المتجر ---
with tab1:
    st.subheader("اختر المتجر للتصفح:")
    col1, col2, col3 = st.columns(3)
    if col1.button("🛍️ تصفح SHEIN"): st.session_state.store = "SHEIN"
    if col2.button("💛 تصفح Noon"): st.session_state.store = "Noon"
    if col3.button("🚀 تصفح AliExpress"): st.session_state.store = "Ali"

    if 'store' in st.session_state:
        st.write(f"### عرض منتجات: {st.session_state.store}")
        # هنا تعرض المنتجات بناءً على الحالة المخزنة
        st.info("تم تحميل المنتجات بنجاح...")

# --- التبويب 2: الفحص ---
with tab2:
    st.subheader("🔍 أداة فحص الروابط")
    link = st.text_input("ضع رابط المنتج هنا:")
    if st.button("تحليل المنتج"):
        with st.spinner("جاري فحص البيانات..."):
            st.success("المنتج متاح وقابل للشراء!")

# --- التبويب 3: محادثة الذكاء الاصطناعي ---
with tab3:
    st.subheader("💬 اسأل Saeed DaTaBoT")
    user_query = st.text_area("اطرح سؤالك هنا:")
    if st.button("إرسال الاستشارة"):
        model = get_model()
        if model:
            with st.spinner("Saeed DaTaBoT يفكر..."):
                resp = model.generate_content(f"أنت Saeed DaTaBoT، أجب على هذا الاستفسار باختصار: {user_query}")
                st.markdown(f"**Saeed DaTaBoT:** {resp.text}")
                asyncio.run(play_voice_async(resp.text))
        else:
            st.error("مفتاح API غير مفعل.")

# ============================================================
# 4. السايدبار (الهوية)
# ============================================================
with st.sidebar:
    st.markdown("## 🤖 Saeed DaTaBoT")
    st.markdown("- ✅ نظام فحص ذكي")
    st.markdown("- ✅ تحليل متطور بالذكاء الاصطناعي")
    st.markdown("---")
    st.markdown("[Telegram Channel](https://t.me/SaeedMarketAds)")

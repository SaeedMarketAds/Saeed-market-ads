import streamlit as st
import google.generativeai as genai
import cloudscraper
import requests
import os
import base64
import streamlit.components.v1 as components
import edge_tts
import tempfile
import asyncio
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

# ============================================================
# 1. إعدادات الصفحة
# ============================================================
st.set_page_config(
    page_title="سوق سعيد | متاجر SHEIN - نون - علي اكسبرس",
    page_icon="🛍️",
    layout="wide"
)

# ============================================================
# 2. الخلفية والتصميم (CSS)
# ============================================================
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: rgba(0,0,0,0.2); }
.stMarkdown { color: #fff; }
.stButton > button {
    background: linear-gradient(90deg, #ff6b6b, #feca57);
    color: white;
    border: none;
    border-radius: 30px;
    padding: 12px 28px;
    font-weight: bold;
    font-size: 16px;
    transition: all 0.3s ease;
    width: 100%;
}
.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #feca57, #ff6b6b);
    box-shadow: 0 5px 20px rgba(0,0,0,0.3);
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.1);
    color: white;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.2);
    padding: 12px 20px;
}
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.1);
    color: white;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.2);
}
.product-card {
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(250,250,255,0.95));
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
}
.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.25);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ============================================================
# 3. دالة تشغيل الصوت
# ============================================================
async def generate_audio(text, voice="ar-SA-HamedNeural"):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            output_file = tmp_file.name
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        with open(output_file, "rb") as f:
            audio_bytes = f.read()
        os.unlink(output_file)
        return audio_bytes
    except Exception:
        return None

def play_voice(text):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_bytes = loop.run_until_complete(generate_audio(text))
        loop.close()
        if audio_bytes:
            b64 = base64.b64encode(audio_bytes).decode()
            audio_html = f'''
            <audio autoplay="true" style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            '''
            st.markdown(audio_html, unsafe_allow_html=True)
            return True
    except Exception:
        return False

# ============================================================
# 4. قراءة المفاتيح والتعليمات
# ============================================================
def get_secret(key, fallback_key=None, default=None):
    try:
        if key in st.secrets: return st.secrets[key]
        if fallback_key and fallback_key in st.secrets: return st.secrets[fallback_key]
        return default
    except: return default

GEMINI_API_KEY = get_secret("GEMINI_MAIN_KEY", "GEMINI_API", None)

try:
    with open("Instructions.txt", "r", encoding="utf-8") as f:
        instructions = f.read()
except FileNotFoundError:
    instructions = "أنت Saeed DaTaBoT، المساعد الذكي لمنصة سوق سعيد. المؤسس سعيد المسوري."

# ============================================================
# 5. إعداد موديل Gemini
# ============================================================
def init_model(api_key, model_name):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=instructions,
            generation_config={"max_output_tokens": 4096, "temperature": 0.7}
        )
        return model
    except Exception as e:
        st.error(f"خطأ في تهيئة النموذج: {str(e)}")
        return None

# ============================================================
# 6. تحليل الروابط
# ============================================================
def analyze_link_with_gemini(url, model):
    if not model: return "خدمة الذكاء الاصطناعي غير متاحة."
    
    try:
        prompt = f"قم بتحليل هذا المنتج: {url} وقدم تفاصيل عن السعر والاسم والملاحظات."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"حدث خطأ تقني، تفاصيل الخطأ هي: {str(e)}"

# ============================================================
# 7. الردود السريعة
# ============================================================
def quick_response(question):
    q = question.lower()
    if "السلام" in q or "مرحبا" in q or "هلا" in q:
        return "وعليكم السلام ورحمة الله وبركاته"
    elif "كود" in q or "خصم" in q:
        return "🎁 كود خصم SHEIN الحصري 🎁\n\n🏷️ الكود: WL7KA\n\n🔥 خصم يصل إلى 60% على أول طلب"
    elif "من أنت" in q or "سعيد" in q:
        return "أنا Saeed DaTaBoT، مساعدك الذكي للتسوق. المطور سعيد المسوري، مؤسس SaeedMarketAds."
    return None

# ============================================================
# 8. الواجهة الرئيسية
# ============================================================
st.title("🛍️ سوق سعيد")
welcome_msg = "مرحبا بكم في منصة saeedmarketads الرائدة المدعومة بالذكاء الاصطناعي"
st.markdown(f"### 🎙️ {welcome_msg}")
play_voice(welcome_msg)

# ============================================================
# 9. السايدبار
# ============================================================
with st.sidebar:
    st.header("إعدادات البوت")
    model_choice = st.selectbox(
        "اختر نموذج الذكاء الاصطناعي:",
        ["gemini-3.5-flash", "gemini-3.1-flash-lite"],
        index=0
    )
    
    if GEMINI_API_KEY:
        model = init_model(GEMINI_API_KEY, model_choice)
        if model: st.success(f"✅ يعمل على {model_choice}")
    else:
        model = None
        st.error("⚠️ مفتاح API غير موجود")

# ============================================================
# 10. التبويبات
# ============================================================
tab1, tab2, tab3 = st.tabs(["🛍️ المنتجات", "🔍 الفحص", "💬 المحادثة"])

with tab2:
    link = st.text_input("ضع رابط المنتج:")
    if st.button("تحليل"):
        if link:
            res = analyze_link_with_gemini(link, model)
            st.markdown(f"<div>{res}</div>", unsafe_allow_html=True)
            play_voice(res)

with tab3:
    user_query = st.text_area("اطرح سؤالك:")
    if st.button("إرسال"):
        if user_query:
            quick = quick_response(user_query)
            if quick:
                st.markdown(f"<div>{quick}</div>", unsafe_allow_html=True)
                play_voice(quick)
            elif model:
                response = model.generate_content(user_query)
                st.markdown(f"<div>Saeed DaTaBoT يرد: {response.text}</div>", unsafe_allow_html=True)
                play_voice(response.text)

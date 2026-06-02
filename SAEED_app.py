import streamlit as st
import os
import google.generativeai as genai
from gtts import gTTS
import tempfile
import time
from io import BytesIO
import base64

# إعداد الصفحة
st.set_page_config(page_title="Saeed MarketAds - بالصوت والصورة", layout="wide")

# ======================= تهيئة حالة الجلسة =======================
if "products" not in st.session_state:
    st.session_state.products = []
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "current_avatar" not in st.session_state:
    st.session_state.current_avatar = "saeed.jpg" if os.path.exists("saeed.jpg") else "ROBOT.jpg"
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True
if "use_recorded_voice" not in st.session_state:
    st.session_state.use_recorded_voice = False
if "recorded_voice_path" not in st.session_state:
    st.session_state.recorded_voice_path = None

# ======================= دالة الإعداد الذكي لـ Gemini =======================
def setup_gemini():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.sidebar.error("❌ مفتاح API غير موجود، أضفه في secrets")
        return None
    genai.configure(api_key=api_key)
    
    # قائمة النماذج المحدثة للبحث التلقائي
    models_to_try = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-3.5-pro']
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            model.generate_content("test") # اختبار اتصال سريع
            st.sidebar.success(f"✅ متصل بـ: {model_name}")
            return model
        except Exception:
            continue
    st.sidebar.error("❌ تعذر الاتصال بجميع النماذج، تأكد من مفتاح API")
    return None

gemini_model = setup_gemini()

# ======================= دوال الصوت =======================
def text_to_speech_tts(text, lang='ar'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        return None

def animate_avatar(image_path):
    if not os.path.exists(image_path): return
    placeholder = st.empty()
    for i in range(3):
        placeholder.image(image_path, width=180, caption="🗣️ يتحدث...")
        time.sleep(0.1)
        placeholder.image(image_path, width=170, caption=" ")
        time.sleep(0.1)
    placeholder.image(image_path, width=180, caption="سعيد")

# ======================= الواجهة الرئيسية =======================
st.title("🎭 Saeed Talking Avatar - بالصوت والشفاه")

with st.sidebar:
    st.header("⚙️ إعدادات الأفاتار والصوت")
    avatar_option = st.selectbox("اختر الأفاتار", ["سعيد (saeed.jpg)", "روبوت (ROBOT.jpg)"])
    st.session_state.current_avatar = "saeed.jpg" if avatar_option == "سعيد (saeed.jpg)" else "ROBOT.jpg"
    
    st.session_state.voice_enabled = st.checkbox("🔊 تفعيل الصوت", value=True)
    st.info("جميع الحقوق محفوظة SaeedMarketAds ©")

tab1, tab2, tab3 = st.tabs(["💬 تكلم مع سعيد", "➕ إضافة منتج", "📦 قائمة المنتجات"])

with tab1:
    col_img, col_chat = st.columns([1, 2])
    with col_img:
        if os.path.exists(st.session_state.current_avatar):
            st.image(st.session_state.current_avatar, width=200)
    
    with col_chat:
        user_question = st.chat_input("اكتب سؤالك هنا...")
        if user_question:
            st.session_state.conversation.append({"role": "user", "content": user_question})
            
            if gemini_model:
                response = gemini_model.generate_content(user_question)
                ai_reply = response.text
            else:
                ai_reply = "النموذج غير متاح حالياً."
            
            st.session_state.conversation.append({"role": "assistant", "content": ai_reply})
            
            if st.session_state.voice_enabled:
                animate_avatar(st.session_state.current_avatar)
                audio_file = text_to_speech_tts(ai_reply)
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
                    os.unlink(audio_file)
            st.rerun()

# باقي الكود كما هو (التبويبات 2 و 3) ...


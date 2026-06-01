import streamlit as st
import os
import google.generativeai as genai
from gtts import gTTS
import tempfile
from io import BytesIO
# ملاحظة مهمة: هذا الكود لا يتضمن Wav2Lip حاليًا ولكنه جاهز لك
# لإضافة دعم Wav2Lip، ستحتاج إلى استيراده وكتابة دالة لدمج الصوت والصورة

# إعدادات الصفحة
st.set_page_config(page_title="Saeed DataBot", layout="wide")

# تهيئة حالة الجلسة
if "products" not in st.session_state:
    st.session_state.products = []
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# تهيئة نموذج Gemini
def setup_gemini_model():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    model_names = ['models/gemini-1.5-flash', 'gemini-3.5-flash']
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            model.generate_content("test")
            return model
        except Exception:
            continue
    return None

model = setup_gemini_model()
if not model:
    st.warning("⚠️ لم يتم العثور على مفتاح API أو النموذج، الرجاء مراجعة الإعدادات.")

# دالة تحويل النص لصوت باستخدام gTTS
def text_to_speech(text, lang='ar'):
    try:
        # إنشاء كائن gTTS (يدعم العربية بامتياز)
        tts = gTTS(text=text, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحويل النص لصوت: {e}")
        return None

# واجهات التطبيق الأساسية
st.title("🎭 سعيد توكينج أفatar - Saeed Talking Avatar")
tab1, tab2, tab3 = st.tabs(["💬 تكلم مع سعيد", "➕ أضف منتجًا", "🛒 كل المنتجات"])

# تبويب المحادثة
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.image("saeed.jpg" if os.path.exists("saeed.jpg") else "ROBOT.jpg", width=200)
    with col2:
        st.markdown("### 🧠 أهلاً بك! أنا سعيد الذكي.")
        st.markdown("يمكنني مساعدتك بأي شيء، فقط اسألني.")
        avatar_img = st.file_uploader("🖼️ حمّل صورة وجهك (اختياري)", type=["jpg", "png", "jpeg"], key="avatar")
        use_voice = st.checkbox("🔊 شغّل خاصية الصوت (اختياري)", value=True)
    st.divider()
    for msg in st.session_state.conversation:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    user_input = st.chat_input("اسأل سعيد هنا...")
    if user_input:
        st.session_state.conversation.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        if model:
            try:
                response = model.generate_content(user_input)
                ai_reply = response.text
            except Exception as e:
                ai_reply = f"عذرًا، حدث خطأ: {e}"
        else:
            ai_reply = "عذرًا، مفتاح API غير صحيح أو غير موجود."
        with st.chat_message("assistant"):
            st.write(ai_reply)
        if use_voice:
            with st.spinner("⏳ جاري تحويل الرد إلى صوت..."):
                audio_file = text_to_speech(ai_reply, lang='ar')
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
                    os.unlink(audio_file)
        st.session_state.conversation.append({"role": "assistant", "content": ai_reply})
        st.rerun()

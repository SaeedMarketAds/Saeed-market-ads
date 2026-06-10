import json
import streamlit as st
from streamlit_chat import message
import gtts
from io import BytesIO
import base64

# تحميل الإعدادات
with open("saeed_databot_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

BOT_NAME = config["bot_name"]
OWNER_NAME = config["owner_name"]

def get_bot_response(user_input):
    """دالة ردود البوت (تم إزالة كلمة SHEIN من الترحيبة)"""
    user_input_lower = user_input.lower().strip()
    
    # 1. الرد على التحية (السلام) - بدون SHEIN
    greetings = ["سلام", "مرحباً", "اهلا", "السلام", "مرحبا", "هلا"]
    if any(word in user_input_lower for word in greetings):
        return "وعليكم السلام ورحمة الله وبركاته، كيف أخدمك اليوم؟"
    
    # 2. الرد على سؤال عن SHEIN
    if "shein" in user_input_lower:
        return "عالم الموضة والأزياء بين يديك. وجهتك للأسعار التنافسية. خيارك السريع للأناقة!"
    
    # 3. الرد على AliExpress أو Noon
    if any(market in user_input_lower for market in ["aliexpress", "noon"]):
        return "أنا هنا لمساعدتك في AliExpress، Noon، أو SHEIN. ما هو طلبك بالضبط؟"
    
    # 4. الرد على السعر والميزانية
    if "ميزانيتك" in user_input or "سعر" in user_input or "$" in user_input:
        return f"فهمت ميزانيتك. {BOT_NAME} سيساعدك في إيجاد أفضل العروض من AliExpress، Noon، و SHEIN."
    
    # 5. الرد العام
    return f"كيف يمكنني مساعدتك اليوم؟ يمكنني مساعدتك في شراء هاتف، أو إيجاد عروض في Noon أو AliExpress أو SHEIN."

def text_to_speech(text):
    """تحويل النص إلى صوت"""
    try:
        tts = gtts.gTTS(text, lang="ar")
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        audio_base64 = base64.b64encode(audio_bytes.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    except:
        return ""

# ========== واجهة Streamlit ==========
st.set_page_config(page_title=BOT_NAME, page_icon="🤖")

# عرض الفيديو كأفتار متحرك (بدلاً من الصورة الثابتة)
st.markdown("""
    <style>
        .stVideo {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# محاولة عرض الفيديو
try:
    with open("saeed_avatar_v1.mp4", "rb") as video_file:
        video_bytes = video_file.read()
    st.video(video_bytes, format="video/mp4")
    st.caption(f"🎙️ {BOT_NAME} - بوت التسوق الذكي")
except FileNotFoundError:
    st.warning("⚠️ الفيديو saeed_avatar_v1.mp4 غير موجود، يرجى رفعه إلى مجلد المشروع")
    # عرض اسم البوت كبديل
    st.title(f"🤖 {BOT_NAME}")

st.title(f"🤖 {BOT_NAME}")
st.caption(f"بوت التسوق الذكي - صنع بواسطة {OWNER_NAME}")

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for msg in st.session_state.messages:
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=msg["key"])
    else:
        message(msg["content"], is_user=False, key=msg["key"])

# مربع إدخال المستخدم
user_input = st.chat_input("اكتب رسالتك هنا...")

if user_input:
    # إضافة رسالة المستخدم
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "key": f"user_{len(st.session_state.messages)}"
    })
    message(user_input, is_user=True)
    
    # الحصول على رد البوت
    response = get_bot_response(user_input)
    
    # إضافة رد البوت
    st.session_state.messages.append({
        "role": "bot",
        "content": response,
        "key": f"bot_{len(st.session_state.messages)}"
    })
    message(response, is_user=False)
    
    # تشغيل الصوت إذا كان مفعلاً
    if config.get("voice_enabled", False):
        audio_html = text_to_speech(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)

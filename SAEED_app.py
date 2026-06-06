import json
import streamlit as st
from streamlit_chat import message
import gtts
from io import BytesIO
import base64
import random

# ========== الإعدادات ==========
BOT_NAME = "Saeed DataBot"  # ✅ الاسم بالإنجليزي
OWNER_NAME = "Saeed Almasoori"

# إعدادات الصوت
VOICE_ENABLED = True

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

def get_bot_response(user_input):
    """دالة ردود البوت الذكية"""
    user_input_lower = user_input.lower().strip()
    
    # 1. الرد على التحية (السلام) - الأولوية القصوى
    greetings = ["سلام", "مرحباً", "اهلا", "السلام", "مرحبا", "هلا", "السلام عليكم", "السالم"]
    for word in greetings:
        if word in user_input_lower:
            return "وعليكم السلام ورحمة الله وبركاته، SHEIN موجود لخدمتك! كيف أقدم المساعدة؟"
    
    # 2. الرد على SHEIN
    if "shein" in user_input_lower:
        return "🌟 SHEIN: عالم الموضة والأزياء بين يديك! أسعار تنافسية وتوصيل سريع. هل تريد البحث عن منتج معين؟"
    
    # 3. البحث عن هاتف (سامسونج، نوت، جالكسي، iPhone)
    phones = ["هاتف", "سامسونج", "iphone", "نوت", "note", "جالكسي", "galaxy", "موبايل"]
    if any(word in user_input_lower for word in phones):
        if "نوت" in user_input_lower or "note" in user_input_lower:
            return "📱 Samsung Galaxy Note 10+ متوفر على SHEIN وAliExpress وNoon. سعره يبدأ من $250. هل تريد مساعدة في الشراء؟"
        elif "سامسونج" in user_input_lower or "galaxy" in user_input_lower:
            return "📱 سامسونج جالكسي متوفر الآن! قارن الأسعار بين SHEIN وAliExpress وNoon. ما موديلك المفضل؟"
        else:
            return "📱 أبحث عن هاتف؟ سأبحث لك أفضل العروض من SHEIN وAliExpress وNoon. ما هي ميزانيتك؟"
    
    # 4. سؤال عن السعر والميزانية
    if any(word in user_input_lower for word in ["سعر", "$", "دولار", "ميزانية", "كم"]):
        return f"💰 فهمت ميزانيتك. {BOT_NAME} سيبحث لك أفضل العروض من SHEIN وAliExpress وNoon."
    
    # 5. سؤال "من انت" أو "who are you"
    if any(word in user_input_lower for word in ["من انت", "who are you", "من أنت"]):
        return f"🤖 أنا {BOT_NAME}، مساعدك الذكي للتسوق من SHEIN، AliExpress، وNoon. صنعني {OWNER_NAME}!"
    
    # 6. رد افتراضي ذكي
    return f"🛒 كيف يمكنني مساعدتك اليوم؟\n✅ اكتب 'SHEIN' لعروض الموضة\n✅ اكتب 'هاتف' لشراء هاتف\n✅ اكتب 'سلام' للتحية"

# ========== واجهة Streamlit ==========
st.set_page_config(page_title=BOT_NAME, page_icon="🤖", layout="centered")

# محاولة عرض الصورة (جرب أسماء مختلفة)
image_found = False
for img_name in ["ROBO.T.jpg", "ROBOT.jpg", "robot.jpg", "ROBO-T.jpg"]:
    try:
        st.image(img_name, caption=BOT_NAME, width=120)
        image_found = True
        break
    except:
        pass

if not image_found:
    st.info(f"🤖 {BOT_NAME} - مساعدك الذكي للتسوق")

# العنوان
st.title(f"🤖 {BOT_NAME}")
st.caption(f"🛍️ Smart Shopping Assistant - Built by {OWNER_NAME}")

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = f"Welcome! I'm {BOT_NAME}. How can I help you today? Looking for SHEIN fashion? Or a new phone?"
    st.session_state.messages.append({
        "role": "bot",
        "content": welcome_msg,
        "key": "welcome"
    })

# عرض المحادثة
for msg in st.session_state.messages:
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=msg["key"])
    else:
        message(msg["content"], is_user=False, key=msg["key"])

# مربع الإدخال
user_input = st.chat_input("✍️ Type your message here...")

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
    
    # تشغيل الصوت
    if VOICE_ENABLED:
        audio_html = text_to_speech(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
    
    st.rerun()

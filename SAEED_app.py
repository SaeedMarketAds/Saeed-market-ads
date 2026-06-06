hereimport json
import streamlit as st
from streamlit_chat import message
import gtts
from io import BytesIO
import base64
import random

# تحميل الإعدادات
with open("saeed_databot_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

BOT_NAME = config["bot_name"]
OWNER_NAME = config["owner_name"]

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
    """دالة ردود البوت الذكية - تفهم SHEIN والسلام والمنتجات"""
    user_input_lower = user_input.lower().strip()
    
    # 1. الرد على التحية (السلام)
    greetings = ["سلام", "مرحباً", "اهلا", "السلام", "مرحبا", "هلا", "السلام عليكم"]
    if any(word in user_input_lower for word in greetings):
        responses = [
            "وعليكم السلام ورحمة الله وبركاته، SHEIN موجود لخدمتك! كيف أقدم المساعدة؟",
            "السلام عليكم! أنا Saeed DataBot، شريكك للتسوق من SHEIN وAliExpress وNoon.",
            "وعليكم السلام! SHEIN عندي أفضل العروض للموضة والأزياء."
        ]
        return random.choice(responses)
    
    # 2. الرد على سؤال عن SHEIN (الأهم)
    if "shein" in user_input_lower:
        responses = [
            "🌟 SHEIN: عالم الموضة والأزياء بين يديك! أسعار تنافسية وتوصيل سريع. هل تريد البحث عن منتج معين؟",
            "👗 SHEIN هو وجهتك الأولى للموضة! فساتين، أحذية، إكسسوارات - خصومات تصل إلى 70%",
            "🛍️ SHEIN متوفر الآن! أخبرني ما تبحث عنه: ملابس، أحذية، أو إكسسوارات؟"
        ]
        return random.choice(responses)
    
    # 3. البحث عن هاتف
    if any(word in user_input_lower for word in ["هاتف", "سامسونج", "iphone", "نوت", "note", "جالكسي", "galaxy"]):
        phone_models = {
            "note": "Samsung Galaxy Note 10+",
            "سامسونج": "Samsung Galaxy",
            "iphone": "iPhone"
        }
        for key, model in phone_models.items():
            if key in user_input_lower:
                return f"📱 {model} متوفر على SHEIN وAliExpress وNoon. سعره يبدأ من $250. هل تريد مقارنة الأسعار؟"
        return "📱 أبحث عن هاتف؟ سأبحث لك أفضل العروض من SHEIN وAliExpress وNoon. ما هي ميزانيتك؟"
    
    # 4. سؤال عن السعر والميزانية
    if any(word in user_input_lower for word in ["سعر", "$", "دولار", "ميزانية", "كم"]):
        return f"💰 فهمت ميزانيتك. {BOT_NAME} سيبحث لك أفضل العروض من SHEIN (للموضة) وAliExpress (للإلكترونيات) وNoon (للجميع)."
    
    # 5. سؤال "من انت" أو "who are you"
    if any(word in user_input_lower for word in ["من انت", "who are you", "من أنت"]):
        return f"🤖 أنا {BOT_NAME}، مساعدك الذكي للتسوق من SHEIN، AliExpress، وNoon. صنعني {OWNER_NAME} لمساعدتك في إيجاد أفضل العروض!"
    
    # 6. أي سؤال عام
    return f"🛒 كيف يمكنني مساعدتك اليوم؟ يمكنني: \n✅ البحث في SHEIN عن الملابس والأزياء\n✅ مقارنة أسعار الهواتف في AliExpress\n✅ إيجاد عروض Noon\n✅ الرد على استفساراتك عن المنتجات"

# ========== واجهة Streamlit ==========
st.set_page_config(page_title=BOT_NAME, page_icon="🤖", layout="centered")

# محاولة عرض الصورة
try:
    st.image("ROBO.T.jpg", caption=BOT_NAME, width=120)
except:
    st.warning("⚠️ الصورة ROBO.T.jpg غير موجودة - تأكد من وجودها في مجلد المشروع")

# العنوان
st.title(f"🤖 {BOT_NAME}")
st.caption(f"🛍️ مساعدك الذكي للتسوق العالمي - صنع بواسطة {OWNER_NAME}")

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []
    # رسالة ترحيب أولية
    welcome_msg = f"أهلاً بك! أنا {BOT_NAME}. كيف أخدمك اليوم؟ أبحث عن عروض SHEIN؟ أو تريد شراء هاتف؟"
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
user_input = st.chat_input("✍️ اكتب رسالتك هنا...")

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
    if config.get("voice_enabled", True):
        audio_html = text_to_speech(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
    
    # تحديث الصفحة لعرض الصوت
    st.rerun()

import streamlit as st
from google import genai
import gtts  # مكتبة تحويل النص إلى صوت (تأكد من إضافتها في requirements.txt)
import os

# 1. تهيئة إعدادات الصفحة وعرض الهوية البصرية للبوت
st.set_page_config(page_title="Saeed DataBot", page_icon="🚀")

# عرض صورتك الرقمية (الأفاتار) في أعلى المحادثة
st.image("saeed_avatar.jpg", use_column_width=True)
st.title("إمبراطورية سعيد ماركت | الروبوت الذكي")
st.write("مرحباً بك! أنا مساعدك الذكي للتسويق الرقمي وإدارة الإعلانات.")

# تشغيل ملف الصوت الترحيبي تلقائياً لمن يدخل الموقع
st.audio("saeed_voice.mp3")

# 2. إدخال مفتاح الـ API الخاص بجوجل بشكل آمن من السيكرتس
try:
    YOUR_API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=YOUR_API_KEY)
except Exception as e:
    st.error("تأكد من إعداد مفتاح GEMINI_API_KEY في Streamlit Secrets بالشكل الصحيح.")

# 3. إنشاء ذاكرة للمحادثة لكي يتذكر البوت الكلام السابق
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة في الشاشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"])

# ميزة المايكروفون (ليسمعك البوت إذا أردت التسجيل بصوتك بدلاً من الكتابة)
audio_value = st.audio_input("اضغط على المايك وتحدث مع البوت بصوتك 🎙️")
user_input = st.chat_input("أو اكتب رسالتك للبوت هنا...")

# إذا تحدث المستخدم بالصوت (هنا تحتاج كود تحويل الصوت لنص، لكن لتسهيل الأمر حالياً سنعتمد على النص والرد الصوتي)
if audio_value:
    st.info("تم استقبال تسجيلك الصوتي بنجاح! جاري المعالجة...")
    # يمكنك لاحقاً ربط مكتبة تحويل الصوت إلى نص هنا

# 4. استقبال رسائل المستخدم النصية والرد عليها بالصوت والنص
if user_input:
    # عرض رسالة المستخدم
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # توجيه الرسالة للذكاء الاصطناعي للحصول على الرد
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # تعليمات خاصة بالبوت لكي يعرف هويته (System Instruction)
            prompt_instructions = (
                f"أنت بوت ذكي وصوتي لبراند 'saeedmarketads' المتخصص في التسويق الإلكتروني وإعلانات المتاجر مثل AliExpress و Noon و SHEIN. "
                f"تحدث بذكاء، وود، واحترافية باللغة العربية واجعل إجابتك مختصرة ومناسبة للقراءة الصوتية. رسالة المستخدم هي: {user_input}"
            )
            
            # استدعاء نموذج Gemini
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_instructions
            )
            
            bot_reply = response.text
            message_placeholder.markdown(bot_reply)
            
            # توليد رد صوتي للبوت لكي ينطق الكلام (يتكلم معك)
            tts = gtts.gTTS(text=bot_reply, lang='ar')
            audio_file = "bot_reply.mp3"
            tts.save(audio_file)
            
            # تشغيل الرد الصوتي للمستخدم
            st.audio(audio_file)
            
            # حفظ الرسالة والرد الصوتي في الذاكرة
            st.session_state.messages.append({"role": "assistant", "content": bot_reply, "audio": audio_file})
            
        except Exception as e:
            message_placeholder.markdown("عذراً، واجهت مشكلة في الرد السريع.")

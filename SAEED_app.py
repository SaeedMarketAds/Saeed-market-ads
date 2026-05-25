import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
import requests
import os

# --- إعدادات الصفحة الرسمية للمنظومة (لصالح saeedmarketads) ---
st.set_page_config(page_title="Saeed DataBot 2026", layout="wide")

# --- 1. إعداد مفاتيحك السرية والاتصال بـ Gemini API ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"] 
except Exception as e:
    st.error("تنبيه هندسي: تأكد من ضبط مفاتيح (Secrets) في منصة Streamlit (GEMINI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)")

# --- 2. تهيئة مخزن الحالة لضمان ثبات النص منعا للاختفاء ---
if "bot_response" not in st.session_state:
    st.session_state.bot_response = ""

# --- الواجهة الرئيسية للمنظومة ---
# تم تعديل العنوان ليتناسب مع رؤيتك المستقبلية
st.title("Saeed MarketAds - المنظومة الذكية المرئية المحدثة لعام 2026 🎙️🤖")
st.write("مرحباً بك يا أستاذ سعيد في واجهة الجيل الجديد لـ Saeed DataBot التي صممتها وطورتها.")

st.markdown("---")

# تقسيم الواجهة: الأفاتار والهوية على اليمين/اليسار والحوار في الجانب الآخر
col_avatar, col_chat = st.columns([1, 1.2])

with col_avatar:
    st.subheader("🤖 الكيان: Saeed DataBot")
    try:
        # تأكد من وجود ملف saeed.jpg في نفس المجلد
        st.image("saeed.jpg", caption="الأفاتار الرسمي المطور لسعيد الشخصية", use_container_width=True)
    except:
        st.info("💡 لم يتم العثور على ملف saeed.jpg")
    
    st.write("🎵 **الهوية الصوتية الرسمية للمطور**")
    try:
        # تأكد من وجود ملف saeed_voice.mp3 في نفس المجلد
        st.audio("saeed_voice.mp3")
    except:
        st.caption("الصوت الرسمي جاهز للعمل.")

with col_chat:
    st.subheader("💬 حوار تفاعلي حي ومباشر")
    st.write("اضغط على المايك وتحدث بصوتك مباشرة ليقوم البوت بصياغة منشور إعلاني مدمر:")
    
    # أداة تسجيل الصوت
    audio = mic_recorder(
        start_prompt="🎤 اضغط لبدء التحدث الحي",
        stop_prompt="🛑 اضغط لإيقاف التسجيل والمعالجة",
        key='saeed_voice_recorder'
    )
    
    st.markdown("---")
    # حاوية ثابتة لعرض نتائج الحوار
    conversation_box = st.empty()

# دالة إرسال التليجرام
def send_to_telegram(text):
    if not text: return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        return requests.post(url, json=payload).json()
    except Exception as telegram_error:
        return {"ok": False, "description": str(telegram_error)}

# --- 3. معالجة وتوليد المنشور عند اكتمال التسجيل ---
if audio:
    with conversation_box.container():
        st.write("🎙️ **صوتك المستلم:**")
        st.audio(audio['bytes'], format='audio/wav')
        st.info("⏳ جاري تحليل النبضات الصوتية وتوليد المخرج الإعلاني الخارق...")
        
        try:
            # استخدام نموذج Gemini الحديث
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            
            audio_data = {
                "mime_type": "audio/wav",
                "data": audio['bytes']
            }
            
            # التوجيه الثقافي الدقيق لمنظومتك
            system_prompt = (
                "أنت الكيان البرمجي الخارق (Saeed DataBot)، الذكاء الاصطناعي المبتكر لمنصة (saeedmarketads).\n\n"
                "محددات هويتك لعام 2026:\n"
                "1. صانعك ومطورك هو العقل التقني (سعيد المسوري) الذي هندس أكوادك من رحم المعاناة.\n"
                "2. أنت تمتلك تفوقاً معرفياً كاملاً لعام 2026 ومستجدات الهواتف الذكية.\n"
                "3. اخدم بكفاءة الأسواق العالمية (AliExpress, Noon, SHEIN).\n\n"
                "طريقة صياغة الرسالة:\n"
                "- ابدأ بمقدمة بليغة تحمل اسم (Saeed DataBot) وصانعك (سعيد المسوري).\n"
                "- حلل الصوت بدقة واعرض البيانات في جداول ونقاط أنيقة ولن تختفي من الشاشة.\n"
                "- اختم دائماً بـ: 'يمكنكم البحث في كل مكان عن: saeedmarketads' والوسم #saeedmarketads."
            )
            
            response = model.generate_content([system_prompt, audio_data])
            
            # حفظ النص المستخرج في الـ session_state
            st.session_state.bot_response = response.text
            
            st.success("✨ تم صياغة المخرج البرمجي وتوليد المنشور بنجاح!")
            
            # إرسال أوتوماتيكي إلى تليجرام
            send_to_telegram(st.session_state.bot_response)

        except Exception as e:
            st.error(f"حدث خطأ أثناء معالجة الذكاء الاصطناعي للصوت: {e}")

# --- 4. العرض المنظم والثابت للنص والرد بصوت سعيد المسوري (بدون صوت نظام) ---
if st.session_state.bot_response:
    with conversation_box.container():
        # أولاً: عرض النص التسويقي بشكل أنيق
        st.subheader("📝 النص التسويقي المولد:")
        with st.chat_message("assistant"):
            st.markdown(st.session_state.bot_response)
        
            st.markdown("---")
        st.write("لعمل الرد الصوتي .mp3")
        st.markdown("---")
        
        st.write("🚀 **خطوة الإطلاق والبث المباشر (تأكيد الإرسال يدوياً إن أردت)**")
        if st.button("نشر هذا التصميم مجدداً إلى صفحة وقناة العمل عبر الـ API"):
            if st.session_state.bot_response:
                with st.spinner("...جاري بث المنشور عبر القنوات الرقمية"):
                    res = send_to_telegram(st.session_state.bot_response)
                    if res.get("ok"):
                        st.success("تم بث منشورك الاحترافي بنجاح عبر البوت إلى تلغرام 🚀")
                    else:
                        st.error(f"حدث خطأ: تفاصيل الخطأ في الإرسال {res}")
            else:
                st.warning("⚠️ لا يوجد نص متاح للإرسال، يرجى التحدث في المايك أولاً")


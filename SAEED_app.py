import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
import requests
from gtts import gTTS  
import os

# --- إعدادات الصفحة الرسمية للمنظومة ---
st.set_page_config(page_title="Saeed DataBot 2026", layout="wide")

# --- 1. إعداد مفاتيحك السرية والاتصال بـ Gemini API ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"] 
except Exception as e:
    st.error("تنبيه: تأكد من ضبط مفاتيح (Secrets) في منصة Streamlit (GEMINI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)")

# --- 2. تهيئة مخزن الحالة (Session State) لضمان ثبات النص والصوت ---
if "bot_response" not in st.session_state:
    st.session_state.bot_response = ""
if "generated_audio" not in st.session_state:
    st.session_state.generated_audio = None

# --- الواجهة الرئيسية للمنظومة ---
st.title("Saeed MarketAds - المنظومة الذكية المرئية المحدثة 🎙️🤖")
st.write("مرحباً بك يا أستاذ سعيد في واجهة الجيل الجديد لـ Saeed DataBot لعام 2026.")

st.markdown("---")

# تقسيم الواجهة: الأفاتار والهوية على اليمين/اليسار والحوار في الجانب الآخر
col_avatar, col_chat = st.columns([1, 1.2])

with col_avatar:
    st.subheader("🤖 الكيان: Saeed DataBot")
    try:
        st.image("saeed.jpg", caption="الأفاتار الرسمي المطور لسعيد الشخصية", use_container_width=True)
    except:
        st.info("💡 لم يتم العثور على ملف saeed.jpg، يرجى التأكد من وجوده في المستودع بنظام حروف صغيرة.")
    
    st.write("🎵 **الهوية الصوتية الرسمية للمطور**")
    try:
        st.audio("saeed_voice.mp3")
    except:
        st.caption("الصوت الرسمي جاهز للعمل.")

with col_chat:
    st.subheader("💬 حوار تفاعلي حي ومباشر")
    st.write("اضغط على المايك وتحدث بصوتك مباشرة ليقوم البوت بصياغة مراجعة أو إعلان تسويقي مدمر مع النطق الصوتي الحي:")
    
    # أداة تسجيل الصوت
    audio = mic_recorder(
        start_prompt="🎤 اضغط لبدء التحدث الحي",
        stop_prompt="🛑 اضغط لإيقاف التسجيل والمعالجة",
        key='saeed_voice_recorder'
    )
    
    # حاوية ثابتة مخصصة لعرض الحوار والنصوص لكي تبقى على الشاشة دائماً
    conversation_box = st.empty()

# --- 3. معالجة وتوليد المنشور والنطق الصوتي عند اكتمال التسجيل ---
if audio:
    with col_chat:
        st.audio(audio['bytes'], format='audio/wav')
        
        with conversation_box.container():
            st.info("⏳ جاري تحليل النبضات الصوتية وتوليد المخرج الإعلاني الخارق وتحويله لصوت عبر نموذج Gemini...")
            
            try:
                # استخدام نموذج Gemini الحديث والمعتمد في مشروعك
                model = genai.GenerativeModel(model_name="gemini-2.5-flash")
                
                audio_data = {
                    "mime_type": "audio/wav",
                    "data": audio['bytes']
                }
                
                # التوجيه الثقافي والتقني الدقيق لشخصيتك الرقمية لعام 2026
                system_prompt = (
                    "أنت الكيان البرمجي الخارق (Saeed DataBot)، الذكاء الاصطناعي المبتكر لمنصة (saeedmarketads).\n\n"
                    "محددات هويتك لعام 2026:\n"
                    "1. صانعك ومطورك هو العقل التقني (سعيد المسوري) الذي هندس أكوادك من رحم المعاناة.\n"
                    "2. هويتك الحالية هي الأفاتار الذكي المخصص الممثل لشخصية سعيد الذكية الرقمية.\n"
                    "3. أنت تمتلك تفوقاً معرفياً كاملاً لعام 2026 الحالي ومستجدات الهواتف الذكية (مثل Samsung Galaxy S26 Ultra).\n"
                    "4. اخدم بكفاءة الأسواق العالمية (AliExpress, Noon, SHEIN).\n\n"
                    "طريقة صياغة الرسالة:\n"
                    "- ابدأ بمقدمة بليغة تحمل اسم (Saeed DataBot) وصانعك (سعيد المسوري).\n"
                    "- حلل الصوت بدقة واعرض البيانات في جداول ونقاط أنيقة ولن تختفي من الشاشة.\n"
                    "- اختم دائماً بـ: 'يمكنكم البحث في كل مكان عن: saeedmarketads' والوسم #saeedmarketads."
                )
                
                response = model.generate_content([system_prompt, audio_data])
                
                # تخزين النص المستخرج في الـ session_state لمنع الاختفاء
                st.session_state.bot_response = response.text
                
                # توليد النطق الصوتي من النص المكتوب تلقائياً
                tts = gTTS(text=st.session_state.bot_response, lang='ar', slow=False)
                tts.save("bot_speech.mp3")
                
                # حفظ بايتات الصوت في الجلسة للبقاء الدائم
                with open("bot_speech.mp3", "rb") as f:
                    st.session_state.generated_audio = f.read()

                st.success("✨ تم صياغة المخرج البرمجي وتوليد النطق الصوتي بنجاح!")

            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الذكاء الاصطناعي للصوت: {e}")

# --- 4. عرض التحديثات من الجلسة بعبارات ثابتة ومستقرة ---
if st.session_state.bot_response:
    with col_chat:
        with conversation_box.container():
            st.subheader("📝 النص التسويقي المولد:")
            with st.chat_message("assistant"):
                st.markdown(st.session_state.bot_response)
            
            st.markdown("---")
            
            if st.session_state.generated_audio:
                st.subheader("🔊 النطق الصوتي للبوت (Saeed DataBot):")
                st.audio(st.session_state.generated_audio, format="audio/mp3")

    # --- 5. زر النشر المباشر والتلقائي إلى التليجرام ---
    st.write("---")
    st.write("🚀 **خطوة الإطلاق والبث المباشر:**")
    
    def send_to_telegram(text):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
        try:
            return requests.post(url, json=payload).json()
        except Exception as telegram_error:
            return {"ok": False, "description": str(telegram_error)}
        
    if st.button("نشر هذا التصميم فوراً إلى صفحة وقناة العمل عبر الـ API"):
        if st.session_state.bot_response:
            with st.spinner("جاري بث المنشور عبر القنوات الرقمية..."):
                res = send_to_telegram(st.session_state.bot_response)
                if res.get("ok"):
                    st.success("🎉 تم بث منشورك الاحترافي بنجاح مذهل عبر البوت إلى تلغرام!")
                else:
                    st.error(f"تفاصيل الخطأ في الإرسال: {res}")
        else:
            st.warning("⚠️ لا يوجد نص متاح حالياً لإرساله، يرجى التحدث في المايك أولاً.")

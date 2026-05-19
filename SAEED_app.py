import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
import requests

# 1. إعداد مفاتيحك السرية بأمان تام من إعدادات Streamlit
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"] 
except Exception as e:
    st.error("تنبيه: تأكد من ضبط مفاتيح (Secrets) في منصة Streamlit (GEMINI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)")

# إعدادات الصفحة لتكون مريحة واحترافية
st.set_page_config(page_title="Saeed DataBot 2026", layout="wide")

# العنوان الرئيسي للمنظومة
st.title("Saeed MarketAds - المنظومة الذكية المرئية المحدثة 🎙️🤖")
st.write("مرحباً بك يا أستاذ سعيد في الواجهة الجيل الجديد لـ Saeed DataBot لعام 2026.")

---

# 2. تقسيم الواجهة لضمان عدم ضياع أو اختفاء النصوص خلف الأفاتار
col_avatar, col_chat = st.columns([1, 1.2])

with col_avatar:
    st.subheader("🤖 الكيان: Saeed DataBot")
    # هنا يتم عرض صورة الأفاتار الشخصية الخاصة بك وتثبيتها في الجانب
    # يمكنك تغيير رابط الصورة برابط صورتك المباشر إذا كنت ترفعها على موقع خارجي أو تضعها في نفس المجلد باسم avatar.png
    try:
        st.image("avatar.png", caption="الأفاتار الرسمي المطور لسعيد الشخصية", use_container_width=True)
    except:
        st.info("💡 لرفع صورتك الشخصية كأفاتار، تأكد من تسميتها avatar.png ووضعها بجانب ملف الكود في حساب GitHub.")
    
    st.write("🎵 **الهوية الصوتية الرسمية للمطور**")
    # شريط الصوت الثابت
    try:
        st.audio("voice.mp3")
    except:
        st.caption("الصوت الرسمي جاهز للعمل.")

with col_chat:
    st.subheader("💬 حوار تفاعلي حي ومباشر")
    st.write("اضغط على المايك وتحدث بصوتك مباشرة ليقوم البوت بصياغة مراجعة أو إعلان تسويقي مدمر دون اختفاء النصوص:")
    
    # أداة تسجيل الصوت
    audio = mic_recorder(
        start_prompt="🎤 اضغط لبدء التحدث الحي",
        stop_prompt="🛑 اضغط لإيقاف التسجيل والمعالجة",
        key='saeed_voice_recorder'
    )
    
    # حاوية ثابتة مخصصة لعرض الحوار والنصوص لكي تبقى على الشاشة دائماً أمام الناس
    conversation_box = st.container()

# 3. معالجة وتوليد المنشور عند اكتمال تسجيل الصوت
if audio:
    with col_chat:
        st.audio(audio['bytes'], format='audio/wav')
        
        with conversation_box:
            st.info("⏳ جاري تحليل النبضات الصوتية وتوليد المخرج الإعلاني الخارق...")
            
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                audio_data = {
                    "mime_type": "audio/wav",
                    "data": audio['bytes']
                }
                
                # التوجيه الثقافي والتقني الدقيق لمنع ظهور الأسماء القديمة غير المرغوبة
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
                
                # مسح رسالة التحميل وعرض النص النهائي بشكل مرئي بليغ وثابت
                st.success("✨ تم صياغة المخرج البرمجي بنجاح!")
                
                # عرض النص داخل قالب محادثة احترافي ليبقى ثابتاً ولا يضيع تحت الأفاتار
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                
                # حفظ النص في الجلسة لمنع اختفائه عند الضغط على أزرار أخرى
                st.session_state['current_designed_post'] = response.text

            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الذكاء الاصطناعي للصوت: {e}")

# 4. زر النشر المباشر والتلقائي إلى التليجرام
if 'current_designed_post' in st.session_state:
    st.write("---")
    st.write("🚀 **خطوة الإطلاق والبث المباشر:**")
    
    # دالة إرسال التليجرام
    def send_to_telegram(text):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
        return requests.post(url, json=payload).json()
        
    if st.button("نشر هذا التصميم فوراً إلى صفحة وقناة العمل عبر الـ API"):
        with st.spinner("جاري بث المنشور عبر القنوات الرقمية..."):
            res = send_to_telegram(st.session_state['current_designed_post'])
            if res.get("ok"):
                st.success("🎉 تم بث منشورك الاحترافي بنجاح مذهل عبر البوت!")
            else:
                st.error(f"تفاصيل الخطأ في الإرسال: {res}")

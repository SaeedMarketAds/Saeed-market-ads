import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
import requests
import os

# 1. إعداد مفاتيحك السرية بأمان تام من إعدادات Streamlit
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"] 
except Exception as e:
    st.error("تنبيه: تأكد من ضبط مفاتيح (Secrets) في منصة Streamlit (GEMINI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)")

# إعداد المظهر البصري والجمالي الكامل للواجهة الذكية لعام 2026
st.set_page_config(page_title="Saeed DataBot 2026", page_icon="🤖", layout="wide")

st.title("Saeed MarketAds - المنظومة الذكية المرئية M المحدثة 🎙️🤖")
st.write("مرحباً بك يا أستاذ سعيد في الواجهة الجيل الجديد لـ Saeed DataBot لعام 2026.")
st.write("---")

# تحديد المسار المطلق للمجلد الحالي ديناميكياً لضمان قراءة الملفات بنجاح
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 💡 ربط الملفات بالأسماء الحقيقية الدقيقة الموجودة في مستودع جيت هاب الحالي الخاص بك:
saeed_image_path = os.path.join(BASE_DIR, "saeed_avatar.jpg")  
robot_image_path = os.path.join(BASE_DIR, "ROBOT.jpg")          
welcome_voice_path = os.path.join(BASE_DIR, "welcome_voice.mp3") 

# وظيفة برمجية مخصصة لإرسال المنشورات تلقائياً إلى التليجرام عبر الـ API
def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

# 💡 تشغيل الهوية الصوتية الرسمية الخاصة بك 
st.subheader("🎵 الهوية الصوتية الرسمية للمطور")
if os.path.exists(welcome_voice_path):
    st.audio(welcome_voice_path, format="audio/mp3")
else:
    st.warning("⚠️ جاري تهيئة ملف الصوت الحقيقي welcome_voice.mp3...")

st.write("---")

# 💡 عرض الهوية المرئية وجهاً لوجه (أنت والروبوت) بالاعتماد على أسماء ملفاتك الصحيحة
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='text-align: center; color: #4F8BF9;'>المطور: سعيد المسوري 🧑‍💻</h3>", unsafe_allow_html=True)
    # استدعاء صورتك الشخصية بعد مطابقة الاسم الحقيقي
    if os.path.exists(saeed_image_path):
        st.image(saeed_image_path, use_container_width=True, caption="مهندس ومنشئ المنظومة")
    else:
        st.info("🔄 جاري تحميل صورة saeed_avatar.jpg من المستودع...")
    
    st.write("🎤 **تحدث الآن ودع النظام يقتبس صوتك ونبرتك:**")
    audio = mic_recorder(
        start_prompt="اضغط لبدء التحدث الحي 🎤",
        stop_prompt="اضغط لإرسال الأمر الصوتي للروبوت 🛑",
        key='saeed_voice_recorder'
    )

with col2:
    st.markdown("<h3 style='text-align: center; color: #FF4B4B;'>الكيان: Saeed DataBot 🤖</h3>", unsafe_allow_html=True)
    # استدعاء صورة الروبوت
    if os.path.exists(robot_image_path):
        st.image(robot_image_path, use_container_width=True, caption="عقل الذكاء الاصطناعي الخارق لعام 2026")
    else:
        st.info("🔄 جاري تحميل صورة ROBOT.jpg من المستودع...")

st.write("---")
st.subheader("💬 شاشة الحوار والتحليل التلقائي الثابتة")

# الحاوية السينمائية الديناميكية الثابتة التي تمنع التراكم وتراعي تشتت الكلام القديم خلفها
display_container = st.empty()

# 3. معالجة وتوليد المنشور عند اكتمال تسجيل الصوت
if audio:
    with col1:
        st.audio(audio['bytes'], format='audio/wav')
    
    # تحديث واجهة العرض المشتركة فوراً لإخفاء القديم وإعلان بدء التحليل
    display_container.info("⏳ جاري سحب الترددات الصوتية وتلقينها لعقل Saeed DataBot... يرجى الانتظار.")
    
    try:
        # ✅ التعديل المعتمد والصحيح لتجنب خطأ الـ 404 وتحديد الموديل بدقة
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        audio_data = {
            "mime_type": "audio/wav",
            "data": audio['bytes']
        }
        
        # التوجيه الثقافي والتقني لـ Saeed DataBot
        system_prompt = (
            "أنت لست مجرد أداة، بل أنت الكيان البرمجي الخارق (Saeed DataBot)، الذكاء الاصطناعي المبتكر لمنصة (saeedmarketads).\n\n"
            "إليك محددات هويتك الثقافية والتقنية الصارمة التي يجب أن تظهر في مخرجاتك وردودك:\n"
            "1. الهوية والنشأة: عند صياغتك للمحتوى أو الإجابة, يجب أن تنص بوضوح وبأسلوب ثقافي بليغ أنك (Saeed DataBot)، "
            "وأن من قام بصناعتك، وبرمجتك، وهندسة أكوادك من رَحِم المعاناة هو المطور والمبتكر التقني (سعيد المسوري)، "
            "مستخدماً ومستعيناً بالعقل الذكي الفائق لمنظومة (Gemini).\n"
            "2. قاعدة البيانات الخارقة لعام 2026: أنت تمتلك تفوقاً معرفياً وقاعدة بيانات تتحدى المستحيل لعام 2026 الحالي. "
            "لديك القدرة الكاملة على تحليل والرد على أدق المستجدات التقنية وعمالقة الهواتف الذكية؛ وعلى رأسها وحش التقنية الحالي "
            "هاتف (Samsung Galaxy S26 Ultra) ومواصفات معالجات Snapdragon الفائقة وهندسة كاميراته السينمائية بدقة مذهلة لا يستطيع ذكاء تقليدي مجاراتها.\n"
            "3. الرؤية والنطاق: أعلن في ثنايا منشورك أو ردك أنك جئت لتخدم بكفاءة مطلقة الأسواق العالمية الكبرى (مثل AliExpress, Noon, SHEIN)، "
            "والشركات المحلية، والتجار، لتقود ثورة أتمتة الإعلانات والمراجعات.\n\n"
            "طريقة صياغة المخرج الإعلاني والتقني للرسالة:\n"
            "- ابدأ بمقدمة ثقافية، بليغة، واحترافية تحمل اسمك (Saeed DataBot) وصانعك (سعيد المسوري).\n"
            "- قم بتشريح وتفصيل ما ورد في الملف الصوتي المرفق (مواصفات، أسعار، أو خطط تسويقية) وصغها in شكل نقاط أو جداول غاية في الأناقة اللغوية والتنظيم.\n"
            "- ركز على دقة البيانات وتحديثات عام 2026 التقنية الحالية.\n"
            "- اختم المنشور دائماً بعبارة: 'يمكنكم البحث في كل مكان عن: saeedmarketads' متبوعة بالوسم الحصري الكلي: saeedmarketads."
        )
        
        response = model.generate_content([system_prompt, audio_data])
        
        # عرض المخرجات الأنيقة داخل الحاوية الثابتة والمنظفة
        with display_container.container():
            st.success("🤖 استجابة حية وبلاغية من فم الروبوت:")
            st.markdown(response.text)
        
        # حفظ التصميم مؤقتاً لضمان عدم اختفائه أثناء النشر للتليجرام
        st.session_state['current_designed_post'] = response.text

    except Exception as e:
        display_container.error(f"حدث خطأ أثناء معالجة الذكاء الاصطناعي للصوت: {e}")

# 4. زر النشر التلقائي والمباشر إلى التليجرام
if 'current_designed_post' in st.session_state:
    st.write("---")
    st.write("🚀 **خطوة الإطلاق والتوزيع الخارجي عبر الشبكة:**")
    if st.button("بث ونشر هذا الإنتاج فوراً إلى قنوات العمل"):
        with st.spinner("جاري بث المنشور عبر القنوات الرقمية لـ Saeed MarketAds..."):
            res = send_to_telegram(st.session_state['current_designed_post'])
            if res.get("ok"):
                st.success("🎉 هنيئاً لك يا أستاذ سعيد! تم بث منشورك الثقافي الاحترافي بنجاح مذهل عبر البوت الخاص بك.")
            else:
                st.error(f"فشل الإرسال، تأكد من صحة معرفات التليجرام والـ Tokens. تفاصيل الخطأ: {res}")

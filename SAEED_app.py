import streamlit as st
import google.generativeai as genai
import cloudscraper
import requests
import os
import base64
import edge_tts
import tempfile
import asyncio
from bs4 import BeautifulSoup
import re
import pandas as pd
from io import StringIO, BytesIO
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import time
# ==========================================
# ==========================================
# 1. الاستيرادات (Imports)
# ==========================================
import streamlit as st
import google.generativeai as genai
import pandas as pd
import requests
from io import StringIO

# ==========================================
# 2. إعدادات الموديلات (القاموس الذي طلبته)
# ==========================================
# أضف هذا السطر تحت تعريف MODEL_MAPPING مباشرة


# هنا تحدد الموديل الذي تريده (فقط غيّر هذه الكلمة لـ "3.1" إذا أردت التغيير)
# تعريفات بسيطة ليرتاح الكود القديم
DEFAULT_MODEL = "gemini-1.5-flash"
AVAILABLE_MODELS = ["3.5", "3.1"]
MODEL_MAPPING = {"3.5": "gemini-1.5-flash", "3.1": "gemini-1.5-pro"}


# ==========================================
# 3. الدوال (تعريف الوظائف)
# ==========================================

def get_system_instructions():
    try:
        with open('identity.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "You are a helpful assistant."

@st.cache_resource(ttl=3600)
def init_gemini():
    # هنا نستخدم القاموس لاختيار الموديل بناءً على ACTIVE_MODEL
    model_name = MODEL_MAPPING.get(ACTIVE_MODEL, "gemini-1.5-flash")
    
    if "GEMINI_MAIN_KEY" not in st.secrets:
        st.error("⚠️ مفتاح API غير موجود.")
        return None
        
    try:
        genai.configure(api_key=st.secrets["GEMINI_MAIN_KEY"])
        model = genai.GenerativeModel(
            model_name=model_name, 
            system_instruction=get_system_instructions() 
        )
        return model
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# دالة جلب المنتجات (التي ستستخدمها لاحقاً)
@st.cache_data(ttl=3600)
def load_products_from_csv():
    # كود جلب المنتجات يوضع هنا
    return None 

# ==========================================
# 4. أمر التشغيل (يأتي بعد كل الدوال)
# ==========================================
st.session_state.model = init_gemini()

# ==========================================
# 5. واجهة التطبيق (بدء عرض المحتوى)
# ==========================================
# هنا يمكنك كتابة كود الواجهة (st.write, st.image...)


# ==========================================
# 2. دالة التعليمات (الهوية والقواعد)
# ==========================================
def get_system_instructions():
    try:
        with open('identity.txt', 'r', encoding='utf-8') as f1:
            identity = f1.read()
        with open('rules.txt', 'r', encoding='utf-8') as f2:
            rules = f2.read()
        return f"{identity}\n\n[القواعد والالتزامات]:\n{rules}"
    except Exception:
        return """
        أنت مساعد ذكي متخصص في الأسواق الخليجية.
        هويتك: Saeed DaTaBoT، المساعد الذكي لمنصة SaeedMarketAds.
        المطور: سعيد المسوري.
        ردودك باللغة العربية الفصحى.
        قواعد:
        1. عند سؤالك عن هويتك أو المطور: عرف نفسك بالاسم والمطور.
        2. عند تحليل المنتجات: لا تذكر اسمك أو اسم المنصة.
        3. تحليل المنتجات: مختصر (≤200 كلمة).
        4. استخدم العملة المحلية حسب الدولة.
        5. لا تستخدم رموزاً مثل ⭐ أو ★ في تحليل المنتجات.
        """

# ==========================================
# 3. تهيئة الموديل مع التخزين المؤقت
# ==========================================
@st.cache_resource(ttl=3600)
def init_gemini(model_name):
    if "GEMINI_MAIN_KEY" not in st.secrets:
        st.error("⚠️ مفتاح API غير موجود في secrets.toml")
        return None
    genai.configure(api_key=st.secrets["GEMINI_MAIN_KEY"])
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=get_system_instructions()
    )

# ==========================================
# 4. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="سوق سعيد | متاجر SHEIN - نون - علي اكسبرس",
    page_icon="🛍️",
    layout="wide"
)

# ==========================================
# 5. CSS (التصميم + الميكروفون)
# ==========================================
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: rgba(0,0,0,0.2); }
.stMarkdown { color: #fff; }
.stButton > button {
    background: linear-gradient(90deg, #ff6b6b, #feca57);
    color: white;
    border: none;
    border-radius: 30px;
    padding: 12px 28px;
    font-weight: bold;
    font-size: 16px;
    transition: all 0.3s ease;
    width: 100%;
}
.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #feca57, #ff6b6b);
    box-shadow: 0 5px 20px rgba(0,0,0,0.3);
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.1);
    color: white;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.2);
    padding: 12px 20px;
}
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.1);
    color: white;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.2);
}
.product-card {
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(250,250,255,0.95));
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
}
.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.25);
}
.product-code {
    position: absolute;
    top: 10px;
    right: 15px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: bold;
    direction: ltr;
}
.product-name {
    font-size: 16px;
    font-weight: bold;
    color: #1e293b;
    margin-bottom: 12px;
    min-height: 50px;
    padding-right: 60px;
}
.product-price {
    color: #ff4757;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;
}
.old-price {
    color: #999;
    font-size: 14px;
    text-decoration: line-through;
    margin-right: 10px;
}
.product-sales {
    color: #2ecc71;
    font-weight: bold;
    font-size: 13px;
    margin-bottom: 10px;
}
.product-discount {
    background: #ff6b6b;
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    display: inline-block;
}
.product-btn {
    background: linear-gradient(90deg, #667eea, #764ba2);
    border-radius: 40px;
    padding: 12px;
    text-align: center;
    cursor: pointer;
    font-weight: bold;
    color: white;
    transition: all 0.3s ease;
    margin-top: 15px;
    border: none;
}
.product-btn:hover {
    background: linear-gradient(90deg, #764ba2, #667eea);
    transform: scale(1.02);
}
hr { border-color: rgba(255,255,255,0.1); }

.hero-section {
    background: linear-gradient(135deg, #ff6b6b, #feca57, #ff6b6b);
    background-size: 300% 300%;
    animation: gradientShift 5s ease infinite;
    padding: 40px;
    border-radius: 30px;
    text-align: center;
    margin-bottom: 30px;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hero-title {
    color: #fff;
    font-size: 48px;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
.hero-subtitle {
    color: #fff;
    font-size: 22px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}
.hero-code {
    background: white;
    display: inline-block;
    padding: 15px 50px;
    border-radius: 80px;
    margin: 10px 0;
}
.hero-code-text {
    color: #ff0844;
    margin: 0;
    font-size: 45px;
    font-weight: bold;
}

.shein-section {
    background: linear-gradient(135deg, rgba(255,107,107,0.1), rgba(254,202,87,0.1));
    border-radius: 30px;
    padding: 25px;
    margin: 20px 0;
    border: 2px solid rgba(254,202,87,0.3);
}
.shein-header {
    background: linear-gradient(135deg, #ff6b6b, #feca57);
    border-radius: 20px;
    padding: 15px 25px;
    text-align: center;
    margin-bottom: 25px;
}
.shein-header h2 {
    color: #fff;
    margin: 0;
    font-size: 28px;
}
.shein-header p {
    color: #fff;
    margin: 5px 0 0 0;
    font-size: 16px;
    opacity: 0.9;
}

/* تنسيق زر الميكروفون (شبيه بـ Gemini) */
[data-testid="stAudio"] { display: none; }

.stMicRecorder {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 10px 0;
}
.stMicRecorder button {
    width: 80px !important;
    height: 80px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #4285f4, #34a853) !important;
    color: white !important;
    font-size: 36px !important;
    border: none !important;
    box-shadow: 0 8px 20px rgba(66, 133, 244, 0.4) !important;
    transition: all 0.3s ease;
}
.stMicRecorder button:hover {
    transform: scale(1.05);
    box-shadow: 0 12px 30px rgba(66, 133, 244, 0.6);
}
.stMicRecorder button:active {
    transform: scale(0.95);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ==========================================
# 6. دوال الصوت (TTS) مع معالجة أفضل للأخطاء
# ==========================================
async def generate_audio(text, voice="ar-SA-HamedNeural"):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
            output = tmp.name
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output)
        with open(output, 'rb') as f:
            audio_bytes = f.read()
        os.unlink(output)
        return audio_bytes
    except Exception as e:
        st.warning(f"⚠️ خطأ في توليد الصوت: {e}")
        return None

def play_voice(text):
    if not text:
        return False
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_bytes = loop.run_until_complete(generate_audio(text))
        loop.close()
        if audio_bytes:
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(
                f'<audio autoplay style="display:none;"><source src="data:audio/mp3;base64,{b64}"></audio>',
                unsafe_allow_html=True
            )
            return True
    except Exception as e:
        st.warning(f"⚠️ خطأ في تشغيل الصوت: {e}")
    return False

# ==========================================
# 7. دوال جلب المنتجات
# ==========================================
@st.cache_data(ttl=3600)
def load_products_from_csv():
    try:
        url = 'https://raw.githubusercontent.com/SaeedMarketAds/Saeed-market-ads/main/products.csv'
        r = requests.get(url)
        if r.status_code == 200:
            return pd.read_csv(StringIO(r.text))
    except:
        pass
    return None

def get_golden_deals_from_csv():
    df = load_products_from_csv()
    if df is not None and 'discount' in df.columns:
        return df[df['discount'] >= 50].to_dict('records')
    return []

# ==========================================
# 8. بيانات المنتجات (ثابتة)
# ==========================================
SHEIN_PRODUCTS = [
    {"code": "SH001", "name": "معطف مبطن بغطاء رأس للفتيات", "price": 19.39, "discount": 43, "link": "https://onelink.shein.com/38/5shrzfcizjmg", "sales": "150+"},
    {"code": "SH002", "name": "قميص أنيق بتصميم هونج كونج", "price": 14.18, "discount": 37, "link": "https://onelink.shein.com/38/5shune7n90yf", "sales": "200+"},
    {"code": "SH003", "name": "نظارات حفلات مطبوعة 6 قطع", "price": 2.70, "discount": 0, "link": "https://onelink.shein.com/38/5shujg5f2ywk", "sales": "300+"},
    {"code": "SH004", "name": "حقيبة مستلزمات سفر مقاومة للماء", "price": 3.90, "discount": 17, "link": "https://onelink.shein.com/38/5shuimjyfjt7", "sales": "100+"},
    {"code": "SH005", "name": "معطف رجالي كاجوال سادة", "price": 25.67, "discount": 24, "link": "https://onelink.shein.com/38/5shui8qqn60h", "sales": "200+"},
]

GOLDEN_DEALS = [
    {"name": "Men Ice Silk Polo Shirt", "price": 4.71, "discount": 60, "link": "#", "sales": "500+"},
    {"name": "Pajama Set Button Front", "price": 6.91, "discount": 69, "link": "#", "sales": "300+"},
    {"name": "Shower Curtain Set", "price": 4.47, "discount": 70, "link": "#", "sales": "200+"},
    {"name": "Sports Waist Belt", "price": 5.12, "discount": 61, "link": "#", "sales": "400+"},
]

# ==========================================
# 9. دوال تحليل الرابط
# ==========================================
def check_link_status(url):
    try:
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False},
            interpreter='nodejs'
        )
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        r = scraper.get(url, timeout=20, headers=headers, allow_redirects=True)
        if r.status_code == 200:
            return 'متاح', r.text
        elif r.status_code in [404, 410]:
            return 'غير موجود', None
        else:
            return check_link_status_fallback(url)
    except:
        return 'غير موجود', None

def check_link_status_fallback(url):
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        r = session.get(url, timeout=20, allow_redirects=True, verify=False)
        if r.status_code == 200:
            return 'متاح', r.text
    except:
        pass
    return 'غير موجود', None

def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(["script", "style", "noscript", "meta", "link"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:50000] + ("..." if len(text) > 50000 else "")

def get_currency(country):
    mapping = {
        "السعودية": "ريال سعودي", "الإمارات": "درهم إماراتي",
        "الكويت": "دينار كويتي", "قطر": "ريال قطري",
        "عمان": "ريال عماني", "البحرين": "دينار بحريني"
    }
    return mapping.get(country, "ريال سعودي")

# ==========================================
# 10. الردود السريعة
# ==========================================
def quick_response(question):
    q = question.lower()
    if "السلام" in q or "مرحبا" in q or "هلا" in q:
        return "وعليكم السلام ورحمة الله وبركاته"
    elif "كيف حال" in q or "كيفك" in q:
        return "بخير والحمد لله، أنا هنا لخدمتك."
    elif "كود" in q or "خصم" in q:
        return "كود الخصم الحصري هو: N73QS"
    elif any(w in q for w in ["من أنت", "من برمج", "مين أنت", "من صنعك"]):
        return "أنا Saeed DaTaBoT، المساعد الذكي لمنصة SaeedMarketAds. تم تطويري بواسطة سعيد المسوري، مؤسس المنصة."
    elif "شكرا" in q:
        return "العفو، أنا في خدمتك."
    return None

# ==========================================
# 11. دوال تحويل الصوت ومعالجة الاستعلامات (مع إصلاح مشكلة التنسيق)
# ==========================================
def convert_audio_to_wav(audio_bytes):
    """تحويل أي صيغة صوت إلى WAV باستخدام pydub"""
    if not PYDUB_AVAILABLE:
        st.error("⚠️ مكتبة pydub غير مثبتة. الرجاء تثبيتها: `pip install pydub` مع تثبيت ffmpeg.")
        return None
    try:
        audio = AudioSegment.from_file(BytesIO(audio_bytes))
        wav_io = BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        return wav_io.read()
    except Exception as e:
        st.error(f"⚠️ خطأ في تحويل الصوت: {e}")
        return None

def transcribe_audio(audio_bytes):
    try:
        wav_bytes = convert_audio_to_wav(audio_bytes)
        if wav_bytes is None:
            # إذا فشل التحويل، نحاول مباشرة (قد تنجح مع بعض الصيغ)
            wav_bytes = audio_bytes

        recognizer = sr.Recognizer()
        with sr.AudioFile(BytesIO(wav_bytes)) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language='ar-AR')
    except sr.UnknownValueError:
        st.warning("⚠️ لم أستطع فهم الصوت، حاول مرة أخرى بوضوح.")
    except sr.RequestError as e:
        st.error(f"⚠️ خطأ في الاتصال بخدمة التعرف: {e}")
    except Exception as e:
        st.error(f"⚠️ حدث خطأ: {e}")
    return None

def display_and_speak(text):
    if not text:
        return
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'>
        <h4 style='color: #feca57;'>🤖 الرد:</h4>
        <p style='color: #e2e8f0;'>{text}</p>
    </div>
    """, unsafe_allow_html=True)
    play_voice(text[:500])

def process_query(query, model):
    if not query:
        return
    quick = quick_response(query)
    if quick:
        display_and_speak(quick)
        return
    if model is None:
        st.warning("⚠️ النموذج غير مهيأ. يرجى اختيار موديل صحيح.")
        return
    try:
        with st.spinner("🤖 جاري التفكير..."):
            response = model.generate_content(f"""
            أجب على هذا السؤال باللغة العربية الفصحى:
            {query}

            تنبيهات:
            - إذا سأل عن هويتك، عرف بنفسك كـ Saeed DaTaBoT المساعد الذكي لـ SaeedMarketAds والمطور سعيد المسوري.
            - إذا سأل عن تحليل منتج، لا تذكر اسمك.
            - كن مختصراً وواضحاً.
            """)
            clean = re.sub(r'[⭐★✨]', '', response.text)
            clean = re.sub(r'\s+', ' ', clean).strip()
            display_and_speak(clean)
    except Exception as e:
        st.error(f"❌ خطأ أثناء معالجة الطلب: {e}")

# ==========================================
# 12. دوال الأفاتار والمحادثة (تُعرَّف مبكراً لتجنب NameError)
# ==========================================
def animate_avatar(image_path, duration=1.5):
    """تأثير وميض وتحريك بسيط لمحاكاة حركة الشفاه"""
    if not os.path.exists(image_path):
        return
    placeholder = st.empty()
    for i in range(3):
        placeholder.image(image_path, width=180, caption="🗣️ يتحدث...")
        time.sleep(0.15)
        placeholder.image(image_path, width=170, caption=" ")
        time.sleep(0.15)
    placeholder.image(image_path, width=180, caption="سعيد")

def process_query_avatar(query, model):
    """معالجة الاستعلام وعرضه مع الأفاتار والصوت"""
    if not query:
        return
    # إضافة سؤال المستخدم للمحادثة
    st.session_state.conversation.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    # الحصول على الرد
    quick = quick_response(query)
    if quick:
        ai_reply = quick
    elif model is None:
        ai_reply = "⚠️ النموذج غير مهيأ."
    else:
        with st.spinner("🤖 جاري التفكير..."):
            try:
                response = model.generate_content(f"""
                أجب على هذا السؤال باللغة العربية الفصحى:
                {query}

                تنبيهات:
                - إذا سأل عن هويتك، عرف بنفسك كـ Saeed DaTaBoT المساعد الذكي لـ SaeedMarketAds والمطور سعيد المسوري.
                - إذا سأل عن تحليل منتج، لا تذكر اسمك.
                - كن مختصراً وواضحاً.
                """)
                ai_reply = re.sub(r'[⭐★✨]', '', response.text)
                ai_reply = re.sub(r'\s+', ' ', ai_reply).strip()
            except Exception as e:
                ai_reply = f"❌ خطأ: {e}"

    # عرض الرد في الدردشة
    with st.chat_message("assistant"):
        st.write(ai_reply)
    
    # تشغيل الصوت وتحريك الأفاتار
    if st.session_state.voice_enabled and ai_reply:
        animate_avatar(st.session_state.current_avatar, duration=1.2)
        if st.session_state.use_recorded_voice and st.session_state.recorded_voice_path and os.path.exists(st.session_state.recorded_voice_path):
            with open(st.session_state.recorded_voice_path, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format='audio/mp3')
        else:
            play_voice(ai_reply[:500])

    st.session_state.conversation.append({"role": "assistant", "content": ai_reply})
    st.rerun()

# ==========================================
# 13. تهيئة النموذج وحالة الجلسة
# ==========================================
if 'model_name' not in st.session_state:
    st.session_state.model_name = DEFAULT_MODEL
if 'model' not in st.session_state or st.session_state.model is None:
    st.session_state.model = init_gemini(st.session_state.model_name)

# متغيرات الأفاتار والصوت المسجل
if 'current_avatar' not in st.session_state:
    st.session_state.current_avatar = "saeed.jpg" if os.path.exists("saeed.jpg") else "ROBOT.jpg"
if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = True
if 'use_recorded_voice' not in st.session_state:
    st.session_state.use_recorded_voice = False
if 'recorded_voice_path' not in st.session_state:
    st.session_state.recorded_voice_path = None
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'products' not in st.session_state:
    st.session_state.products = []

# ==========================================
# 14. الغلاف العلوي
# ==========================================
st.markdown("""
<div class='hero-section'>
    <h1 class='hero-title'>🛍️ سوق سعيد</h1>
    <p class='hero-subtitle'>متجر SHEIN | نون | علي اكسبرس</p>
    <div style='margin: 20px 0;'>
        <span style='background: #ff6b6b; color: white; padding: 10px 30px; border-radius: 30px; font-size: 18px;'>
            🤖 مساعد ذكي للتسوق
        </span>
    </div>
    <div style='background: rgba(255,255,255,0.2); border-radius: 20px; padding: 20px; margin-top: 15px;'>
        <p style='color: #fff; font-size: 20px; margin: 0;'>🎁 كود الخصم الحصري</p>
        <div class='hero-code'>
            <h1 class='hero-code-text'>N73QS</h1>
        </div>
        <p style='color: #fff; font-size: 18px; margin: 5px 0 0 0;'>🔥 خصم يصل إلى 60% على أول طلب</p>
    </div>
</div>
""", unsafe_allow_html=True)

play_voice("مرحباً بكم في سوق سعيد، منصة التسوق الذكية. استمتعوا بأفضل العروض والخصومات.")

# ==========================================
# 15. السايدبار (مع إعدادات الأفاتار والصوت)
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 30px; margin-bottom: 20px;'>
        <h2 style='color: #feca57;'>🤖 المساعد الذكي</h2>
        <p style='color: #aaa;'>للتسوق والاستشارات</p>
    </div>
    """, unsafe_allow_html=True)

    country = st.selectbox("🌍 اختر دولتك:", ["السعودية", "الإمارات", "الكويت", "قطر", "عمان", "البحرين"], index=0)

    # اختيار الموديل مع تحديث فوري
    model_choice = st.selectbox(
        "🧠 اختر الموديل:",
        AVAILABLE_MODELS,
        index=AVAILABLE_MODELS.index(st.session_state.model_name) if st.session_state.model_name in AVAILABLE_MODELS else 0
    )

    if model_choice != st.session_state.model_name:
        st.session_state.model_name = model_choice
        st.session_state.model = init_gemini(model_choice)

    model = st.session_state.model

    if model:
        st.success(f"✅ يعمل على {st.session_state.model_name}")
    else:
        st.error("⚠️ فشل تهيئة النموذج (تأكد من المفتاح)")

    st.markdown("---")
    st.markdown("### 🔥 العروض المميزة")
    if st.button("🔥 عرض الغلات الآن", use_container_width=True):
        st.session_state.show_golden = True
        st.session_state.store = None

    if st.session_state.get('show_golden', False):
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ff6b6b, #feca57); border-radius: 20px; padding: 15px; text-align: center; margin: 10px 0;'>
            <h4 style='color: #fff;'>🔥 العروض الذهبية</h4>
        </div>
        """, unsafe_allow_html=True)
        golden = get_golden_deals_from_csv() or GOLDEN_DEALS
        for prod in golden[:5]:
            final = prod['price'] * (1 - prod['discount']/100)
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); border-radius: 15px; padding: 12px; margin-bottom: 10px; border-right: 4px solid #feca57;'>
                <p style='color: #e2e8f0; margin: 0;'><b>{prod['name'][:30]}...</b></p>
                <p style='color: #feca57; margin: 0;'>💰 ${final:.2f} <span style='color: #ff6b6b; text-decoration: line-through;'>${prod['price']:.2f}</span></p>
                <p style='color: #2ecc71; margin: 0;'>خصم {prod['discount']}%</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 خدماتي:")
    st.markdown("- ✅ تحليل الروابط المتقدم")
    st.markdown("- ✅ عروض SHEIN")
    st.markdown("- ✅ عروض نون")
    st.markdown("- ✅ محادثة ذكية (نص + صوت)")
    st.markdown("---")
    
    # إعدادات الأفاتار والصوت
    st.markdown("### 🎭 الأفاتار والصوت")
    avatar_option = st.selectbox("اختر الأفاتار", ["سعيد (saeed.jpg)", "روبوت (ROBOT.jpg)", "صورتي أنا (ارفع صورة)"])
    if avatar_option == "سعيد (saeed.jpg)":
        st.session_state.current_avatar = "saeed.jpg" if os.path.exists("saeed.jpg") else "ROBOT.jpg"
    elif avatar_option == "روبوت (ROBOT.jpg)":
        st.session_state.current_avatar = "ROBOT.jpg" if os.path.exists("ROBOT.jpg") else "saeed.jpg"
    else:
        uploaded_img = st.file_uploader("ارفع صورتك", type=["jpg", "png"], key="avatar_upload")
        if uploaded_img:
            with open("my_avatar.jpg", "wb") as f:
                f.write(uploaded_img.getbuffer())
            st.session_state.current_avatar = "my_avatar.jpg"
    
    st.session_state.voice_enabled = st.checkbox("🔊 تفعيل الصوت", value=True)
    st.session_state.use_recorded_voice = st.checkbox("🎙️ استخدام صوتي المسجل (للردود)", value=False)
    if st.session_state.use_recorded_voice:
        recorded_voice_file = st.file_uploader("ارفع ملف صوتي (mp3) للردود", type=["mp3"], key="voice_upload")
        if recorded_voice_file:
            with open("my_voice.mp3", "wb") as f:
                f.write(recorded_voice_file.getbuffer())
            st.session_state.recorded_voice_path = "my_voice.mp3"
            st.success("تم رفع صوتك! سيتم استخدامه لكل رد.")
        else:
            if os.path.exists("my_voice.mp3"):
                st.session_state.recorded_voice_path = "my_voice.mp3"
                st.info("صوتك المسجل موجود مسبقاً.")
            else:
                st.warning("يرجى رفع ملف صوتي لتفعيل هذه الخاصية.")
    
    st.markdown("---")
    st.markdown("### 📞 للتواصل:")
    st.markdown("[@SaeedMarketAds](https://t.me/SaeedMarketAds)")
    st.markdown("---")
    st.caption("© 2026 سوق سعيد")

# ==========================================
# 16. Tabs (مع إضافة تبويب إدارة المنتجات)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["🛍️ متجر المنتجات", "🔍 أداة الفحص المتقدم", "💬 المحادثة الذكية", "🗂️ إدارة المنتجات"])

# ==========================================
# 17. تبويب المنتجات (نفس الكود الأول)
# ==========================================
with tab1:
    st.subheader("اختر المتجر للتصفح:")
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("🛍️ تصفح SHEIN"):
        st.session_state.store = "SHEIN"
        st.session_state.show_golden = False
    if col2.button("💛 تصفح Noon"):
        st.session_state.store = "Noon"
        st.session_state.show_golden = False
    if col3.button("🚀 تصفح AliExpress"):
        st.session_state.store = "AliExpress"
        st.session_state.show_golden = False
    if col4.button("🔥 الغلات"):
        st.session_state.show_golden = True
        st.session_state.store = None

    if st.session_state.get('show_golden', False):
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ff6b6b, #feca57); border-radius: 30px; padding: 20px; text-align: center; margin: 20px 0;'>
            <h2 style='color: #fff;'>🔥 عروض الغلات الحصرية 🔥</h2>
            <p style='color: #fff; font-size: 18px;'>خصومات تصل إلى 70%</p>
            <p style='color: #fff; font-size: 16px;'>🎁 استخدم كود الخصم: N73QS</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔊 استمع لعروض الغلات"):
            play_voice("مرحباً بك في عروض الغلات الحصرية. خصومات تصل إلى سبعين بالمئة على منتجات مختارة.")

        golden = get_golden_deals_from_csv() or GOLDEN_DEALS
        cols = st.columns(4)
        for i, prod in enumerate(golden[:12]):
            with cols[i % 4]:
                final = prod['price'] * (1 - prod['discount']/100)
                st.markdown(f"""
                <div class='product-card' style='border: 3px solid #feca57;'>
                    <div class='product-code' style='background: linear-gradient(90deg, #ff6b6b, #feca57);'>🔥 غلة</div>
                    <div class='product-name'>{prod['name']}</div>
                    <div class='product-price'>${final:.2f}</div>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span class='product-discount'>-{prod['discount']}%</span>
                        <span class='product-sales'>📊 {prod.get('sales', 'N/A')}</span>
                    </div>
                    <a href='{prod.get('link', '#')}' target='_blank' style='text-decoration: none;'>
                        <div class='product-btn' style='background: linear-gradient(90deg, #ff6b6b, #feca57);'>🛒 احصل على العرض</div>
                    </a>
                </div>
                """, unsafe_allow_html=True)
        st.info("✅ تم تحميل الغلات بنجاح...")

    elif st.session_state.get('store'):
        store = st.session_state.store
        st.write(f"### عرض منتجات: {store}")
        if store == "SHEIN":
            cols = st.columns(4)
            for i, prod in enumerate(SHEIN_PRODUCTS):
                with cols[i % 4]:
                    final = prod['price'] * (1 - prod['discount']/100) if prod['discount'] > 0 else prod['price']
                    st.markdown(f"""
                    <div class='product-card'>
                        <div class='product-code'>📦 {prod['code']}</div>
                        <div class='product-name'>{prod['name']}</div>
                        <div class='product-price'>${final:.2f}</div>
                        <div class='product-sales'>📊 تم البيع: {prod['sales']}</div>
                        <a href='{prod['link']}' target='_blank' style='text-decoration: none;'>
                            <div class='product-btn'>🛒 تسوق الآن</div>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
        elif store == "Noon":
            NOON_PRODUCTS = [
                {"code": "N001", "name": "ساعة ذكية رياضية", "price": 89.99, "discount": 30, "link": "https://www.noon.com/ar-sa/Z09748F5900924601C848Z/p/", "sales": "500+"},
                {"code": "N002", "name": "سماعات لاسلكية بلوتوث", "price": 45.50, "discount": 25, "link": "https://www.noon.com/ar-sa/N11200839A/p/", "sales": "1200+"},
            ]
            cols = st.columns(4)
            for i, prod in enumerate(NOON_PRODUCTS):
                with cols[i % 4]:
                    final = prod['price'] * (1 - prod['discount']/100) if prod['discount'] > 0 else prod['price']
                    st.markdown(f"""
                    <div class='product-card'>
                        <div class='product-code'>📦 {prod['code']}</div>
                        <div class='product-name'>{prod['name']}</div>
                        <div class='product-price'>${final:.2f}</div>
                        <div class='product-sales'>📊 تم البيع: {prod['sales']}</div>
                        <a href='{prod['link']}' target='_blank' style='text-decoration: none;'>
                            <div class='product-btn'>🛒 تسوق الآن</div>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
        elif store == "AliExpress":
            st.markdown("""
            <div style='text-align: center; padding: 50px; background: rgba(255,71,87,0.1); border-radius: 40px;'>
                <h3 style='color: #feca57;'>🚀 قادم قريباً جداً</h3>
                <p style='color: #ddd;'>نستعد لإطلاق متجر AliExpress مع أفضل العروض</p>
            </div>
            """, unsafe_allow_html=True)
        st.info("✅ تم تحميل المنتجات بنجاح...")

# ==========================================
# 18. تبويب تحليل الرابط (نفس الكود الأول)
# ==========================================
with tab2:
    st.subheader("🔍 أداة فحص الروابط المتقدمة")
    link = st.text_input("ضع رابط المنتج هنا:", placeholder="https://...")
    if st.button("تحليل المنتج"):
        if not link:
            st.warning("📝 يرجى إدخال رابط المنتج")
        elif not model:
            st.warning("⚠️ النموذج غير مهيأ.")
        else:
            with st.spinner("جاري التحليل..."):
                status, html = check_link_status(link)
                if status == 'متاح' and html:
                    page_text = extract_text_from_html(html)
                    currency = get_currency(country)
                    prompt = f"""
                    قم بتحليل هذا المنتج بدقة باللغة العربية الفصحى.
                    استخرج: 1. اسم المنتج 2. السعر بالعملة: {currency} 3. التقييمات 4. التوفر.
                    نص الصفحة: {page_text[:5000]}
                    تنبيهات: لا تذكر اسم Saeed DaTaBoT أو SaeedMarketAds، لا تستخدم ⭐ أو ★، استخدم {currency} فقط، كن مختصراً ≤200 كلمة.
                    """
                    try:
                        response = model.generate_content(prompt)
                        clean = re.sub(r'[⭐★✨]', '', response.text)
                        clean = re.sub(r'Saeed\s*DaTaBoT|SaeedMarketAds', '', clean, flags=re.IGNORECASE)
                        clean = re.sub(r'\s+', ' ', clean).strip()
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'>
                            <h4 style='color: #feca57;'>📊 نتيجة التحليل:</h4>
                            <p style='color: #e2e8f0; white-space: pre-wrap;'>{clean}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        play_voice(clean[:200])
                    except Exception as e:
                        st.error(f"خطأ: {e}")
                else:
                    st.warning("⚠️ الرابط غير متاح أو لا يحتوي على محتوى.")

# ==========================================
# 19. تبويب المحادثة الذكية (مع الأفاتار والصوت المسجل)
# ==========================================
with tab3:
    st.subheader("💬 المحادثة الذكية (نص + صوت)")
    if not PYDUB_AVAILABLE:
        st.warning("⚠️ مكتبة pydub غير مثبتة. لتحويل الصوت بشكل صحيح، قم بتثبيتها: `pip install pydub` مع تثبيت ffmpeg. قد لا تعمل خاصية الميكروفون بشكل صحيح.")
    st.info("💡 يمكنك إما كتابة سؤالك أو استخدام الميكروفون للتحدث. سيتحرك الأفاتار أثناء النطق.")

    # عرض المحادثة السابقة
    for msg in st.session_state.conversation:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # عمودان للميكروفون والنص
    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown("#### 🎤 تحدث")
        audio = mic_recorder(
            start_prompt="🎤 اضغط للتحدث",
            stop_prompt="⏹️ أوقف",
            just_once=True,
            key='mic_recorder'
        )
        if audio and audio.get('bytes'):
            st.audio(audio['bytes'], format='audio/wav')
            with st.spinner("🔄 جاري تحويل الصوت إلى نص..."):
                user_text = transcribe_audio(audio['bytes'])
                if user_text:
                    st.success(f"📝 النص المُستمع: {user_text}")
                    process_query_avatar(user_text, model)

    with col2:
        st.markdown("#### ✍️ أو اكتب سؤالك")
        user_query = st.chat_input("اكتب سؤالك هنا...")
        if user_query:
            process_query_avatar(user_query, model)

# ==========================================
# 20. تبويب إدارة المنتجات (إضافة وعرض)
# ==========================================
with tab4:
    st.subheader("🗂️ إدارة المنتجات المخصصة")
    st.markdown("أضف منتجك الخاص أو استعرض المنتجات المضافة.")
    
    # نموذج إضافة منتج
    with st.expander("➕ إضافة منتج جديد", expanded=False):
        with st.form(key="product_form", clear_on_submit=True):
            prod_name = st.text_input("🏷️ اسم المنتج")
            prod_price = st.number_input("💰 السعر (دولار)", min_value=0.0, step=0.5)
            prod_desc = st.text_area("📝 الوصف")
            hidden_link = st.text_input("🔗 رابط المنتج (اختياري)")
            img_link = st.text_input("🖼️ رابط صورة المنتج (اختياري)")
            submitted = st.form_submit_button("📌 نشر المنتج")
            if submitted and prod_name and prod_price > 0:
                st.session_state.products.append({
                    "name": prod_name,
                    "price": prod_price,
                    "desc": prod_desc,
                    "link": hidden_link,
                    "image": img_link
                })
                st.balloons()
                st.success(f"✅ تمت إضافة {prod_name}")
                st.rerun()
            elif submitted:
                st.error("الاسم والسعر مطلوبان")
    
    # عرض قائمة المنتجات المضافة
    st.markdown("### 📦 قائمة منتجاتي")
    if not st.session_state.products:
        st.info("لا توجد منتجات مضافة بعد. أضف منتجاً من الأعلى.")
    else:
        for idx, prod in enumerate(st.session_state.products):
            with st.container():
                c1, c2 = st.columns([1, 3])
                with c1:
                    if prod["image"]:
                        st.image(prod["image"], width=120)
                    else:
                        st.image("https://via.placeholder.com/120?text=No+Image", width=120)
                with c2:
                    st.markdown(f"### 🛍️ {prod['name']}")
                    st.markdown(f"**السعر:** 💲{prod['price']}")
                    st.markdown(f"**الوصف:** {prod['desc']}")
                    if prod["link"]:
                        st.markdown(f"[رابط المنتج]({prod['link']})")
                st.divider()
        if st.button("🗑️ حذف الكل", key="delete_all_products"):
            st.session_state.products.clear()
            st.rerun()



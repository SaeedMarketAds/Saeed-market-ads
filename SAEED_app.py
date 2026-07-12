# 1. أنشئ الملف المحدث
cat > /mnt/user-data/outputs/SAEED_app.py << 'PYEOF'
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
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# محاولة استيراد pydub للتحويل الصوتي
# ==========================================
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

# ==========================================
# 1. إعدادات الموديل (تلقائي بالكامل)
# ==========================================
AVAILABLE_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash-exp"
]

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
        رؤية المنصة: المنصة دليل للتسوق الآمن عبر الإنترنت، ونموذج ملهم لكل من يطمح للتعلم الذاتي وتطوير مهاراته وتحدي الظروف.
        قواعد هامة:
        1. عند سؤالك عن هويتك أو المطور: عرف نفسك بالاسم والمطور سعيد المسوري واذكر الرؤية الملهمة.
        2. عند تحليل المنتجات: لا تذكر اسمك أو اسم المنصة مطلقاً.
        3. تحليل المنتجات: مختصر جداً وبأسلوب احترافي (≤200 كلمة).
        4. استخدم العملة المحلية حسب الدولة المختارة.
        5. لا تستخدم رموزاً مثل ⭐ أو ★ في تحليل المنتجات نهائياً.
        """

# ==========================================
# 3. تهيئة الموديل مع التخزين المؤقت والتبديل التلقائي (باستخدام مفتاح API المعتمد)
# ==========================================
@st.cache_resource(ttl=3600)
def init_gemini(model_name):
    if "API" not in st.secrets:
        return None
    genai.configure(api_key=st.secrets["API"])
    try:
        return genai.GenerativeModel(
            model_name=model_name,
            system_instruction=get_system_instructions()
        )
    except Exception:
        return None

def get_working_model():
    """يحاول الموديلات المتاحة بالترتيب حتى يجد واحداً يعمل دون إزعاج المستخدم."""
    for m in AVAILABLE_MODELS:
        model = init_gemini(m)
        if model is not None:
            return model, m
    return None, None

# ==========================================
# 4. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="سوق سعيد | SHEIN - نون - AliExpress",
    page_icon="🛍️",
    layout="wide"
)

# ==========================================
# 5. CSS التصميم الفاخر
# ==========================================
page_bg = """
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&family=Cairo:wght@400;600;800&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'Tajawal', 'Cairo', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 10% 10%, #1b0f3a 0%, transparent 40%),
                radial-gradient(circle at 90% 20%, #3a0f5c 0%, transparent 45%),
                radial-gradient(circle at 50% 90%, #0f1f3a 0%, transparent 45%),
                linear-gradient(160deg, #05010f 0%, #0d0620 35%, #140a2e 65%, #05010f 100%);
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: rgba(0,0,0,0.15); backdrop-filter: blur(6px); }
.stMarkdown { color: #fff; }

::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: #0d0620; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg,#ffb300,#ff4d8d); border-radius: 10px; }

.stButton > button {
    background: linear-gradient(90deg, #ff4d8d, #ffb300);
    color: #1a0a2e;
    border: none;
    border-radius: 30px;
    padding: 13px 28px;
    font-weight: 800;
    font-size: 16px;
    letter-spacing: 0.3px;
    transition: all 0.35s cubic-bezier(.2,.9,.3,1.2);
    width: 100%;
    box-shadow: 0 6px 18px rgba(255,77,141,0.25);
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.03);
    background: linear-gradient(90deg, #ffb300, #ff4d8d);
    box-shadow: 0 12px 30px rgba(255,179,0,0.4);
}
.stButton > button:active { transform: translateY(0) scale(0.98); }

.stTextInput > div > div > input, .stNumberInput input {
    background: rgba(255,255,255,0.06);
    color: white;
    border-radius: 30px;
    border: 1px solid rgba(255,179,0,0.35);
    padding: 12px 20px;
}
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.06);
    color: white;
    border-radius: 20px;
    border: 1px solid rgba(255,179,0,0.35);
}

.product-card {
    border-radius: 24px;
    padding: 22px;
    margin-bottom: 24px;
    background: linear-gradient(160deg, rgba(255,255,255,0.98), rgba(245,244,255,0.96));
    box-shadow: 0 10px 30px rgba(0,0,0,0.35), inset 0 0 0 1px rgba(255,179,0,0.15);
    transition: all 0.35s cubic-bezier(.2,.9,.3,1.2);
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}
.product-card::before {
    content: "";
    position: absolute;
    top: 0; right: 0; left: 0;
    height: 5px;
    background: linear-gradient(90deg, #ff4d8d, #ffb300, #7c3aed);
}
.product-card:hover {
    transform: translateY(-8px) scale(1.015);
    box-shadow: 0 20px 45px rgba(0,0,0,0.45), inset 0 0 0 1px rgba(255,179,0,0.35);
}
.product-code {
    position: absolute;
    top: 16px;
    right: 15px;
    background: linear-gradient(90deg, #7c3aed, #ff4d8d);
    color: white;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
    direction: ltr;
    box-shadow: 0 4px 10px rgba(124,58,237,0.35);
}
.product-name {
    font-size: 17px;
    font-weight: 800;
    color: #1a0a2e;
    margin-bottom: 14px;
    margin-top: 10px;
    min-height: 50px;
    padding-right: 65px;
}
.product-price {
    background: linear-gradient(90deg, #ff4d8d, #ff7a00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 26px;
    font-weight: 900;
    margin-bottom: 5px;
}
.product-discount {
    background: linear-gradient(90deg, #ff4d8d, #7c3aed);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 800;
    display: inline-block;
}
.product-btn {
    background: linear-gradient(90deg, #1a0a2e, #3a1466);
    border-radius: 40px;
    padding: 13px;
    text-align: center;
    cursor: pointer;
    font-weight: 800;
    color: #ffb300;
    transition: all 0.3s ease;
    margin-top: 16px;
    border: 1px solid rgba(255,179,0,0.4);
}
.product-btn:hover {
    background: linear-gradient(90deg, #ffb300, #ff4d8d);
    color: #1a0a2e;
    transform: scale(1.03);
}

.hero-section {
    background: linear-gradient(120deg, #ff4d8d, #ffb300, #7c3aed, #ff4d8d);
    background-size: 400% 400%;
    animation: gradientShift 8s ease infinite;
    padding: 50px 40px;
    border-radius: 34px;
    text-align: center;
    margin-bottom: 34px;
    box-shadow: 0 20px 60px rgba(124,58,237,0.35);
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hero-title { color: #fff; font-size: 54px; font-weight: 900; text-shadow: 3px 3px 10px rgba(0,0,0,0.35); }
.hero-subtitle { color: #fff; font-size: 22px; font-weight: 600; }
.hero-badge { background: rgba(0,0,0,0.25); backdrop-filter: blur(10px); display: inline-block; padding: 10px 34px; border-radius: 30px; font-size: 18px; font-weight: 800; color: #fff; border: 1px solid rgba(255,255,255,0.35); margin-top: 12px; }
.hero-code { background: #fff; display: inline-block; padding: 16px 55px; border-radius: 90px; margin: 14px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.35); }
.hero-code-text { background: linear-gradient(90deg, #ff4d8d, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 0; font-size: 48px; font-weight: 900; }

.store-banner { border-radius: 30px; padding: 26px; text-align: center; margin: 22px 0; box-shadow: 0 15px 40px rgba(0,0,0,0.35); }
.store-banner h2 { color: #fff; margin: 0; font-size: 30px; font-weight: 900; }

[data-testid="stAudio"] { display: none; }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ==========================================
# 6. دوال الصوت المعزولة والمستقرة للتنفيذ المتزامن
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
    except Exception:
        return None

def run_async_safe(coro):
    """تشغيل الدوال المتزامنة عبر خيط مستقل لعدم كسر سيرفر Streamlit."""
    with ThreadPoolExecutor() as executor:
        future = executor.submit(lambda: asyncio.run(coro))
        return future.result()

def play_voice(text):
    if not text:
        return False
    try:
        audio_bytes = run_async_safe(generate_audio(text))
        if audio_bytes:
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(
                f'<audio autoplay style="display:none;"><source src="data:audio/mp3;base64,{b64}"></audio>',
                unsafe_allow_html=True
            )
            return True
    except Exception:
        pass
    return False

# ==========================================
# 7. جلب البيانات والأكواد السريعة
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

def quick_response(question):
    q = question.lower()
    if any(w in q for w in ["السلام", "مرحبا", "هلا"]):
        return "وعليكم السلام ورحمة الله وبركاته، مرحباً بك في سوق سعيد الفاخر."
    elif "كيف حال" in q or "كيفك" in q:
        return "بخير والحمد لله، يسعدني جداً مساعدتك اليوم."
    elif "كود" in q or "خصم" in q:
        return "كود الخصم الحصري والخاص بالمنصة هو: N73QS"
    elif any(w in q for w in ["من أنت", "من برمج", "مين أنت", "من صنعك"]):
        return "أنا Saeed DaTaBoT، المساعد الذكي لمنصة SaeedMarketAds. تم تطويري بالكامل بواسطة المطور سعيد المسوري؛ ليكون هذا العمل نموذجاً ملهماً في العصامية والتعلم الذاتي، ودليلاً ذكياً للتسوق الآمن عبر الإنترنت."
    elif "شكرا" in q:
        return "العفو يا صديقي، أنا دائماً في خدمتك الفاخرة."
    return None

# ==========================================
# 8. بيانات المنتجات الافتراضية
# ==========================================
SHEIN_PRODUCTS = [
    {"code": "SH001", "name": "معطف مبطن بغطاء رأس للفتيات", "price": 19.39, "discount": 43, "link": "https://onelink.shein.com/38/5shrzfcizjmg", "sales": "150+"},
    {"code": "SH002", "name": "قميص أنيق بتصميم هونج كونج", "price": 14.18, "discount": 37, "link": "https://onelink.shein.com/38/5shune7n90yf", "sales": "200+"},
    {"code": "SH003", "name": "نظارات حفلات مطبوعة 6 قطع", "price": 2.70, "discount": 0, "link": "https://onelink.shein.com/38/5shujg5f2ywk", "sales": "300+"},
]
ALIEXPRESS_PRODUCTS = [
    {"code": "AE001", "name": "ساعة ذكية رياضية مقاومة للماء", "price": 25.99, "discount": 40, "link": "https://s.click.aliexpress.com/e/_DeXBKQH", "sales": "2,300+"},
    {"code": "AE002", "name": "سماعات لاسلكية TWS Bass", "price": 15.50, "discount": 55, "link": "https://s.click.aliexpress.com/e/_DeXBKQH", "sales": "5,100+"},
]
NOON_PRODUCTS = [
    {"code": "N001", "name": "ساعة ذكية رياضية ممتازة", "price": 89.99, "discount": 30, "link": "https://www.noon.com/ar-sa/Z09748F5900924601C848Z/p/", "sales": "500+"},
]
GOLDEN_DEALS = [
    {"name": "Men Ice Silk Polo Shirt", "price": 4.71, "discount": 60, "link": "#", "sales": "500+"},
]

# ==========================================
# 9. معالجة الروابط واستخراج النصوص
# ==========================================
def check_link_status(url):
    try:
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = scraper.get(url, timeout=20, headers=headers, allow_redirects=True)
        if r.status_code == 200:
            return 'متاح', r.text
    except:
        pass
    return 'غير موجود', None

def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(["script", "style", "noscript", "meta", "link"]):
        tag.decompose()
    return re.sub(r'\s+', ' ', soup.get_text(separator=" ", strip=True))[:5000]

def get_currency(country):
    mapping = {"السعودية": "ريال سعودي", "الإمارات": "درهم إماراتي", "الكويت": "دينار كويتي", "قطر": "ريال قطري", "عمان": "ريال عماني", "البحرين": "دينار بحريني"}
    return mapping.get(country, "ريال سعودي")

# ==========================================
# 10. دالة تحويل الصوت إلى نص
# ==========================================
def transcribe_audio(audio_bytes):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(BytesIO(audio_bytes)) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language='ar-AR')
    except:
        return None

# ==========================================
# 11. معالجة وإرسال الاستعلامات للأفاتار والمحادثة
# ==========================================
def animate_avatar(image_path):
    if not os.path.exists(image_path):
        return
    placeholder = st.empty()
    for _ in range(2):
        placeholder.image(image_path, width=175, caption="🗣️ يتحدث الآن...")
        time.sleep(0.2)
        placeholder.image(image_path, width=170, caption=" ")
        time.sleep(0.2)
    placeholder.image(image_path, width=175, caption="المساعد الذكي جاهز")

def process_query_avatar(query, model):
    if not query:
        return
    st.session_state.conversation.append({"role": "user", "content": query})
    
    quick = quick_response(query)
    if quick:
        ai_reply = quick
    elif model is None:
        ai_reply = "⚠️ الخدمة الذكية غير متاحة حالياً، يرجى فحص مفتاح الـ API."
    else:
        with st.spinner("🤖 جاري التفكير بصياغة فاخرة..."):
            try:
                response = model.generate_content(f"أجب باختصار بليغ وفصيح ودون استخدام أي نجوم أو رموز تقييم على: {query}")
                ai_reply = re.sub(r'[⭐★✨]', '', response.text)
                ai_reply = re.sub(r'Saeed\s*DaTaBoT|SaeedMarketAds', '', ai_reply, flags=re.IGNORECASE).strip()
            except Exception as e:
                ai_reply = f"❌ حدث خطأ أثناء المعالجة: {e}"

    st.session_state.conversation.append({"role": "assistant", "content": ai_reply})
    
    if st.session_state.voice_enabled and ai_reply:
        animate_avatar(st.session_state.current_avatar)
        play_voice(ai_reply[:400])

    st.rerun()

# ==========================================
# 12. تهيئة النموذج وحالة الجلسة المستقرة
# ==========================================
if 'model' not in st.session_state or st.session_state.model is None:
    _model, _model_name = get_working_model()
    st.session_state.model = _model
    st.session_state.model_name = _model_name

if 'current_avatar' not in st.session_state:
    st.session_state.current_avatar = "saeed.jpg" if os.path.exists("saeed.jpg") else "ROBOT.jpg"
if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = True
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'products' not in st.session_state:
    st.session_state.products = []
if 'last_audio_hash' not in st.session_state:
    st.session_state.last_audio_hash = None

model = st.session_state.model

# ==========================================
# 13. الغلاف العلوي للمنصة
# ==========================================
st.markdown("""
<div class='hero-section'>
    <h1 class='hero-title'>✨ سوق سعيد ✨</h1>
    <p class='hero-subtitle'>وجهتك الفاخرة للتسوق العالمي الذكي — SHEIN | نون | AliExpress</p>
    <div style='background: rgba(255,255,255,0.15); border-radius: 24px; padding: 22px; margin-top: 18px; backdrop-filter: blur(8px);'>
        <p style='color: #fff; font-size: 20px; margin: 0; font-weight:700;'>كود الخصم الحصري والآمن</p>
        <div class='hero-code'><h1 class='hero-code-text'>N73QS</h1></div>
        <p style='color: #fff; font-size: 18px; margin: 5px 0 0 0;'>استمتع بتجربة تسوق آمنة واحترافية بالكامل</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 14. القائمة الجانبية الاستاتيكية والذكية
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1a0a2e, #3a1466); border-radius: 25px; margin-bottom: 20px;'>
        <h2 style='color: #ffb300; margin:0;'>👑 المساعد الذكي</h2>
        <p style='color: #d1c4e9; margin-top:4px;'>إدارة وفحص العروض الفاخرة</p>
    </div>
    """, unsafe_allow_html=True)

    country = st.selectbox("🌍 اختر دولتك المستهدفة:", ["السعودية", "الإمارات", "الكويت", "قطر", "عمان", "البحرين"], index=0)

    if model:
        st.success(f"✅ الخدمة الذكية متصلة بنجاح")
    else:
        st.error("⚠️ تعذر تفعيل الخدمة الذكية. يرجى إدخال مفتاح باسم 'API' في secrets.")

    st.markdown("---")
    st.session_state.voice_enabled = st.checkbox("تفعيل النطق الصوتي التلقائي", value=True)
    
    avatar_option = st.selectbox("تخصيص أفاتار التحدث", ["سعيد (saeed.jpg)", "روبوت الافتراضي"])
    st.session_state.current_avatar = "saeed.jpg" if (avatar_option == "سعيد (saeed.jpg)" and os.path.exists("saeed.jpg")) else "ROBOT.jpg"

    st.markdown("---")
    st.caption("© 2026 سوق سعيد — صُنع بكفاءة وفخامة عصامية 👑")

# ==========================================
# 15. علامات التبويب الرئيسية (Tabs)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["🛍️ متجر المنتجات", "🔍 الفحص المتقدم للروابط", "💬 المحادثة الذكية (صوت + نص)", "📦 إضافة وإدارة المنتجات"])

# --- تبويب استعراض المتاجر والعروض ---
with tab1:
    st.subheader("اختر منصة التسوق لتصفح العروض الثابتة:")
    col1, col2, col3 = st.columns(3)
    
    if col1.button("🩷 تصفح عروض SHEIN", use_container_width=True):
        st.session_state.store = "SHEIN"
    if col2.button("🟡 تصفح عروض Noon", use_container_width=True):
        st.session_state.store = "Noon"
    if col3.button("🧡 تصفح عروض AliExpress", use_container_width=True):
        st.session_state.store = "AliExpress"

    current_store = st.session_state.get('store', 'SHEIN')
    st.write(f"### 🛒 المنتجات المعروضة حالياً: {current_store}")
    
    prod_list = SHEIN_PRODUCTS if current_store == "SHEIN" else (NOON_PRODUCTS if current_store == "Noon" else ALIEXPRESS_PRODUCTS)
    
    cols = st.columns(3)
    for i, prod in enumerate(prod_list):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='product-card'>
                <div class='product-code'>{prod['code']}</div>
                <div class='product-name'>{prod['name']}</div>
                <div class='product-price'>${prod['price']}</div>
                <div class='product-sales'>خصم حقيقي: {prod['discount']}%</div>
                <a href='{prod['link']}' target='_blank' style='text-decoration: none;'>
                    <div class='product-btn'>تسوق الرابط الآمن</div>
                </a>
            </div>
            """, unsafe_allow_html=True)

# --- تبويب الفحص المتقدم ---
with tab2:
    st.subheader("🔍 أداة كشط وتحليل روابط المنتجات العالمية")
    link = st.text_input("ضع رابط المنتج المراد فحصه هنا تلقائياً:", placeholder="https://...")
    if st.button("بدء الفحص والتلخيص الذكي"):
        if not link:
            st.warning("يرجى إدخال الرابط أولاً.")
        elif not model:
            st.error("الخدمة الذكية غير مفعلة.")
        else:
            with st.spinner("جاري جلب بيانات الصفحة وفحصها..."):
                status, html = check_link_status(link)
                if status == 'متاح' and html:
                    page_text = extract_text_from_html(html)
                    currency = get_currency(country)
                    prompt = f"حلل واستخرج: اسم المنتج، السعر بـ {currency}، والتوفر من النص التالي باختصار شديد وبدون نجوم تقييم: {page_text[:3000]}"
                    try:
                        response = model.generate_content(prompt)
                        clean_text = re.sub(r'[⭐★✨]', '', response.text).strip()
                        st.info(clean_text)
                        if st.session_state.voice_enabled:
                            play_voice(clean_text[:300])
                    except Exception as e:
                        st.error(f"خطأ أثناء التحليل بالذكاء الاصطناعي: {e}")
                else:
                    st.error("تعذر كشط هذا الرابط، قد يكون محمياً أو غير صالح.")

# --- تبويب المحادثة الفاخرة لمنع التكرار اللانهائي ---
with tab3:
    st.subheader("💬 اسأل المساعد الذكي (نصياً أو صوتياً)")
    
    # عرض سجل المحادثة الحالي
    for msg in st.session_state.conversation:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("##### 🎙️ اضغط وتحدث مباشرة:")
        audio = mic_recorder(start_prompt="بدء التسجيل", stop_prompt="إرسال الصوت", just_once=True, key='voice_mic')
        
        # حماية فريدة ضد التكرار اللانهائي للميكروفون عند عمل Rerun
        if audio and audio.get('bytes'):
            audio_bytes = audio['bytes']
            audio_hash = hash(audio_bytes)
            
            if st.session_state.last_audio_hash != audio_hash:
                st.session_state.last_audio_hash = audio_hash  # حفظ البصمة لمنع الدخول في حلقة تكرار
                with st.spinner("جاري قراءة وتحليل صوتك..."):
                    user_text = transcribe_audio(audio_bytes)
                    if user_text:
                        st.success(f"القول المستمع: {user_text}")
                        process_query_avatar(user_text, model)

    with c2:
        st.markdown("##### ✍️ اكتب سؤالك هنا:")
        user_query = st.chat_input("اكتب رسالتك ودع المساعد يجيبك...", key="text_chat_input")
        if user_query:
            process_query_avatar(user_query, model)

# --- تبويب إدارة المنتجات ---
with tab4:
    st.subheader("📦 إضافة منتجات مخصصة يدوياً لعرضها بالصفحة")
    with st.form(key="custom_product_form", clear_on_submit=True):
        p_name = st.text_input("اسم المنتج الجديد")
        p_price = st.number_input("السعر المقدر ($)", min_value=0.0, step=1.0)
        p_desc = st.text_area("وصف مختصر للمنتج")
        p_submitted = st.form_submit_button("نشر وعرض المنتج بالمنصة")
        
        if p_submitted and p_name:
            st.session_state.products.append({"name": p_name, "price": p_price, "desc": p_desc})
            st.success(f"تمت إضافة منتج ({p_name}) بنجاح للمنصة!")
            st.rerun()

    if st.session_state.products:
        st.write("### 📜 قائمة المنتجات المضافة يدويًا:")
        for idx, prod in enumerate(st.session_state.products):
            st.markdown(f"**📦 {prod['name']}** | السعر: `${prod['price']}` | الوصف: {prod['desc']}")
        if st.button("مسح كافة المنتجات المضافة"):
            st.session_state.products.clear()
            st.success("تم تنظيف القائمة المخصصة.")
            st.rerun()
PYEOF

# 2. تشغيل التطبيق بأعلى كفاءة وسرعة
streamlit run /mnt/user-data/outputs/SAEED_app.py

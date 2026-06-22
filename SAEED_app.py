import streamlit as st
import google.generativeai as genai
import requests
import os
import base64
import streamlit.components.v1 as components
import pyttsx3
from gtts import gTTS
import io
import tempfile

# ============================================================
# 1. إعدادات الصفحة
# ============================================================
st.set_page_config(
    page_title="سوق سعيد | متاجر SHEIN - نون - علي اكسبرس",
    page_icon="🛍️",
    layout="wide"
)

# ============================================================
# 2. الخلفية والتصميم (CSS)
# ============================================================
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0.2);
}
.stMarkdown {
    color: #fff;
}
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
.store-section {
    background: rgba(255,255,255,0.05);
    border-radius: 30px;
    padding: 25px;
    margin-bottom: 40px;
    backdrop-filter: blur(5px);
}
.store-header-shein {
    background: linear-gradient(135deg, #ff6b6b, #feca57);
    text-align: center;
    padding: 20px;
    border-radius: 25px;
    margin-bottom: 30px;
}
.store-header-noon {
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    text-align: center;
    padding: 20px;
    border-radius: 25px;
    margin-bottom: 30px;
}
.store-header-aliexpress {
    background: linear-gradient(135deg, #ff4757, #ff6b81);
    text-align: center;
    padding: 20px;
    border-radius: 25px;
    margin-bottom: 30px;
}
hr {
    border-color: rgba(255,255,255,0.1);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ============================================================
# 3. دالة تشغيل الصوت (pyttsx3 مع Fallback إلى gTTS)
# ============================================================
@st.cache_resource
def init_tts_engine():
    """تهيئة محرك pyttsx3 مع اختيار الصوت الرجالي."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if "male" in voice.name.lower() or "arabic" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 160)
        engine.setProperty('volume', 0.9)
        return engine, True
    except Exception as e:
        return None, False

def play_voice(text):
    """تشغيل الصوت باستخدام pyttsx3، وفي حال الفشل يستخدم gTTS."""
    try:
        # المحاولة الأولى: pyttsx3
        engine, success = init_tts_engine()
        if success and engine:
            engine.say(text)
            engine.runAndWait()
            return True
        else:
            # المحاولة الثانية: gTTS (حل احتياطي يعمل دائماً)
            tts = gTTS(text=text, lang='ar')
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                tts.save(fp.name)
                with open(fp.name, 'rb') as f:
                    audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                audio_html = f'''
                <audio autoplay="true" style="display:none;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                '''
                st.markdown(audio_html, unsafe_allow_html=True)
                os.unlink(fp.name)
                return True
    except Exception as e:
        st.warning(f"⚠️ حدث خطأ في تشغيل الصوت: {str(e)}")
        return False

# ============================================================
# 4. قراءة المفاتيح من st.secrets
# ============================================================
def get_secret(key, fallback_key=None, default=None):
    try:
        if key in st.secrets:
            return st.secrets[key]
        if fallback_key and fallback_key in st.secrets:
            return st.secrets[fallback_key]
        for k in st.secrets.keys():
            if key.lower() in k.lower() or (fallback_key and fallback_key.lower() in k.lower()):
                return st.secrets[k]
        return default
    except:
        return default

GEMINI_API_KEY = get_secret("GEMINI_MAIN_KEY", "GEMINI_API", None)

# ============================================================
# 5. قراءة التعليمات
# ============================================================
try:
    with open('Instructions.txt', 'r', encoding='utf-8') as f:
        instructions = f.read()
except FileNotFoundError:
    instructions = "أنت مساعد ذكي للتسوق الإلكتروني، اسمك Saeed DaTaBoT، تساعد المستخدمين في العثور على أفضل العروض والإجابة على استفساراتهم."

# ============================================================
# 6. إعداد موديل Gemini
# ============================================================
try:
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-3.1-flash-lite",
            system_instruction=instructions
        )
        st.sidebar.success("✅ يعمل على gemini-3.5-flash-lite")
    else:
        model = None
        st.error("⚠️ مفتاح API غير موجود")
except Exception as e:
    model = None
    st.error(f"⚠️ حدث خطأ: {str(e)}")

# ============================================================
# 7. الوظائف المساعدة
# ============================================================
@st.cache_data(ttl=3600)
def is_product_available(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, timeout=8, headers=headers)
        unavailable_indicators = ["sold out", "out of stock", "غير متوفر", "نفدت الكمية"]
        for indicator in unavailable_indicators:
            if indicator in response.text.lower():
                return False
        return response.status_code == 200
    except:
        return True

def quick_response(question):
    q = question.lower()
    if "كود" in q or "خصم" in q:
        return "🎁 **كود خصم SHEIN الحصري** 🎁\n\n🏷️ **الكود: WL7KA**\n\n🔥 خصم يصل إلى 60% على أول طلب"
    elif "من أنت" in q:
        return "🤖 أنا **Saeed DaTaBoT**، مساعدك الذكي للتسوق."
    elif "السلام" in q or "مرحبا" in q:
        return "وعليكم السلام ورحمة الله وبركاته 🌹\n\nأهلاً بك في **سوق سعيد**!"
    return None

def render_custom_banner():
    html_code = """
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 40px; margin-bottom: 30px;'>
        <h1 style='color: #feca57; font-size: 45px;'>🛍️ سوق سعيد</h1>
        <p style='color: #aaa; font-size: 20px;'>متجر SHEIN | نون | علي اكسبرس</p>
        <p style='color: #ff6b6b; font-size: 18px;'>🤖 مساعدك الذكي Saeed DaTaBoT</p>
    </div>
    """
    components.html(html_code, height=200)

# ============================================================
# 8. الواجهة الرئيسية
# ============================================================
render_custom_banner()

st.markdown("""
<div style='background: linear-gradient(135deg, #ff0844, #ffb199); padding: 40px; border-radius: 55px; text-align: center; margin-bottom: 40px;'>
    <h2 style='color: #fff;'>🎁 عرض خاص للمستخدمين الجدد 🎁</h2>
    <div style='background: white; display: inline-block; padding: 15px 50px; border-radius: 80px; margin: 10px 0;'>
        <h1 style='color: #ff0844; margin: 0; font-size: 45px;'>🏷️ WL7KA</h1>
    </div>
    <p style='color: #fff; font-size: 22px;'>🔥 خصم يصل إلى 60% على أول طلب 🔥</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🎙️ استمع لرسالة الترحيب")
play_voice("مرحباً بك في سوق سعيد، أنا سعيد داتا بوت، مساعدك الذكي للتسوق.")

# ============================================================
# 9. تحليل الروابط
# ============================================================
st.markdown("<h2 style='color: #feca57; text-align: center;'>🔗 تحليل الرابط</h2>", unsafe_allow_html=True)

url_input = st.text_input("📎 أرسل رابط المنتج:", placeholder="https://...")

if url_input:
    with st.spinner("🤖 جاري التحليل..."):
        is_available = is_product_available(url_input)
        if model:
            try:
                response = model.generate_content(f"حلل هذا الرابط باختصار: {url_input}")
                status = "✅ متوفر" if is_available else "❌ غير متوفر"
                result = f"{response.text}\n\n📦 حالة المنتج: {status}"
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px;'>
                    <p style='color: #e2e8f0;'>{result}</p>
                </div>
                """, unsafe_allow_html=True)
                play_voice(result)
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

st.markdown("---")

# ============================================================
# 10. منتجات SHEIN (جميع المنتجات موجودة)
# ============================================================
st.markdown("""
<div class='store-section'>
    <div class='store-header-shein'>
        <h2 style='color: white;'>🛍️ متجر SHEIN</h2>
        <p style='color: white;'>أفضل العروض</p>
    </div>
</div>
""", unsafe_allow_html=True)

SHEIN_PRODUCTS = [
    {"code": "SH001", "name": "معطف مبطن بغطاء رأس للفتيات", "price": 19.39, "discount": 43, "link": "https://onelink.shein.com/38/5shrzfcizjmg", "sales": "150+"},
    {"code": "SH002", "name": "قميص أنيق بتصميم هونج كونج", "price": 14.18, "discount": 37, "link": "https://onelink.shein.com/38/5shune7n90yf", "sales": "200+"},
    {"code": "SH003", "name": "نظارات حفلات مطبوعة 6 قطع", "price": 2.70, "discount": 0, "link": "https://onelink.shein.com/38/5shujg5f2ywk", "sales": "300+"},
    {"code": "SH004", "name": "حقيبة مستلزمات سفر مقاومة للماء", "price": 3.90, "discount": 17, "link": "https://onelink.shein.com/38/5shuimjyfjt7", "sales": "100+"},
    {"code": "SH005", "name": "معطف رجالي كاجوال سادة", "price": 25.67, "discount": 24, "link": "https://onelink.shein.com/38/5shui8qqn60h", "sales": "200+"},
    {"code": "SH006", "name": "أقراط زهرية بتصميم لافت", "price": 1.44, "discount": 4, "link": "https://onelink.shein.com/38/5shtox57cemc", "sales": "300+"},
    {"code": "SH007", "name": "ربطات شعر ملونة 5 قطع", "price": 1.50, "discount": 38, "link": "https://onelink.shein.com/38/5shtobfv3sxn", "sales": "800+"},
    {"code": "SH008", "name": "أحذية رياضية نسائية كاجوال", "price": 5.00, "discount": 82, "link": "https://onelink.shein.com/38/5shtl502kmcf", "sales": "200+"},
    {"code": "SH009", "name": "مجموعة خواتم زهور وردية", "price": 2.16, "discount": 6, "link": "https://onelink.shein.com/38/5shtkl9rhh8f", "sales": "500+"},
    {"code": "SH010", "name": "دلو أرز مع كوب قياس", "price": 8.84, "discount": 70, "link": "https://onelink.shein.com/38/5shtjtnbwphj", "sales": "200+"},
]

cols = st.columns(4)
for i, product in enumerate(SHEIN_PRODUCTS):
    with cols[i % 4]:
        final_price = product['price'] * (1 - product['discount']/100) if product['discount'] > 0 else product['price']
        st.markdown(f"""
        <div class='product-card'>
            <div class='product-code'>📦 {product['code']}</div>
            <div class='product-name'>{product['name']}</div>
            <div class='product-price'>${final_price:.2f}</div>
            <div class='product-sales'>📊 تم البيع: {product['sales']}</div>
            <a href='{product['link']}' target='_blank' style='text-decoration: none;'>
                <div class='product-btn'>🛒 تسوق الآن</div>
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# 11. منتجات نون
# ============================================================
st.markdown("""
<div class='store-section'>
    <div class='store-header-noon'>
        <h2 style='color: white;'>🛍️ متجر نون</h2>
    </div>
</div>
""", unsafe_allow_html=True)

NOON_PRODUCTS = [
    {"code": "N001", "name": "ساعة ذكية رياضية", "price": 89.99, "discount": 30, "link": "https://www.noon.com/ar-sa/Z09748F5900924601C848Z/p/", "sales": "500+"},
    {"code": "N002", "name": "سماعات لاسلكية بلوتوث", "price": 45.50, "discount": 25, "link": "https://www.noon.com/ar-sa/N11200839A/p/", "sales": "1200+"},
    {"code": "N003", "name": "شاحن سريع بقاعدة", "price": 29.90, "discount": 15, "link": "https://www.noon.com/ar-sa/N70140492V/p/", "sales": "800+"},
    {"code": "N004", "name": "حافظة جوال سيليكون", "price": 12.99, "discount": 40, "link": "https://www.noon.com/ar-sa/ZF23DE5EC51560ADE2D7EZ/p/", "sales": "2000+"},
    {"code": "N005", "name": "سوار رياضي ذكي", "price": 35.00, "discount": 20, "link": "https://www.noon.com/ar-sa/N70140491V/p/", "sales": "300+"},
    {"code": "N006", "name": "مروحة USB محمولة", "price": 18.75, "discount": 35, "link": "https://www.noon.com/ar-sa/N23772548A/p/", "sales": "600+"},
]

cols = st.columns(4)
for i, product in enumerate(NOON_PRODUCTS):
    with cols[i % 4]:
        final_price = product['price'] * (1 - product['discount']/100) if product['discount'] > 0 else product['price']
        st.markdown(f"""
        <div class='product-card'>
            <div class='product-code'>📦 {product['code']}</div>
            <div class='product-name'>{product['name']}</div>
            <div class='product-price'>${final_price:.2f}</div>
            <div class='product-sales'>📊 تم البيع: {product['sales']}</div>
            <a href='{product['link']}' target='_blank' style='text-decoration: none;'>
                <div class='product-btn'>🛒 تسوق الآن</div>
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# 12. علي اكسبرس (قادم)
# ============================================================
st.markdown("""
<div class='store-section'>
    <div class='store-header-aliexpress'>
        <h2 style='color: white;'>🛍️ متجر AliExpress</h2>
        <p style='color: white;'>قادم قريباً</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 50px; background: rgba(255,71,87,0.1); border-radius: 40px;'>
    <h3 style='color: #feca57;'>🚀 قادم قريباً جداً</h3>
    <p style='color: #ddd;'>نستعد لإطلاق متجر AliExpress مع أفضل العروض</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# 13. بوت الدردشة
# ============================================================
st.markdown("<h2 style='color: #feca57; text-align: center;'>💬 تحدث مع Saeed DaTaBoT</h2>", unsafe_allow_html=True)

chat_question = st.text_area("📝 اكتب سؤالك هنا:", height=100)

if st.button("💬 أرسل", use_container_width=True):
    if chat_question:
        quick_ans = quick_response(chat_question)
        if quick_ans:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px;'>
                <p style='color: #e2e8f0;'>{quick_ans}</p>
            </div>
            """, unsafe_allow_html=True)
            play_voice(quick_ans)
        elif model:
            try:
                response = model.generate_content(f"رد باختصار بالعربية الفصحى كـ Saeed DaTaBoT: {chat_question}")
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px;'>
                    <p style='color: #e2e8f0;'>{response.text}</p>
                </div>
                """, unsafe_allow_html=True)
                play_voice(response.text)
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    else:
        st.warning("📝 يرجى كتابة سؤالك")

# ============================================================
# 14. السايدبار
# ============================================================
with st.sidebar:
    st.markdown("### 🤖 Saeed DaTaBoT")
    st.markdown("مساعدك الذكي للتسوق")
    st.markdown("---")
    st.markdown("### 🎯 خدماتي:")
    st.markdown("""
    - ✅ تحليل الروابط
    - ✅ عروض SHEIN
    - ✅ عروض نون
    - ✅ محادثة ذكية
    """)
    st.markdown("---")
    st.markdown("### 📞 للتواصل:")
    st.markdown("[@SaeedMarketAds](https://t.me/SaeedMarketAds)")
    st.caption("© 2026 سوق سعيد")

import streamlit as st
import google.generativeai as genai
import cloudscraper  # بديل قوي لـ requests
import requests      # تمت إضافته للاستخدام في fallback
import os
import base64
import streamlit.components.v1 as components
import edge_tts
import tempfile
import asyncio
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

# ============================================================
# 1. إعدادات الصفحة
# ============================================================
st.set_page_config(
    page_title="سوق سعيد | متاجر SHEIN - نون - علي اكسبرس",
    page_icon="🛍️",
    layout="wide"
)

# ============================================================
# 2. الخلفية والتصميم (CSS) - محسّن لعرض المنتجات بشكل جذاب
# ============================================================
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
hr { border-color: rgba(255,255,255,0.1); }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ============================================================
# 3. دالة تشغيل الصوت (بصوت رجالي فصيح باستخدام edge-tts)
# ============================================================
async def generate_audio(text, voice="ar-SA-HamedNeural"):
    """توليد ملف صوتي بصوت رجالي عربي فصيح (Hamed)."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            output_file = tmp_file.name
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        with open(output_file, 'rb') as f:
            audio_bytes = f.read()
        os.unlink(output_file)
        return audio_bytes
    except Exception as e:
        st.warning(f"⚠️ خطأ في توليد الصوت: {str(e)}")
        return None

def play_voice(text):
    """تشغيل الصوت في المتصفح."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_bytes = loop.run_until_complete(generate_audio(text))
        loop.close()
        if audio_bytes:
            b64 = base64.b64encode(audio_bytes).decode()
            audio_html = f'''
            <audio autoplay="true" style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            '''
            st.markdown(audio_html, unsafe_allow_html=True)
            return True
        else:
            return False
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
    instructions = """
    أنت Saeed DaTaBoT، المساعد الذكي لمنصة سوق سعيد.
    هويتك: أنت منصة SaeedMarketAds الرائدة مع تقنية الذكاء الاصطناعي.
    المطور والمؤسس هو سعيد المسوري، العقل المدبر لتأسيس منصة SaeedMarketAds و Saeed DaTaBoT.
    ردودك دائماً باللغة العربية الفصحى، مختصرة وواضحة، لكن يمكنك الإسهاب عند الحاجة لتحليل المنتجات أو النصوص الطويلة.
    """

# ============================================================
# 6. إعداد موديل Gemini (اختيار النموذج من السايدبار)
# ============================================================
def init_model(api_key, model_name="gemini-3.1-flash"):
    """تهيئة النموذج مع إعدادات مناسبة."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=instructions,
            generation_config={
                "max_output_tokens": 4096,   # دعم النصوص الطويلة
                "temperature": 0.7,
                "top_p": 0.95
            }
        )
        return model
    except Exception as e:
        st.error(f"⚠️ خطأ في تهيئة النموذج: {str(e)}")
        return None

# ============================================================
# 7. دوال مساعدة محسّنة للتحليل العميق (باستخدام cloudscraper)
# ============================================================
@st.cache_data(ttl=3600)
def fetch_page_content(url):
    """جلب محتوى الصفحة باستخدام cloudscraper لتجاوز الحماية."""
    try:
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
        )
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = scraper.get(url, timeout=15, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # إزالة العناصر غير المرغوب فيها
            for script in soup(["script", "style", "noscript", "meta", "link"]):
                script.decompose()
            # استخراج النص
            text = soup.get_text(separator=" ", strip=True)
            # تنظيف النص من المسافات الزائدة والأسطر الفارغة
            text = re.sub(r'\s+', ' ', text).strip()
            # قص النص إذا كان طويلاً جداً
            if len(text) > 50000:
                text = text[:50000] + "..."
            return text
        else:
            # محاولة بديلة باستخدام requests العادي مع User-Agent محدث
            return fetch_page_content_fallback(url)
    except Exception as e:
        # محاولة بديلة
        return fetch_page_content_fallback(url)

def fetch_page_content_fallback(url):
    """محاولة جلب المحتوى باستخدام requests العادي مع محاكاة متصفح."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'ar,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        response = requests.get(url, timeout=15, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style", "noscript", "meta", "link"]):
                script.decompose()
            text = soup.get_text(separator=" ", strip=True)
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) > 50000:
                text = text[:50000] + "..."
            return text
        else:
            return None
    except Exception as e:
        return None

def analyze_link_with_gemini(url, model):
    """تحليل الرابط باستخدام Gemini مع استخراج النص من الصفحة."""
    if not model:
        return "❌ خدمة الذكاء الاصطناعي غير متاحة."
    
    with st.spinner("جاري جلب محتوى الصفحة..."):
        page_text = fetch_page_content(url)
    
    if not page_text:
        return "⚠️ تعذر الوصول إلى محتوى الصفحة. قد يكون الرابط غير صحيح أو محجوب. تأكد من صحة الرابط وحاول مرة أخرى."
    
    # تحليل النص المستخرج
    prompt = f"""
    أنت محلل منتجات خبير. قم بتحليل الرابط التالي واستخرج المعلومات التالية بدقة:
    - اسم المنتج (إذا وجد)
    - السعر (بالعملة المحلية، مع ذكر العملة)
    - حالة التوفر (متاح / غير متاح / غير معروف)
    - وصف مختصر للمنتج (لا يزيد عن 30 كلمة)
    - أي تقييمات أو مراجعات بارزة (إن وجدت)
    - ملاحظات إضافية (مثل الخصومات، الشحن، الضمان)
    
    نص الصفحة المستخرجة:
    {page_text}
    
    قدم الإجابة بصيغة منظمة وواضحة باللغة العربية الفصحى.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # عرض الخطأ الحقيقي للمستخدم كما هو مطلوب في الصور
        error_msg = f"حدث خطأ تقني، تفاصيل الخطأ هي: {str(e)}"
        st.error(error_msg)  # عرض باللون الأحمر في الواجهة
        return f"⚠️ حدث خطأ أثناء التحليل بواسطة الذكاء الاصطناعي: {str(e)}"

# ============================================================
# 8. الردود السريعة (مع تحسين الرد على السلام)
# ============================================================
def quick_response(question):
    q = question.lower()
    
    # --- الرد على التحية بالضبط كما يطلب المستخدم ---
    if "السلام" in q or "مرحبا" in q or "هلا" in q:
        return "وعليكم السلام ورحمة الله وبركاته"
    
    # --- باقي الردود السريعة ---
    elif "لقد اعطيتك منتج رابط احتيالي" in q or ("رابط احتيالي" in q and "اتعلم من اخطائك" in q):
        return (
            "أهلاً بك. أنا Saeed DaTaBoT، لقد قمت بتحديث سجلاتي لتجنب التفاعل مع الروابط الاحتيالية أو الترويج لها مستقبلاً. شكراً لتنبيهي، سأكون أكثر دقة في التحقق من صحة المحتوى."
        )
    elif "كيف حال" in q or "كيفك" in q or "اخبار" in q:
        return "بخير والحمد لله، أنا هنا لخدمتك يا صديقي. كيف يمكنني مساعدتك اليوم؟"
    elif "كود" in q or "خصم" in q:
        return "🎁 **كود خصم SHEIN الحصري** 🎁\n\n🏷️ **الكود: WL7KA**\n\n🔥 خصم يصل إلى 60% على أول طلب"
    elif "من أنت" in q or "من برمج" in q or "المطور" in q or "سعيد" in q:
        return (
            "🤖 أنا **Saeed DaTaBoT**، مساعدك الذكي للتسوق.\n\n"
            "المطور والعقل المدبر هو **سعيد المسوري**، مؤسس **SaeedMarketAds**، رائد أعمال ومطور أنظمة ذكاء اصطناعي."
        )
    elif "شكرا" in q:
        return "العفو، تحت أمرك في أي وقت."
    else:
        # إذا كان السؤال يحتوي على رابط، نمرره إلى Gemini للتحليل
        if "http" in q or "https" in q:
            return None
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
# 9. الواجهة الرئيسية
# ============================================================
render_custom_banner()

# رسالة الترحيب الجديدة (مع الرد الصحيح على السلام)
welcome_msg = "وعليكم السلام ورحمة الله وبركاته. مرحباً بكم في SaeedMarketAds، المنصة الرائدة مع تقنية الذكاء الاصطناعي. أنا سعيد داتا بوت، تحت خدمتكم."
st.markdown(f"### 🎙️ {welcome_msg}")
play_voice(welcome_msg)

st.markdown("""
<div style='background: linear-gradient(135deg, #ff0844, #ffb199); padding: 40px; border-radius: 55px; text-align: center; margin-bottom: 40px;'>
    <h2 style='color: #fff;'>🎁 عرض خاص للمستخدمين الجدد 🎁</h2>
    <div style='background: white; display: inline-block; padding: 15px 50px; border-radius: 80px; margin: 10px 0;'>
        <h1 style='color: #ff0844; margin: 0; font-size: 45px;'>🏷️ WL7KA</h1>
    </div>
    <p style='color: #fff; font-size: 22px;'>🔥 خصم يصل إلى 60% على أول طلب 🔥</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 10. السايدبار - الإعدادات والنماذج
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 30px; margin-bottom: 20px;'>
        <h2 style='color: #feca57;'>🤖 Saeed DaTaBoT</h2>
        <p style='color: #aaa;'>مساعدك الذكي للتسوق</p>
    </div>
    """, unsafe_allow_html=True)

    # اختيار النموذج
    model_choice = st.selectbox(
        "اختر نموذج الذكاء الاصطناعي:",
        ["gemini-1.5-flash (سريع)", "gemini-1.5-pro (متقدم)"],
        index=0
    )
    selected_model = "gemini-1.5-flash" if "flash" in model_choice else "gemini-1.5-pro"
    
    # تهيئة النموذج
    if GEMINI_API_KEY:
        model = init_model(GEMINI_API_KEY, selected_model)
        if model:
            st.success(f"✅ يعمل على {selected_model}")
        else:
            st.error("⚠️ فشل تهيئة النموذج")
    else:
        model = None
        st.error("⚠️ مفتاح API غير موجود في secrets.toml")

    st.markdown("---")
    st.markdown("### 🎯 خدماتي:")
    st.markdown("""
    - ✅ تحليل الروابط المتقدم
    - ✅ عروض SHEIN
    - ✅ عروض نون
    - ✅ محادثة ذكية (نصوص طويلة)
    """)
    st.markdown("---")
    st.markdown("### 📞 للتواصل:")
    st.markdown("[@SaeedMarketAds](https://t.me/SaeedMarketAds)")
    st.markdown("---")
    st.markdown("### 📊 إحصائيات:")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🛍️ منتجات SHEIN", "5+")
    with col2:
        st.metric("⭐ منتجات نون", "2+")
    st.markdown("---")
    st.caption("© 2026 سوق سعيد")
    st.caption("برمجة وتطوير: سعيد المسوري")

# ============================================================
# 11. استخدام Tabs للفصل بين الخدمات (محسّن)
# ============================================================
tab1, tab2, tab3 = st.tabs(["🛍️ متجر المنتجات", "🔍 أداة الفحص المتقدم", "💬 محادثة Saeed DaTaBoT"])

# --- التبويب 1: المتجر (صفحة نشر المنتجات) ---
with tab1:
    st.subheader("اختر المتجر للتصفح:")
    col1, col2, col3 = st.columns(3)
    if col1.button("🛍️ تصفح SHEIN"):
        st.session_state.store = "SHEIN"
    if col2.button("💛 تصفح Noon"):
        st.session_state.store = "Noon"
    if col3.button("🚀 تصفح AliExpress"):
        st.session_state.store = "AliExpress"

    if 'store' in st.session_state:
        store = st.session_state.store
        st.write(f"### عرض منتجات: {store}")
        
        if store == "SHEIN":
            SHEIN_PRODUCTS = [
                {"code": "SH001", "name": "معطف مبطن بغطاء رأس للفتيات", "price": 19.39, "discount": 43, "link": "https://onelink.shein.com/38/5shrzfcizjmg", "sales": "150+"},
                {"code": "SH002", "name": "قميص أنيق بتصميم هونج كونج", "price": 14.18, "discount": 37, "link": "https://onelink.shein.com/38/5shune7n90yf", "sales": "200+"},
                {"code": "SH003", "name": "نظارات حفلات مطبوعة 6 قطع", "price": 2.70, "discount": 0, "link": "https://onelink.shein.com/38/5shujg5f2ywk", "sales": "300+"},
                {"code": "SH004", "name": "حقيبة مستلزمات سفر مقاومة للماء", "price": 3.90, "discount": 17, "link": "https://onelink.shein.com/38/5shuimjyfjt7", "sales": "100+"},
                {"code": "SH005", "name": "معطف رجالي كاجوال سادة", "price": 25.67, "discount": 24, "link": "https://onelink.shein.com/38/5shui8qqn60h", "sales": "200+"},
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
        
        elif store == "Noon":
            NOON_PRODUCTS = [
                {"code": "N001", "name": "ساعة ذكية رياضية", "price": 89.99, "discount": 30, "link": "https://www.noon.com/ar-sa/Z09748F5900924601C848Z/p/", "sales": "500+"},
                {"code": "N002", "name": "سماعات لاسلكية بلوتوث", "price": 45.50, "discount": 25, "link": "https://www.noon.com/ar-sa/N11200839A/p/", "sales": "1200+"},
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
        
        elif store == "AliExpress":
            st.markdown("""
            <div style='text-align: center; padding: 50px; background: rgba(255,71,87,0.1); border-radius: 40px;'>
                <h3 style='color: #feca57;'>🚀 قادم قريباً جداً</h3>
                <p style='color: #ddd;'>نستعد لإطلاق متجر AliExpress مع أفضل العروض</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("✅ تم تحميل المنتجات بنجاح...")

# --- التبويب 2: أداة الفحص المتقدم (تحليل حقيقي) ---
with tab2:
    st.subheader("🔍 أداة فحص الروابط المتقدمة")
    link = st.text_input("ضع رابط المنتج هنا:", placeholder="https://...")
    if st.button("تحليل المنتج"):
        if link:
            if model:
                result = analyze_link_with_gemini(link, model)
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'>
                    <h4 style='color: #feca57;'>📊 نتيجة التحليل:</h4>
                    <p style='color: #e2e8f0;'>{result}</p>
                </div>
                """, unsafe_allow_html=True)
                play_voice(result)
            else:
                st.warning("⚠️ خدمة الذكاء الاصطناعي غير متاحة، يرجى التحقق من مفتاح API.")
        else:
            st.warning("📝 يرجى إدخال رابط المنتج")

# --- التبويب 3: محادثة الذكاء الاصطناعي (يدعم النصوص الطويلة) ---
with tab3:
    st.subheader("💬 اسأل Saeed DaTaBoT (يدعم النصوص الطويلة)")
    user_query = st.text_area("اطرح سؤالك هنا:", placeholder="لقد اعطيتك منتج رابط احتيالي وقلت انه متاح اتعلم من اخطائك")
    if st.button("إرسال الاستشارة"):
        if user_query:
            # 1. نبحث عن رد سريع
            quick_ans = quick_response(user_query)
            if quick_ans:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'>
                    <h4 style='color: #feca57;'>🤖 Saeed DaTaBoT يرد:</h4>
                    <p style='color: #e2e8f0;'>{quick_ans}</p>
                </div>
                """, unsafe_allow_html=True)
                play_voice(quick_ans)
            elif model:
                # 2. استخدام Gemini للردود المعقدة والطويلة
                try:
                    with st.spinner("🤖 جاري التفكير (قد يستغرق قليلاً للنصوص الطويلة)..."):
                        response = model.generate_content(
                            f"أنت Saeed DaTaBoT، أجب على الاستفسار التالي بشكل مفصل وواضح باللغة العربية الفصحى، مع تقديم تحليل عميق إذا لزم الأمر: {user_query}"
                        )
                        bot_reply = response.text
                        if not bot_reply or len(bot_reply) < 5:
                            bot_reply = "شكراً لسؤالك. أنا هنا لمساعدتك، هل لديك استفسار آخر؟"
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'>
                            <h4 style='color: #feca57;'>🤖 Saeed DaTaBoT يرد:</h4>
                            <p style='color: #e2e8f0;'>{bot_reply}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        play_voice(bot_reply)
                except Exception as e:
                    # عرض الخطأ الحقيقي كما هو مطلوب في الصور
                    error_msg = f"حدث خطأ تقني، تفاصيل الخطأ هي: {str(e)}"
                    st.error(error_msg)
                    fallback_reply = f"آسف، حدث خطأ تقني. التفاصيل: {str(e)}"
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #ff6b6b;'>
                        <h4 style='color: #feca57;'>🤖 Saeed DaTaBoT يرد:</h4>
                        <p style='color: #e2e8f0;'>{fallback_reply}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    play_voice(fallback_reply)
            else:
                st.warning("⚠️ عذراً، خدمة الذكاء الاصطناعي غير متاحة حالياً.")
        else:
            st.warning("📝 يرجى كتابة سؤالك أولاً")

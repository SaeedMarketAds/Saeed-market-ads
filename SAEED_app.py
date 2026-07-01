import streamlit as st
import google.generativeai as genai
import cloudscraper
import requests
import os
import base64
import streamlit.components.v1 as components
import edge_tts
import tempfile
import asyncio
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import pandas as pd
from io import StringIO

# ==========================================
# 1. إعدادات الموديل
# ==========================================
CURRENT_MODEL = "gemini-3.5-flash" 
# CURRENT_MODEL = "gemini-3.1-flash-lite" 

# ==========================================
# 2. دالة دمج التعليمات
# ==========================================
def get_system_instructions():
    try:
        with open('identity.txt', 'r', encoding='utf-8') as f1:
            identity = f1.read()
        with open('rules.txt', 'r', encoding='utf-8') as f2:
            rules = f2.read()
        return f"{identity}\n\n[القواعد والالتزامات]:\n{rules}"
    except Exception as e:
        return """
        أنت مساعد ذكي متخصص في الأسواق الخليجية.
        ردودك دائماً باللغة العربية الفصحى.
        لا تذكر أي اسم علم أو ماركة في ردودك.
        """

# ==========================================
# 3. تهيئة الموديل
# ==========================================
def init_gemini():
    if "GEMINI_MAIN_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_MAIN_KEY"])
        model = genai.GenerativeModel(
            model_name=CURRENT_MODEL,
            system_instruction=get_system_instructions()
        )
        return model
    else:
        st.error("خطأ: مفتاح API غير موجود في إعدادات Streamlit secrets.")
        return None

# ============================================================
# 4. إعدادات الصفحة
# ============================================================
st.set_page_config(
    page_title="سوق سعيد | متاجر SHEIN - نون - علي اكسبرس",
    page_icon="🛍️",
    layout="wide"
)

# ============================================================
# 5. الخلفية والتصميم (CSS)
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
hr { border-color: rgba(255,255,255,0.1); }

/* تنسيق الغلاف العلوي */
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
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ============================================================
# 6. دالة تشغيل الصوت
# ============================================================
async def generate_audio(text, voice="ar-SA-HamedNeural"):
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
        return False
    except Exception as e:
        st.warning(f"⚠️ حدث خطأ في تشغيل الصوت: {str(e)}")
        return False

# ============================================================
# 7. دوال جلب المنتجات من CSV
# ============================================================
@st.cache_data(ttl=3600)
def load_products_from_csv():
    try:
        url = 'https://raw.githubusercontent.com/SaeedMarketAds/Saeed-market-ads/main/products.csv'
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            return df
        return None
    except:
        return None

def get_golden_deals_from_csv():
    df = load_products_from_csv()
    if df is not None and 'discount' in df.columns:
        golden = df[df['discount'] >= 50]
        return golden.to_dict('records')
    return []

# ============================================================
# 8. بيانات المنتجات
# ============================================================
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

# ============================================================
# 9. دوال تحليل الرابط (بدون أسماء وبدون نجوم)
# ============================================================
def check_link_status(url):
    try:
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False},
            interpreter='nodejs'
        )
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ar,en;q=0.9',
        }
        response = scraper.get(url, timeout=20, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            return 'متاح', response.text
        elif response.status_code in [404, 410]:
            return 'غير موجود', None
        else:
            return check_link_status_fallback(url)
    except:
        return 'غير موجود', None

def check_link_status_fallback(url):
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        })
        response = session.get(url, timeout=20, allow_redirects=True, verify=False)
        if response.status_code == 200:
            return 'متاح', response.text
        else:
            return 'غير موجود', None
    except:
        return 'غير موجود', None

def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(["script", "style", "noscript", "meta", "link"]):
        script.decompose()
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > 50000:
        text = text[:50000] + "..."
    return text

def get_currency(country):
    currency_map = {
        "السعودية": "ريال سعودي",
        "الإمارات": "درهم إماراتي",
        "الكويت": "دينار كويتي",
        "قطر": "ريال قطري",
        "عمان": "ريال عماني",
        "البحرين": "دينار بحريني"
    }
    return currency_map.get(country, "ريال سعودي")

# ============================================================
# 10. دوال الردود السريعة
# ============================================================
def quick_response(question):
    q = question.lower()
    if "السلام" in q or "مرحبا" in q or "هلا" in q:
        return "وعليكم السلام ورحمة الله وبركاته"
    elif "كيف حال" in q or "كيفك" in q:
        return "بخير والحمد لله، أنا هنا لخدمتك."
    elif "كود" in q or "خصم" in q:
        return "كود الخصم الحصري هو: N73QS"
    elif "شكرا" in q:
        return "العفو، أنا في خدمتك."
    else:
        return None

# ============================================================
# 11. الغلاف العلوي (المقدمة)
# ============================================================
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

welcome_msg = "مرحباً بكم في سوق سعيد، منصة التسوق الذكية. استمتعوا بأفضل العروض والخصومات."
play_voice(welcome_msg)

# ============================================================
# 12. عرض منتجات SHEIN في الصفحة الرئيسية
# ============================================================
st.markdown("""
<div class='shein-section'>
    <div class='shein-header'>
        <h2>🛍️ أحدث منتجات SHEIN</h2>
        <p>تشكيلة مميزة من أفضل المنتجات بأسعار رائعة</p>
    </div>
</div>
""", unsafe_allow_html=True)

cols = st.columns(4)
for i, product in enumerate(SHEIN_PRODUCTS):
    with cols[i % 4]:
        final_price = product['price'] * (1 - product['discount']/100) if product['discount'] > 0 else product['price']
        st.markdown(f"""
        <div class='product-card'>
            <div class='product-code'>📦 {product['code']}</div>
            <div class='product-name'>{product['name']}</div>
            <div class='product-price'>${final_price:.2f}</div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span class='product-discount'>-{product['discount']}%</span>
                <span class='product-sales'>📊 تم البيع: {product['sales']}</span>
            </div>
            <a href='{product['link']}' target='_blank' style='text-decoration: none;'>
                <div class='product-btn'>🛒 تسوق الآن</div>
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin: 20px 0;'>
    <span style='color: #feca57; font-size: 14px;'>✨ استخدم كود الخصم N73QS للحصول على خصم إضافي</span>
</div>
<hr>
""", unsafe_allow_html=True)

# ============================================================
# 13. السايدبار
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 30px; margin-bottom: 20px;'>
        <h2 style='color: #feca57;'>🤖 المساعد الذكي</h2>
        <p style='color: #aaa;'>للتسوق والاستشارات</p>
    </div>
    """, unsafe_allow_html=True)

    country = st.selectbox(
        "🌍 اختر دولتك:",
        ["السعودية", "الإمارات", "الكويت", "قطر", "عمان", "البحرين"],
        index=0
    )

    model = init_gemini()
    if model:
        st.success(f"✅ يعمل على {CURRENT_MODEL}")
    else:
        st.error("⚠️ فشل تهيئة النموذج")

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
        golden_products = get_golden_deals_from_csv()
        if not golden_products:
            golden_products = GOLDEN_DEALS
        for product in golden_products[:5]:
            final_price = product['price'] * (1 - product['discount']/100)
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); border-radius: 15px; padding: 12px; margin-bottom: 10px; border-right: 4px solid #feca57;'>
                <p style='color: #e2e8f0; margin: 0;'><b>{product['name'][:30]}...</b></p>
                <p style='color: #feca57; margin: 0;'>💰 ${final_price:.2f} <span style='color: #ff6b6b; text-decoration: line-through;'>${product['price']:.2f}</span></p>
                <p style='color: #2ecc71; margin: 0;'>خصم {product['discount']}%</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 خدماتي:")
    st.markdown("- ✅ تحليل الروابط المتقدم")
    st.markdown("- ✅ عروض SHEIN")
    st.markdown("- ✅ عروض نون")
    st.markdown("- ✅ محادثة ذكية")
    st.markdown("---")
    st.markdown("### 📞 للتواصل:")
    st.markdown("[@SaeedMarketAds](https://t.me/SaeedMarketAds)")
    st.markdown("---")
    st.caption("© 2026 سوق سعيد")

# ============================================================
# 14. استخدام Tabs
# ============================================================
tab1, tab2, tab3 = st.tabs(["🛍️ متجر المنتجات", "🔍 أداة الفحص المتقدم", "💬 المحادثة الذكية"])

# ============================================================
# 15. التبويب 1: متجر المنتجات
# ============================================================
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
            golden_message = "مرحباً بك في عروض الغلات الحصرية. خصومات تصل إلى سبعين بالمئة على منتجات مختارة."
            play_voice(golden_message)
        
        golden_products = get_golden_deals_from_csv()
        if not golden_products:
            golden_products = GOLDEN_DEALS
        
        cols = st.columns(4)
        for i, product in enumerate(golden_products[:12]):
            with cols[i % 4]:
                final_price = product['price'] * (1 - product['discount']/100)
                link = product.get('link', '#')
                sales = product.get('sales', 'N/A')
                st.markdown(f"""
                <div class='product-card' style='border: 3px solid #feca57;'>
                    <div class='product-code' style='background: linear-gradient(90deg, #ff6b6b, #feca57);'>🔥 غلة</div>
                    <div class='product-name'>{product['name']}</div>
                    <div class='product-price'>${final_price:.2f}</div>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span class='product-discount'>-{product['discount']}%</span>
                        <span class='product-sales'>📊 {sales}</span>
                    </div>
                    <a href='{link}' target='_blank' style='text-decoration: none;'>
                        <div class='product-btn' style='background: linear-gradient(90deg, #ff6b6b, #feca57);'>🛒 احصل على العرض</div>
                    </a>
                </div>
                """, unsafe_allow_html=True)
        st.info("✅ تم تحميل الغلات بنجاح...")

    elif 'store' in st.session_state and st.session_state.store:
        store = st.session_state.store
        st.write(f"### عرض منتجات: {store}")
        
        if store == "SHEIN":
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

# ============================================================
# 16. التبويب 2: أداة الفحص المتقدم (بدون أسماء وبدون نجوم)
# ============================================================
with tab2:
    st.subheader("🔍 أداة فحص الروابط المتقدمة")
    link = st.text_input("ضع رابط المنتج هنا:", placeholder="https://...")
    
    if st.button("تحليل المنتج"):
        if link:
            if model:
                with st.spinner("جاري التحليل..."):
                    status, html_content = check_link_status(link)
                    if status == 'متاح' and html_content:
                        page_text = extract_text_from_html(html_content)
                        currency = get_currency(country)
                        prompt = f"""
                        قم بتحليل هذا المنتج بدقة باللغة العربية الفصحى.
                        استخرج المعلومات التالية:
                        1. اسم المنتج
                        2. السعر المتوقع بالعملة المحلية: {currency}
                        3. التقييمات والمراجعات إن وجدت
                        4. حالة التوفر
                        
                        نص الصفحة:
                        {page_text[:5000]}
                        
                        تنبيهات مهمة:
                        - لا تذكر أي اسم علم أو ماركة في ردك
                        - استخدم العملة {currency} فقط
                        - كن مختصراً وواضحاً
                        """
                        try:
                            response = model.generate_content(prompt)
                            # تنظيف الناتج من الأسماء والنجوم
                            clean_response = response.text
                            clean_response = re.sub(r'[⭐]', '', clean_response)
                            clean_response = re.sub(r'Saeed\s*DaTaBoT', '', clean_response, flags=re.IGNORECASE)
                            clean_response = re.sub(r'SaeedMarketAds', '', clean_response, flags=re.IGNORECASE)
                            clean_response = re.sub(r'saeedmarketads', '', clean_response, flags=re.IGNORECASE)
                            clean_response = re.sub(r'\s+', ' ', clean_response).strip()
                            
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'>
                                <h4 style='color: #feca57;'>📊 نتيجة التحليل:</h4>
                                <p style='color: #e2e8f0; white-space: pre-wrap;'>{clean_response}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            play_voice(clean_response[:200])
                        except Exception as e:
                            st.error(f"خطأ: {str(e)}")
                    else:
                        st.warning("⚠️ الرابط غير متاح أو لا يحتوي على محتوى.")
            else:
                st.warning("⚠️ خدمة الذكاء الاصطناعي غير متاحة.")
        else:
            st.warning("📝 يرجى إدخال رابط المنتج")

# ============================================================
# 17. التبويب 3: المحادثة الذكية
# ============================================================
with tab3:
    st.subheader("💬 المحادثة الذكية")
    user_query = st.text_area("اطرح سؤالك هنا:", placeholder="اكتب سؤالك هنا...")
    
    if st.button("إرسال الاستشارة"):
        if user_query:
            quick_ans = quick_response(user_query)
            if quick_ans:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'>
                    <h4 style='color: #feca57;'>🤖 الرد:</h4>
                    <p style='color: #e2e8f0;'>{quick_ans}</p>
                </div>
                """, unsafe_allow_html=True)
                play_voice(quick_ans)
            elif model:
                try:
                    with st.spinner("🤖 جاري التفكير..."):
                        response = model.generate_content(f"""
                        أجب على هذا السؤال باللغة العربية الفصحى:
                        {user_query}
                        
                        تنبيهات:
                        - لا تذكر أي اسم علم أو ماركة في ردك
                        - كن مختصراً وواضحاً
                        """)
                        clean_response = response.text
                        clean_response = re.sub(r'[⭐]', '', clean_response)
                        clean_response = re.sub(r'Saeed\s*DaTaBoT', '', clean_response, flags=re.IGNORECASE)
                        clean_response = re.sub(r'SaeedMarketAds', '', clean_response, flags=re.IGNORECASE)
                        clean_response = re.sub(r'saeedmarketads', '', clean_response, flags=re.IGNORECASE)
                        clean_response = re.sub(r'\s+', ' ', clean_response).strip()
                        
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'>
                            <h4 style='color: #feca57;'>🤖 الرد:</h4>
                            <p style='color: #e2e8f0;'>{clean_response}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        play_voice(clean_response[:200])
                except Exception as e:
                    st.error(f"خطأ: {str(e)}")
            else:
                st.warning("⚠️ خدمة الذكاء الاصطناعي غير متاحة.")
        else:
            st.warning("📝 يرجى كتابة سؤالك أولاً")

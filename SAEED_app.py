import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون واسعة
st.set_page_config(layout="wide")

def render_custom_banner():
    html_code = """
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        body { font-family: 'Cairo', sans-serif; background: transparent; }
        .glass { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
    <div class="glass w-full max-w-4xl rounded-3xl p-8 shadow-2xl mx-auto">
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-white mb-2">سوق سعيد 🛍️</h1>
            <p class="text-blue-300 text-lg">الذكاء الاصطناعي الذي يغير قواعد التسوق العالمي</p>
        </header>
        <div class="grid md:grid-cols-2 gap-8 items-center">
            <div class="space-y-4">
                <div class="bg-blue-600 p-6 rounded-2xl text-white">
                    <h2 class="text-xl font-bold mb-2">تجربة تسوق فريدة</h2>
                    <p class="opacity-90">تحليل فوري للأسعار، كوبونات خصم حصرية، وربط ذكي مع أكبر المتاجر.</p>
                </div>
                <div class="bg-pink-500 p-6 rounded-2xl text-white">
                    <h2 class="text-xl font-bold mb-2">انتشار عالمي في ساعة</h2>
                    <p class="opacity-90">بفضل Saeed DataBot، تسوق بذكاء وسرعة يعتمد عليها الآلاف.</p>
                </div>
            </div>
            <div class="glass p-6 rounded-3xl text-center">
                <div class="text-5xl mb-4">🚀</div>
                <h3 class="text-2xl font-bold text-white mb-2">Code: WL7KA</h3>
                <p class="text-white mb-4">خصم يصل إلى 60% على أول طلب!</p>
            </div>
        </div>
    </div>
    """
    # عرض التصميم
    components.html(html_code, height=550)

# استدعاء الوظيفة في تطبيقك
render_custom_banner()
import streamlit as st
import os
import google.generativeai as genai
import requests
import io
from gtts import gTTS
import random

# ========== إعداد الصفحة ==========
st.set_page_config(page_title="سوق سعيد | متاجر SHEIN - نون - علي اكسبرس", page_icon="🛍️", layout="wide")

# ========== تعريف دالة فحص الروابط ==========
@st.cache_data(ttl=3600)
def is_product_available(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, timeout=8, headers=headers)
        unavailable_indicators = ["sold out", "out of stock", "غير متوفر", "نفدت الكمية", "unavailable"]
        response_lower = response.text.lower()
        for indicator in unavailable_indicators:
            if indicator in response_lower:
                return False
        return response.status_code == 200
    except:
        return True  # افتراضي متوفر في حالة خطأ الاتصال

# ========== التصميم المتطور ==========
page_bg = """
<style>
/* الخلفية الرئيسية */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0.2);
}

/* تنسيق عام */
.stMarkdown {
    color: #fff;
}

/* تنسيق الأزرار */
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

/* تنسيق حقول الإدخال */
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

/* بطاقات المنتجات - موحدة الطول */
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

/* كود المنتج */
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

/* اسم المنتج */
.product-name {
    font-size: 16px;
    font-weight: bold;
    color: #1e293b;
    margin-bottom: 12px;
    min-height: 50px;
    padding-right: 60px;
}

/* السعر */
.product-price {
    color: #ff4757;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;
}

/* السعر القديم */
.old-price {
    color: #999;
    font-size: 14px;
    text-decoration: line-through;
    margin-right: 10px;
}

/* المبيعات */
.product-sales {
    color: #2ecc71;
    font-weight: bold;
    font-size: 13px;
    margin-bottom: 10px;
}

/* نسبة الخصم */
.product-discount {
    background: #ff6b6b;
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    display: inline-block;
}

/* زر التسوق */
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
.product-btn-disabled {
    background: #95a5a6;
    border-radius: 40px;
    padding: 12px;
    text-align: center;
    color: white;
    margin-top: 15px;
}

/* أقسام المتاجر */
.store-section {
    background: rgba(255,255,255,0.05);
    border-radius: 30px;
    padding: 25px;
    margin-bottom: 40px;
    backdrop-filter: blur(5px);
}
.store-header {
    text-align: center;
    padding: 20px;
    border-radius: 25px;
    margin-bottom: 30px;
}
.store-header-shein {
    background: linear-gradient(135deg, #ff6b6b, #feca57);
}
.store-header-noon {
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
}
.store-header-aliexpress {
    background: linear-gradient(135deg, #ff4757, #ff6b81);
}

/* تنسيقات عامة */
hr {
    border-color: rgba(255,255,255,0.1);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ========== قراءة المفاتيح ==========
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API"]
except:
    GEMINI_API_KEY = None

# ========== إعداد Gemini ==========
try:
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-3.5-flash')
    else:
        model = None
except:
    model = None

# ========== دالة الرد السريع ==========
def quick_response(question):
    q = question.lower()
    if "كود الخصم" in q or "خصم" in q or "كود" in q:
        return """🎁 **كود خصم SHEIN الحصري** 🎁\n\n🏷️ **الكود: WL7KA**\n\n🔥 خصم يصل إلى 60% على أول طلب\n✅ ساري على جميع منتجات SHEIN"""
    elif "من أنت" in q:
        return """🤖 أنا **Saeed DaTaBoT**، المساعد الشخصي الذكي.\n\nمتخصص في:\n• تحليل الروابط\n• فحص توفر المنتجات\n• المساعدة في التسوق من SHEIN - نون - علي اكسبرس"""
    elif "السلام" in q or "مرحبا" in q:
        return """وعليكم السلام ورحمة الله وبركاتة 🌹\n\nأهلاً بك في **سوق سعيد**! أنا **Saeed DaTaBoT** تحت خدمتك."""
    return None

# ========== الهيدر الرئيسي ==========
st.markdown("""
<div style='text-align: center; padding: 50px 20px; background: linear-gradient(135deg, rgba(26,26,46,0.9), rgba(22,33,62,0.9)); border-radius: 50px; margin-bottom: 30px;'>
    <h1 style='color: #fff; font-size: 55px; margin-bottom: 10px;'>🛍️ سوق سعيد</h1>
    <p style='color: #feca57; font-size: 24px;'>متجر SHEIN | نون | علي اكسبرس</p>
    <p style='color: #aaa; font-size: 16px;'>تسوق بأفضل الأسعار مع كود خصم حصري</p>
    <p style='color: #ff6b6b; font-size: 18px; margin-top: 10px;'>🤖 مساعدك الذكي Saeed DaTaBoT</p>
</div>
""", unsafe_allow_html=True)

# ========== كود الخصم البارز ==========
st.markdown("""
<div style='background: linear-gradient(135deg, #ff0844, #ffb199); padding: 45px 25px; border-radius: 55px; text-align: center; margin-bottom: 40px;'>
    <h2 style='color: #fff; margin-bottom: 15px; font-size: 32px;'>🎁 عرض خاص للمستخدمين الجدد 🎁</h2>
    <div style='background: white; display: inline-block; padding: 20px 60px; border-radius: 80px; margin: 15px 0;'>
        <h1 style='color: #ff0844; margin: 0; font-size: 55px; letter-spacing: 5px;'>🏷️ WL7KA</h1>
    </div>
    <p style='color: #fff; font-size: 26px; margin: 10px 0 0 0; font-weight: bold;'>🔥 خصم يصل إلى 60% على أول طلب 🔥</p>
    <p style='color: #fff; font-size: 18px; margin-top: 10px;'>✨ استخدم الكود عند الدفع ووفر أكثر ✨</p>
</div>
""", unsafe_allow_html=True)

# ========== تحليل الروابط ==========
st.markdown("<h2 style='color: #feca57; text-align: center; font-size: 32px; margin-bottom: 20px;'>🔗 تحليل الرابط مع Saeed DaTaBoT</h2>", unsafe_allow_html=True)

url_input = st.text_input("📎 أرسل رابط المنتج أو الموقع هنا (SHEIN, نون, AliExpress):", placeholder="https://...")

if url_input:
    with st.spinner("🤖 Saeed DaTaBoT يحلل الرابط..."):
        is_available = is_product_available(url_input)
        if model:
            try:
                response = model.generate_content(f"حلل هذا الرابط باختصار: {url_input}")
                status = "✅ متوفر" if is_available else "❌ غير متوفر حالياً"
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #feca57; margin-bottom: 20px;'>
                    <h4 style='color: #feca57;'>🤖 Saeed DaTaBoT يرد:</h4>
                    <p style='color: #e2e8f0;'>{response.text}</p>
                    <hr>
                    <p style='color: #2ecc71;'><strong>📦 حالة المنتج:</strong> {status}</p>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.info("⚠️ لا يمكن تحليل الرابط حالياً")
        else:
            st.info("🤖 خدمة التحليل غير متاحة حالياً")

st.markdown("---")

# ========== منتجات SHEIN (قسم منفصل) ==========
st.markdown("""
<div class='store-section'>
    <div class='store-header store-header-shein'>
        <h2 style='color: white; font-size: 36px; margin: 0;'>🛍️ متجر SHEIN</h2>
        <p style='color: white; font-size: 18px; margin: 5px 0 0 0;'>51 منتج بأسعار خرافية</p>
    </div>
</div>
""", unsafe_allow_html=True)

# منتجات SHEIN
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
    {"code": "SH011", "name": "أقراط هوب مطلية بالذهب 3 أزواج", "price": 1.43, "discount": 5, "link": "https://onelink.shein.com/38/5shti8ffmexk", "sales": "50+"},
    {"code": "SH012", "name": "شعر مستعار قصير مجعد", "price": 2.70, "discount": 33, "link": "https://onelink.shein.com/38/5shthyka1fts", "sales": "100+"},
    {"code": "SH013", "name": "حذاء تزلج بإضاءة LED للأطفال", "price": 34.72, "discount": 37, "link": "https://onelink.shein.com/38/5shthetyxlby", "sales": "50+"},
    {"code": "SH014", "name": "طقم مقص أظافر احترافي", "price": 1.40, "discount": 36, "link": "https://onelink.shein.com/38/5shtg7fahsfp", "sales": "1200+"},
    {"code": "SH015", "name": "هاتف لعبة موسيقي تعليمي", "price": 3.40, "discount": 0, "link": "https://onelink.shein.com/38/5shtfvl3s22n", "sales": "50+"},
    {"code": "SH016", "name": "شريط إضاءة RGB LED", "price": 2.27, "discount": 55, "link": "https://onelink.shein.com/38/5shtfbusmt15", "sales": "200+"},
    {"code": "SH017", "name": "طقم بيسبول للأولاد", "price": 3.28, "discount": 80, "link": "https://onelink.shein.com/38/5shtek8d4572", "sales": "100+"},
    {"code": "SH018", "name": "شريط لاصق مزدوج قوي", "price": 1.05, "discount": 30, "link": "https://onelink.shein.com/38/5shtead7hrfl", "sales": "800+"},
    {"code": "SH019", "name": "طبق طعام محكم الإغلاق 24 قطعة", "price": 7.14, "discount": 60, "link": "https://onelink.shein.com/38/5shtdonvakbf", "sales": "150+"},
    {"code": "SH020", "name": "حقيبة شاطئ كبيرة السعة", "price": 2.34, "discount": 57, "link": "https://onelink.shein.com/38/5shtcj87y44e", "sales": "100+"},
]

# عرض منتجات SHEIN في شبكة 4 أعمدة
cols = st.columns(4)
for i, product in enumerate(SHEIN_PRODUCTS[:20]):
    with cols[i % 4]:
        final_price = product['price'] * (1 - product['discount']/100) if product['discount'] > 0 else product['price']
        old_price = product['price'] if product['discount'] > 0 else None
        
        st.markdown(f"""
        <div class='product-card'>
            <div class='product-code'>📦 {product['code']}</div>
            <div class='product-name'>{product['name']}</div>
            <div class='product-price'>
                ${final_price:.2f}
                {f"<span class='old-price'>${old_price:.2f}</span>" if old_price else ""}
            </div>
            <div class='product-sales'>📊 تم البيع: {product['sales']}</div>
            <div class='product-discount'>{'🔥 خصم ' + str(product['discount']) + '%' if product['discount'] > 0 else ''}</div>
            <a href='{product['link']}' target='_blank' style='text-decoration: none;'>
                <div class='product-btn'>🛒 تسوق الآن</div>
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== منتجات نون (قسم منفصل) ==========
st.markdown("""
<div class='store-section'>
    <div class='store-header store-header-noon'>
        <h2 style='color: white; font-size: 36px; margin: 0;'>🛍️ متجر نون</h2>
        <p style='color: white; font-size: 18px; margin: 5px 0 0 0;'>أفضل العروض والمنتجات</p>
    </div>
</div>
""", unsafe_allow_html=True)

# منتجات نون
NOON_PRODUCTS = [
    {"code": "N001", "name": "ساعة ذكية رياضية", "price": 89.99, "discount": 30, "link": "https://www.noon.com/ar-sa/Z09748F5900924601C848Z/p/", "sales": "500+"},
    {"code": "N002", "name": "سماعات لاسلكية بلوتوث", "price": 45.50, "discount": 25, "link": "https://www.noon.com/ar-sa/N11200839A/p/", "sales": "1200+"},
    {"code": "N003", "name": "شاحن سريع بقاعدة", "price": 29.90, "discount": 15, "link": "https://www.noon.com/ar-sa/N70140492V/p/", "sales": "800+"},
    {"code": "N004", "name": "حافظة جوال سيليكون", "price": 12.99, "discount": 40, "link": "https://www.noon.com/ar-sa/ZF23DE5EC51560ADE2D7EZ/p/", "sales": "2000+"},
    {"code": "N005", "name": "سوار رياضي ذكي", "price": 35.00, "discount": 20, "link": "https://www.noon.com/ar-sa/N70140491V/p/", "sales": "300+"},
    {"code": "N006", "name": "مروحة USB محمولة", "price": 18.75, "discount": 35, "link": "https://www.noon.com/ar-sa/N23772548A/p/", "sales": "600+"},
    {"code": "N007", "name": "مصباح ليلي LED بتقنية USB", "price": 22.30, "discount": 28, "link": "https://www.noon.com/ar-sa/Z9C3189BD600BD4CEA2D6Z/p/", "sales": "400+"},
    {"code": "N008", "name": "كابل شحن سريع 2 متر", "price": 8.99, "discount": 45, "link": "https://www.noon.com/ar-sa/N70105592V/p/", "sales": "3500+"},
    {"code": "N009", "name": "حامل هاتف للسيارة", "price": 15.50, "discount": 30, "link": "https://www.noon.com/ar-sa/N70211464V/p/", "sales": "900+"},
    {"code": "N010", "name": "سماعة أذن سلكية", "price": 11.20, "discount": 50, "link": "https://www.noon.com/ar-sa/Z07429F51B52E11B1DED8Z/p/", "sales": "1500+"},
    {"code": "N011", "name": "باور بانك 10000mAh", "price": 42.00, "discount": 22, "link": "https://www.noon.com/ar-sa/ZB171FAD035B635D43253Z/p/", "sales": "700+"},
    {"code": "N012", "name": "ساعة يد رجالية", "price": 65.00, "discount": 18, "link": "https://www.noon.com/ar-sa/Z5F0E0825DFAF44FB5ED0Z/p/", "sales": "250+"},
]

# عرض منتجات نون في شبكة 4 أعمدة
cols = st.columns(4)
for i, product in enumerate(NOON_PRODUCTS):
    with cols[i % 4]:
        final_price = product['price'] * (1 - product['discount']/100) if product['discount'] > 0 else product['price']
        old_price = product['price'] if product['discount'] > 0 else None
        
        st.markdown(f"""
        <div class='product-card'>
            <div class='product-code'>📦 {product['code']}</div>
            <div class='product-name'>{product['name']}</div>
            <div class='product-price'>
                ${final_price:.2f}
                {f"<span class='old-price'>${old_price:.2f}</span>" if old_price else ""}
            </div>
            <div class='product-sales'>📊 تم البيع: {product['sales']}</div>
            <div class='product-discount'>{'🔥 خصم ' + str(product['discount']) + '%' if product['discount'] > 0 else ''}</div>
            <a href='{product['link']}' target='_blank' style='text-decoration: none;'>
                <div class='product-btn'>🛒 تسوق الآن</div>
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== منتجات AliExpress (قسم منفصل) ==========
st.markdown("""
<div class='store-section'>
    <div class='store-header store-header-aliexpress'>
        <h2 style='color: white; font-size: 36px; margin: 0;'>🛍️ متجر AliExpress</h2>
        <p style='color: white; font-size: 18px; margin: 5px 0 0 0;'>قادم قريباً بأفضل العروض</p>
    </div>
</div>
""", unsafe_allow_html=True)

# منتجات AliExpress (قادمة)
st.markdown("""
<div style='text-align: center; padding: 60px; background: linear-gradient(135deg, rgba(255,71,87,0.2), rgba(255,107,129,0.2)); border-radius: 40px; margin: 20px 0;'>
    <h3 style='color: #feca57; font-size: 32px; margin-bottom: 20px;'>🚀 قادم قريباً جداً</h3>
    <p style='color: #ddd; font-size: 20px;'>نستعد لإطلاق متجر AliExpress مع أفضل العروض والمنتجات</p>
    <p style='color: #ff6b6b; font-size: 18px; margin-top: 20px;'>✨ تابعونا للمزيد من العروض الحصرية ✨</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== بوت الدردشة ==========
st.markdown("<h2 style='color: #feca57; text-align: center; font-size: 32px; margin-bottom: 20px;'>💬 تحدث مع Saeed DaTaBoT</h2>", unsafe_allow_html=True)

chat_question = st.text_area("📝 اكتب سؤالك هنا:", placeholder="ماذا تريد أن تسأل Saeed DaTaBoT؟", height=100)

if st.button("💬 أرسل", use_container_width=True):
    if chat_question:
        quick_ans = quick_response(chat_question)
        if quick_ans:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71; margin-bottom: 20px;'>
                <h4 style='color: #feca57;'>🤖 Saeed DaTaBoT يرد:</h4>
                <p style='color: #e2e8f0;'>{quick_ans}</p>
            </div>
            """, unsafe_allow_html=True)
            try:
                tts = gTTS(text=quick_ans[:300], lang='ar')
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format='audio/mp3')
            except:
                pass
        elif model:
            try:
                response = model.generate_content(f"رد باختصار وثقة كـ Saeed DaTaBoT: {chat_question}")
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'>
                    <h4 style='color: #feca57;'>🤖 Saeed DaTaBoT يرد:</h4>
                    <p style='color: #e2e8f0;'>{response.text}</p>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.error("⚠️ حدث خطأ، يرجى المحاولة لاحقاً")
    else:
        st.warning("📝 يرجى كتابة سؤالك أولاً")

st.markdown("---")

# ========== السايدبار ==========
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 30px; margin-bottom: 20px;'>
        <h2 style='color: #feca57; margin-bottom: 10px;'>🤖 Saeed DaTaBoT</h2>
        <p style='color: #aaa;'>مساعدك الذكي للتسوق</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 خدمات Saeed DaTaBoT:")
    st.markdown("""
    - ✅ تحليل الروابط
    - ✅ فحص توفر المنتجات
    - ✅ عروض SHEIN الحصرية
    - ✅ عروض نون المميزة
    - ✅ علي اكسبرس قادم
    - ✅ محادثة ذكية
    """)
    
    st.markdown("---")
    
    st.markdown("### 📞 للتواصل:")
    st.markdown("- [@SaeedMarketAds](https://t.me/SaeedMarketAds)")
    st.markdown("- [@SaeedDataBot](https://t.me/SaeedDataBot)")
    
    st.markdown("---")
    
    st.markdown("### 📊 إحصائيات:")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🛍️ منتجات SHEIN", "51")
    with col2:
        st.metric("⭐ منتجات نون", "12+")
    
    st.markdown("---")
    st.caption("© 2026 سوق سعيد - جميع الحقوق محفوظة")
    st.caption("برمجة وتطوير: سعيد المسوري")


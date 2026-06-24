import streamlit as st
import google.generativeai as genai
import requests
import os
import base64
import streamlit.components.v1 as components
import edge_tts
import tempfile
import asyncio
import pandas as pd  # مكتبة قراءة ملفات البيانات

# ============================================================
# 1. إعدادات الصفحة
# ============================================================
st.set_page_config(
    page_title="سوق سعيد | متاجر SHEIN - نون - علي اكسبرس",
    page_icon="🛍️",
    layout="wide"
)

# ============================================================
# 2. دالة قراءة المنتجات المسرعة من ملف CSV
# ============================================================
@st.cache_data(ttl=600)  # تحديث التخزين كل 10 دقائق تلقائياً
def load_products_by_store(store_name):
    try:
        if os.path.exists('products.csv'):
            df = pd.read_csv('products.csv')
            # تصفية المنتجات حسب اسم المتجر المختار
            store_products = df[df['store'].str.upper() == store_name.upper()]
            return store_products.to_dict(orient='records')
        return []
    except Exception as e:
        st.error(f"خطأ في قراءة ملف المنتجات: {str(e)}")
        return []

# ============================================================
# 3. الخلفية والتصميم (CSS)
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
.product-sales {
    color: #2ecc71;
    font-weight: bold;
    font-size: 13px;
    margin-bottom: 10px;
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
# 4. دالة تشغيل الصوت
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
        return None

def play_voice(text):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_bytes = loop.run_until_complete(generate_audio(text))
        loop.close()
        if audio_bytes:
            b64 = base64.b64encode(audio_bytes).decode()
            audio_html = f'<audio autoplay="true" style="display:none;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(audio_html, unsafe_allow_html=True)
            return True
        return False
    except:
        return False

# ============================================================
# 5. قراءة المفاتيح والتعليمات
# ============================================================
def get_secret(key, fallback_key=None, default=None):
    try:
        if key in st.secrets: return st.secrets[key]
        if fallback_key and fallback_key in st.secrets: return st.secrets[fallback_key]
        return default
    except: return default

GEMINI_API_KEY = get_secret("GEMINI_MAIN_KEY", "GEMINI_API", None)

try:
    with open('Instructions.txt', 'r', encoding='utf-8') as f:
        instructions = f.read()
except FileNotFoundError:
    instructions = "أنت Saeed DaTaBoT مساعد ذكي خبير في التسوق الإلكتروني لمشروع saeedmarketads."

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name="gemini-3.1-flash", system_instruction=instructions)
else:
    model = None

# ============================================================
# 6. الردود السريعة
# ============================================================
def quick_response(question):
    q = question.lower()
    if "كيف حال" in q or "كيفك" in q or "اخبار" in q:
        return "بخير والحمد لله، أنا هنا لخدمتك يا صديقي. كيف يمكنني مساعدتك اليوم؟"
    elif "كود" in q or "خصم" in q:
        return "🎁 **كود خصم SHEIN الحصري** 🎁\n\n🏷️ **الكود: WL7KA**\n\n🔥 خصم يصل إلى 60% على أول طلب"
    elif "من أنت" in q or "من برمج" in q or "المطور" in q or "سعيد" in q:
        return "🤖 أنا **Saeed DaTaBoT**، مساعدك الذكي للتسوق.\n\nالمطور والعقل المدبر هو **سعيد المسوري**، مؤسس **saeedmarketads**."
    elif "السلام" in q or "مرحبا" in q:
        return "وعليكم السلام ورحمة الله وبركاته 🌹\n\nمرحباً بكم في **saeedmarketads**، المنصة الرائدة مع تقنية الذكاء الاصطناعي."
    elif "شكرا" in q:
        return "العفو، تحت أمرك في أي وقت."
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
# 7. الواجهة الرئيسية والعروض
# ============================================================
render_custom_banner()

if 'audio_played' not in st.session_state:
    welcome_msg = "مرحباً بكم في منصة saeedmarketads الرائدة مع تقنية الذكاء الاصطناعي. أنا سعيد داتا بوت، تحت خدمتكم."
    play_voice(welcome_msg)
    st.session_state.audio_played = True

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
# 8. أزرار المتاجر الذكية لقراءة ملف الـ CSV
# ============================================================
st.markdown("<h2 style='color: #feca57; text-align: center;'>🏪 اختر المتجر للتصفح</h2>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("🛍️ تصفح عروض SHEIN", key="btn_shein"):
        st.session_state.current_store = "SHEIN"
with col_btn2:
    if st.button("💛 تصفح عروض Noon", key="btn_noon"):
        st.session_state.current_store = "Noon"
with col_btn3:
    if st.button("🚀 تصفح عروض AliExpress", key="btn_ali"):
        st.session_state.current_store = "AliExpress"

# إدارة عرض المنتجات ديناميكياً
if 'current_store' in st.session_state:
    current_store = st.session_state.current_store
    
    if current_store == "SHEIN":
        st.markdown("<div class='store-header-shein'><h2 style='color:white;'>🛍️ منتجات متجر SHEIN الحالية</h2></div>", unsafe_allow_html=True)
    elif current_store == "Noon":
        st.markdown("<div class='store-header-noon'><h2 style='color:white;'>💛 منتجات متجر Noon الحالية</h2></div>", unsafe_allow_html=True)
    elif current_store == "AliExpress":
        st.markdown("<div class='store-header-aliexpress'><h2 style='color:white;'>🚀 منتجات متجر AliExpress</h2></div>", unsafe_allow_html=True)

    products_list = load_products_by_store(current_store)

    if products_list:
        cols = st.columns(4)
        for i, product in enumerate(products_list):
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
    else:
        st.info(f"القسم الخاص بـ {current_store} قيد التحديث وإضافة منتجات جديدة قريباً!")

st.markdown("---")

# ============================================================
# 9. بوت الدردشة الذكي وتحليل الروابط
# ============================================================
st.markdown("<h2 style='color: #feca57; text-align: center;'>💬 تحدث مع Saeed DaTaBoT</h2>", unsafe_allow_html=True)
chat_question = st.text_area("📝 اكتب سؤالك أو ضع رابط المنتج هنا للتحليل والمحادثة المباشرة:", height=100)

if st.button("💬 إرسال الطلب", use_container_width=True):
    if chat_question:
        quick_ans = quick_response(chat_question)
        if quick_ans:
            st.markdown(f"<div style='background: #1e2a3e; border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'><h4 style='color: #feca57;'>🤖 يرد:</h4><p style='color: #e2e8f0;'>{quick_ans}</p></div>", unsafe_allow_html=True)
            play_voice(quick_ans)
        elif model:
            try:
                with st.spinner("🤖 جاري معالجة الطلب بذكاء..."):
                    response = model.generate_content(f"رد باختصار كـ Saeed DaTaBoT: {chat_question}")
                    bot_reply = response.text
                    st.markdown(f"<div style='background: #1e2a3e; border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'><h4 style='color: #feca57;'>🤖 يرد:</h4><p style='color: #e2e8f0;'>{bot_reply}</p></div>", unsafe_allow_html=True)
                    play_voice(bot_reply)
            except:
                fallback = "أهلاً بك، تم استلام طلبك بنجاح وجاري فحص أفضل العروض لك."
                st.markdown(f"<div style='background: #1e2a3e; border-radius: 25px; padding: 25px; border-right: 5px solid #ff6b6b;'><p style='color: #e2e8f0;'>{fallback}</p></div>", unsafe_allow_html=True)
                play_voice(fallback)
    else:
        st.warning("📝 يرجى كتابة استفسارك أولاً.")

# ============================================================
# 10. السايدبار الإحصائي والتواصل
# ============================================================
with st.sidebar:
    st.markdown("<div style='text-align: center; padding: 20px; background: #1a1a2e; border-radius: 30px;'><h2>🤖 سعيد داتا بوت</h2></div>", unsafe_allow_html=True)
    st.markdown("### 🎯 خدمات المنصة:")
    st.markdown("- ✅ استيراد سحابي للمنتجات\n- ✅ تحديث فوري فائق السرعة\n- ✅ دعم الذكاء الاصطناعي الفصيح")
    st.markdown("---")
    st.markdown("### 📞 قنواتنا الحالية:")
    st.markdown("[Telegram Channel](https://t.me/SeenMarket2026)")
    st.markdown("---")
    st.caption("© 2026 saeedmarketads")

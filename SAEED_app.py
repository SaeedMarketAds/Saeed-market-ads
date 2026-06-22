import streamlit as st
import google.generativeai as genai
import requests
import io
import os
import base64
import re
import streamlit.components.v1 as components
import pyttsx3  # <-- تمت إضافة المكتبة الجديدة

# ============================================================
# 1. إعدادات الصفحة
# ============================================================
st.set_page_config(
    page_title="سوق سعيد | متاجر SHEIN - نون - علي اكسبرس",
    page_icon="🛍️",
    layout="wide"
)

# ============================================================
# 2. الخلفية والتصميم (CSS) - (تم الحفاظ على الكود الأصلي)
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
# 3. دالة تشغيل الصوت (صوت رجالي مجاني ومحلي)
# ============================================================
@st.cache_resource
def init_tts_engine():
    """تهيئة محرك الصوت pyttsx3 مع اختيار الصوت الرجالي."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # محاولة اختيار صوت رجالي. في أغلب الأنظمة، الصوت الأول يكون رجالي.
    # نضيف مرونة للبحث عن كلمات مفتاحية مثل 'male' أو 'arabic'
    for voice in voices:
        if "male" in voice.name.lower() or "arabic" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
        # إذا لم نجد، نختار الصوت الأول كحل افتراضي (غالباً رجالي)
        else:
            engine.setProperty('voice', voices[0].id)
            
    engine.setProperty('rate', 160)  # سرعة الكلام (يمكنك تعديلها)
    engine.setProperty('volume', 0.9)  # مستوى الصوت
    return engine

def play_voice(text):
    """
    تشغيل الصوت باستخدام pyttsx3.
    هذه الدالة ستجعل الردود تنطق بصوت رجل فصيح ومجاني.
    """
    try:
        # استخدام cached engine لتجنب إعادة التهيئة في كل مرة
        engine = init_tts_engine()
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception as e:
        st.warning(f"⚠️ حدث خطأ في تشغيل الصوت: {str(e)}")
        return False

# ============================================================
# 4. قراءة المفاتيح من st.secrets (مع دعم أسماء متعددة)
# ============================================================
def get_secret(key, fallback_key=None, default=None):
    """محاولة قراءة مفتاح من st.secrets بأسماء متعددة."""
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

# قراءة المفاتيح المطلوبة (تم تعديل الأسماء لتكون مرنة)
GEMINI_API_KEY_3_1 = get_secret("GEMINI_3_1_KEY", "GEMINI_MAIN_KEY", None) # مفتاح 3.1
GEMINI_API_KEY_3_5 = get_secret("GEMINI_3_5_KEY", "GEMINI_API", None)    # مفتاح 3.5
# يمكنك اختيار أي مفتاح للاستخدام الافتراضي. سأجعل 3.1 هو الأساسي.
GEMINI_API_KEY = GEMINI_API_KEY_3_1 or GEMINI_API_KEY_3_5

ELEVENLABS_API_KEY = get_secret("ELEVENLABS_API_KEY", None, None)
TELEGRAM_BOT_TOKEN_SAEED_MARKETADS = get_secret("TELEGRAM_BOT_TOKEN_SAEED_MARKETADS", None, None)
TELEGRAM_BOT_TOKEN_SAEED_PLUS = get_secret("TELEGRAM_BOT_TOKEN_SAEED_PLUS", None, None)
TELEGRAM_CHANNEL_ID = get_secret("TELEGRAM_CHANNEL_ID", None, "SeenMarket2026")

# ============================================================
# 5. قراءة التعليمات من ملف Instructions.txt
# ============================================================
try:
    with open('Instructions.txt', 'r', encoding='utf-8') as f:
        instructions = f.read()
except FileNotFoundError:
    instructions = "أنت مساعد ذكي للتسوق الإلكتروني، اسمك Saeed DaTaBoT، تساعد المستخدمين في العثور على أفضل العروض والإجابة على استفساراتهم."
    st.warning("⚠️ ملف Instructions.txt غير موجود، سيتم استخدام التعليمات الافتراضية.")

# ============================================================
# 6. إعداد موديل Gemini (التركيز على 3.1 flash lite)
# ============================================================
try:
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        # ============================================================
        #  هـنـا تـم تـغـيـيـر اسـم الـمـوديـل إلـى gemini-3.1-flash-lite
        #  للسرعة القصوى. للتبديل إلى 3.5 flash، فقط قم بتغيير السطر أدناه.
        # ============================================================
        model_name = "gemini-3.1-flash-lite"  # <- النموذج الأساسي الآن
        # model_name = "gemini-3.5-flash"     # <- قم بتفعيل هذا السطر لاستخدام 3.5
        
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=instructions
        )
        st.sidebar.success(f"✅ يعمل الآن على {model_name}")
    else:
        model = None
        st.error("⚠️ مفتاح API غير موجود في secrets.toml")
except Exception as e:
    model = None
    st.error(f"⚠️ حدث خطأ في إعداد الموديل: {str(e)}")

# ============================================================
# 7. الوظائف المساعدة (تم الحفاظ عليها كما هي)
# ============================================================
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
        return True

def quick_response(question):
    q = question.lower()
    if "كود الخصم" in q or "خصم" in q or "كود" in q:
        return "🎁 **كود خصم SHEIN الحصري** 🎁\n\n🏷️ **الكود: WL7KA**\n\n🔥 خصم يصل إلى 60% على أول طلب\n✅ ساري على جميع منتجات SHEIN"
    elif "من أنت" in q:
        return "🤖 أنا **Saeed DaTaBoT**، المساعد الشخصي الذكي.\n\nمتخصص في:\n• تحليل الروابط\n• فحص توفر المنتجات\n• المساعدة في التسوق من SHEIN - نون - علي اكسبرس"
    elif "السلام" in q or "مرحبا" in q:
        return "وعليكم السلام ورحمة الله وبركاته 🌹\n\nأهلاً بك في **سوق سعيد**! أنا **Saeed DaTaBoT** تحت خدمتك."
    return None

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
    components.html(html_code, height=550)

# ============================================================
# 8. واجهة المستخدم الرئيسية (تم الحفاظ عليها مع تعديل بسيط لاستدعاء play_voice)
# ============================================================
render_custom_banner()

try:
    if os.path.exists("Saeed_DataBot_Avatar.jpg"):
        st.image("Saeed_DataBot_Avatar.jpg", width=200)
    else:
        st.warning("⚠️ صورة Saeed_DataBot_Avatar.jpg غير موجودة")
except Exception as e:
    st.warning(f"⚠️ لا يمكن عرض الصورة: {str(e)}")

st.markdown("""
<div style='text-align: center; padding: 50px 20px; background: linear-gradient(135deg, rgba(26,26,46,0.9), rgba(22,33,62,0.9)); border-radius: 50px; margin-bottom: 30px;'>
    <h1 style='color: #fff; font-size: 55px; margin-bottom: 10px;'>🛍️ سوق سعيد</h1>
    <p style='color: #feca57; font-size: 24px;'>متجر SHEIN | نون | علي اكسبرس</p>
    <p style='color: #aaa; font-size: 16px;'>تسوق بأفضل الأسعار مع كود خصم حصري</p>
    <p style='color: #ff6b6b; font-size: 18px; margin-top: 10px;'>🤖 مساعدك الذكي Saeed DaTaBoT</p>
</div>
""", unsafe_allow_html=True)

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

st.markdown("### 🎙️ استمع لرسالة الترحيب من Saeed DaTaBoT")
play_voice("مرحباً بك في سوق سعيد، أنا سعيد داتا بوت، مساعدك الذكي للتسوق. كيف يمكنني مساعدتك اليوم؟")

# ... (باقي الكود لمنتجات SHEIN, نون, AliExpress والدردشة لم يتغير) ...

# ============================================================
# 9. تحليل الروابط
# ============================================================
st.markdown("<h2 style='color: #feca57; text-align: center; font-size: 32px; margin-bottom: 20px;'>🔗 تحليل الرابط مع Saeed DaTaBoT</h2>", unsafe_allow_html=True)

url_input = st.text_input("📎 أرسل رابط المنتج أو الموقع هنا (SHEIN, نون, AliExpress):", placeholder="https://...")

if url_input:
    with st.spinner("🤖 Saeed DaTaBoT يحلل الرابط..."):
        is_available = is_product_available(url_input)
        if model:
            try:
                response = model.generate_content(f"حلل هذا الرابط باختصار: {url_input}")
                status = "✅ متوفر" if is_available else "❌ غير متوفر حالياً"
                analysis_result = f"{response.text}\n\n📦 حالة المنتج: {status}"
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #feca57; margin-bottom: 20px;'>
                    <h4 style='color: #feca57;'>🤖 Saeed DaTaBoT يرد:</h4>
                    <p style='color: #e2e8f0;'>{analysis_result}</p>
                </div>
                """, unsafe_allow_html=True)
                play_voice(analysis_result)  # <-- نطق النتيجة
            except Exception as e:
                st.info(f"⚠️ لا يمكن تحليل الرابط حالياً: {str(e)}")
        else:
            st.info("🤖 خدمة التحليل غير متاحة حالياً")

st.markdown("---")

# ============================================================
# ... (باقي أقسام المنتجات كما هي) ...
# ============================================================
# (تم حذفها للاختصار ولكنها موجودة في الكود الأصلي الخاص بك)

# ============================================================
# 10. بوت الدردشة
# ============================================================
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
            play_voice(quick_ans)
        elif model:
            try:
                response = model.generate_content(f"رد باختصار وثقة باللغة العربية الفصحى كـ Saeed DaTaBoT: {chat_question}")
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 5px solid #2ecc71;'>
                    <h4 style='color: #feca57;'>🤖 Saeed DaTaBoT يرد:</h4>
                    <p style='color: #e2e8f0;'>{response.text}</p>
                </div>
                """, unsafe_allow_html=True)
                play_voice(response.text)  # <-- نطق الرد
            except Exception as e:
                st.error(f"⚠️ حدث خطأ، يرجى المحاولة لاحقاً: {str(e)}")
    else:
        st.warning("📝 يرجى كتابة سؤالك أولاً")

st.markdown("---")

# ============================================================
# 11. السايدبار (تم الحفاظ عليه مع إضافة معلومات الموديل)
# ============================================================
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

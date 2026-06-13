import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile

# إعداد الصفحة - يجب أن يكون أول أمر
st.set_page_config(
    page_title="Saeed Market AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS للتدرج اللوني
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 50%, #fad0c4 100%);
    }
    .main-header {
        background: linear-gradient(135deg, #2c3e50, #1a1a2e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        text-align: center;
        font-weight: bold;
    }
    .product-card {
        background: white;
        border-radius: 20px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# عنوان التطبيق
st.markdown('<h1 class="main-header">🤖 Saeed Market AI | محرك 3.5 Flash + صوت</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:1.2rem">✨ تسريع فائق بالذكاء الاصطناعي | كود SHEIN: <strong style="background:#ff6b4a; padding:5px 15px; border-radius:30px; color:white">WL7KA</strong> | خصم 60% للمستخدمين الجدد ✨</p>', unsafe_allow_html=True)

# تهيئة جلسة المتغيرات
if "messages" not in st.session_state:
    st.session_state.messages = []
if "gemini_ready" not in st.session_state:
    st.session_state.gemini_ready = False
if "error_shown" not in st.session_state:
    st.session_state.error_shown = False

# تهيئة نموذج Gemini (مع معالجة الأخطاء)
def init_gemini():
    try:
        # محاولة الحصول على المفتاح من secrets أو استخدام مفتاح تجريبي
        try:
            API_KEY = st.secrets["GEMINI_API_KEY"]
        except:
            # مفتاح تجريبي عام محدود - يفضل استبداله بمفتاحك الخاص
            API_KEY = "YOUR_API_KEY_HERE"
        
        if API_KEY == "YOUR_API_KEY_HERE":
            st.session_state.gemini_ready = False
            return False
        
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.session_state.model = model
        st.session_state.gemini_ready = True
        return True
    except Exception as e:
        if not st.session_state.error_shown:
            st.error(f"⚠️ لم يتم توصيل Gemini: {e}\n\nيرجى إضافة مفتاح API صالح في .streamlit/secrets.toml")
            st.session_state.error_shown = True
        st.session_state.gemini_ready = False
        return False

# محاولة تهيئة Gemini
init_gemini()

# عرض حالة الاتصال
if st.session_state.gemini_ready:
    st.success("✅ تم توصيل محرك Gemini 3.5 Flash بنجاح!")
else:
    st.info("ℹ️ يعمل التطبيق في وضع تجريبي (بدون AI). أضف مفتاح API للاستفادة من الذكاء الاصطناعي.")

# واجهة الدردشة
st.subheader("💬 الدردشة مع المساعد الذكي")

# عرض سجل المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# إدخال المستخدم - استخدام الطريقة المستقرة
user_input = st.chat_input("اكتب سؤالك هنا...")

def generate_response(prompt):
    """توليد رد من Gemini مع معالجة الأخطاء"""
    if not st.session_state.gemini_ready:
        return "🔧 عذراً، خدمة الذكاء الاصطناعي غير متاحة حالياً. يرجى إضافة مفتاح API صالح أو المحاولة لاحقاً."
    
    try:
        response = st.session_state.model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ حدث خطأ: {str(e)[:100]}"

def text_to_speech(text):
    """تحويل النص إلى صوت"""
    try:
        tts = gTTS(text=text[:500], lang="ar")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        return None

# معالجة إدخال المستخدم
if user_input:
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # توليد الرد
    with st.chat_message("assistant"):
        with st.spinner("🤔 جاري التفكير..."):
            response = generate_response(user_input)
            st.write(response)
    
    # إضافة الرد إلى السجل
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # تشغيل الصوت
    audio_file = text_to_speech(response)
    if audio_file:
        st.audio(audio_file, format="audio/mp3")

# عرض المنتجات
st.subheader("🛍️ منتجات SHEIN - عروض حصرية")

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        st.image("https://img.shein.com/uploadstyle/2024/12/coat_fd.jpg", use_container_width=True)
        st.markdown("**SHEIN Playful Pals Young Girl Hooded Padded Coat**")
        st.markdown("💰 **$19.39** <span style='background:#ffc107; padding:2px 8px; border-radius:20px;'>-43%</span>", unsafe_allow_html=True)
        st.link_button("🛒 شراء الآن", "https://onelink.shein.com/38/5shrzfcizjmg", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        st.image("https://img.shein.com/uploadstyle/2024/11/shirt_blue.jpg", use_container_width=True)
        st.markdown("**Elegant Design Mature Hong Kong Style Shirt**")
        st.markdown("💰 **$14.18** <span style='background:#ffc107; padding:2px 8px; border-radius:20px;'>-37%</span>", unsafe_allow_html=True)
        st.link_button("🛒 شراء الآن", "https://onelink.shein.com/38/5shune7n90yf", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# شريط جانبي
with st.sidebar:
    st.header("🎁 كود الخصم الحصري")
    st.code("WL7KA", language="text")
    st.markdown("**خصم 60% للمستخدمين الجدد!**")
    
    st.divider()
    
    st.header("🔧 كيفية إضافة مفتاح API")
    st.markdown("""
    1. قم بإنشاء ملف `.streamlit/secrets.toml`
    2. أضف السطر التالي:
    ```toml
    GEMINI_API_KEY = "مفتاحك_هنا"
    ```
    3. احصل على مفتاح مجاني من [Google AI Studio](https://aistudio.google.com/)
    """)
    
    st.divider()
    
    st.header("📦 المكتبات المستخدمة")
    libraries = ["streamlit", "google-generativeai", "gtts"]
    for lib in libraries:
        st.write(f"- {lib}")
    
    # زر إعادة ضبط المحادثة
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

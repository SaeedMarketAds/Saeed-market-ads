
import streamlit as st
import os
import google.generativeai as genai
import requests
import base64
from gtts import gTTS
import io

# ========== إعداد الصفحة ==========
st.set_page_config(page_title="Saeed DaTaBoT | سوق سعيد", page_icon="🤖", layout="wide")

# ========== تصميم خلفية الواجهة الاحترافية ==========
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0.3);
}
.stButton > button {
    background: linear-gradient(90deg, #ff6b6b, #feca57);
    color: white;
    border: none;
    border-radius: 30px;
    padding: 10px 25px;
    font-weight: bold;
    transition: 0.3s;
}
.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #feca57, #ff6b6b);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ========== قراءة جميع المفاتيح من Secrets ==========
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API"]
    TELEGRAM_BOT_TOKEN_SAEED_MARKETADS = st.secrets["TELEGRAM_BOT_TOKEN_SAEED_MARKETADS"]
    TELEGRAM_BOT_TOKEN_SAEED_PLUS = st.secrets["TELEGRAM_BOT_TOKEN_SAEED_PLUS"]
    TELEGRAM_CHANNEL_ID = st.secrets["TELEGRAM_CHANNEL_ID"]
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
except Exception as e:
    st.error(f"⚠️ خطأ في قراءة Secrets: {e}")

# ========== إعداد Gemini ==========
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-3.5-flash')
except Exception as e:
    model = None

# ========== تعريف البوت ==========
st.markdown("""
<div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 40px; margin-bottom: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.3);'>
    <h1 style='color: #fff; font-size: 56px; margin-bottom: 10px;'>🤖 Saeed DaTaBoT</h1>
    <p style='color: #ddd; font-size: 22px;'>المساعد الشخصي لـ <span style='color: #ff6b6b; font-weight: bold;'>سعيد المسوري</span></p>
    <p style='color: #aaa; font-size: 16px;'>تم البرمجة بواسطة سعيد المسوري وبمساعدة الذكاء الاصطناعي 🚀</p>
    <div style='background: rgba(255,255,255,0.08); border-radius: 30px; padding: 20px; margin-top: 20px;'>
        <p style='color: #feca57; font-size: 18px;'>🇾🇪 دعم المنتجات اليمنية | التسويق الرقمي | ريلز | صور | فيديوهات 🇾🇪</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== تحليل الروابط ==========
st.markdown("<h2 style='color: #feca57;'>🔗 تحليل الروابط والمساعدة الذكية</h2>", unsafe_allow_html=True)

url_input = st.text_input("أرسل رابط المنتج أو الموقع هنا (SHEIN, AliExpress, Noon, أو أي رابط):", placeholder="https://...")

if url_input:
    with st.spinner("🤖 جاري تحليل الرابط..."):
        try:
            analysis_prompt = f"""
            أنت Saeed DaTaBoT، المساعد الشخصي لسعيد المسوري.
            قم بتحليل هذا الرابط للمستخدم: {url_input}
            
            أجب بالعربية وأخبر المستخدم:
            1. ما هو نوع هذا الرابط (متجر، منتج، فيديو، صورة، ريلز)
            2. ماذا يمكن أن يقدم له هذا الرابط
            3. قدم له نصيحة تسويقية أو شرائية مناسبة
            4. كن ودوداً ومحفزاً بأسلوب اليمني الأصيل
            """
            response = model.generate_content(analysis_prompt)
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 25px; padding: 25px; border-right: 6px solid #ff6b6b; box-shadow: 0 10px 20px rgba(0,0,0,0.2);'>
                <h4 style='color: #feca57; margin-bottom: 15px;'>📊 نتيجة التحليل:</h4>
                <p style='color: #e2e8f0; line-height: 1.8;'>{response.text}</p>
            </div>
            """, unsafe_allow_html=True)
            
            tts = gTTS(text=response.text[:500], lang='ar')
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format='audio/mp3')
            
        except Exception as e:
            st.error(f"خطأ في التحليل: {e}")

st.markdown("---")

# ========== منتجات يمنية ==========
st.markdown("<h2 style='color: #feca57;'>🇾🇪 منتجات يمنية - دعم الصناعة المحلية 🇾🇪</h2>", unsafe_allow_html=True)

yemeni_products = [
    {"name": "عسل السدر اليمني", "price": "25$", "desc": "عسل طبيعي 100% من وادي حضرموت", "image": "🍯"},
    {"name": "قهوة يمنية خولاني", "price": "30$", "desc": "أجود أنواع البن اليمني", "image": "☕"},
    {"name": "لبان بخوري", "price": "10$", "desc": "لبان ذكرى من حضرموت", "image": "🪔"},
    {"name": "مجبس صنعاني", "price": "15$", "desc": "مجبس جلدي صنع يدوي", "image": "👞"},
]

cols = st.columns(4)
for i, product in enumerate(yemeni_products):
    with cols[i]:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0f3460, #16213e); border-radius: 25px; padding: 20px; text-align: center; transition: 0.3s; box-shadow: 0 10px 20px rgba(0,0,0,0.2);'>
            <h1 style='font-size: 60px; margin-bottom: 10px;'>{product['image']}</h1>
            <h3 style='color: #feca57; margin-bottom: 8px;'>{product['name']}</h3>
            <p style='color: #aaa; margin-bottom: 12px;'>{product['desc']}</p>
            <p style='color: #ff6b6b; font-size: 26px; font-weight: bold; margin-bottom: 15px;'>{product['price']}</p>
            <div style='background: linear-gradient(90deg, #ff6b6b, #feca57); border-radius: 40px; padding: 8px; width: 80%; margin: 0 auto; cursor: pointer;'>
                <p style='color: white; font-weight: bold; margin: 0;'>🛒 طلب المنتج</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== منتجات SHEIN ==========
st.markdown("<h2 style='color: #feca57;'>🛍️ متجر SHEIN</h2>", unsafe_allow_html=True)

PRODUCTS = [
    {"name": "معطف مبطن بغطاء رأس للفتيات", "price": 19.39, "discount": 43, "link": "https://onelink.shein.com/38/5shrzfcizjmg", "sales": "150+"},
    {"name": "قميص أنيق بتصميم هونج كونج", "price": 14.18, "discount": 37, "link": "https://onelink.shein.com/38/5shune7n90yf", "sales": "200+"},
    {"name": "نظارات حفلات مطبوعة 6 قطع", "price": 2.70, "discount": 0, "link": "https://onelink.shein.com/38/5shujg5f2ywk", "sales": "300+"},
    {"name": "حقيبة مستلزمات سفر مقاومة للماء", "price": 3.90, "discount": 17, "link": "https://onelink.shein.com/38/5shuimjyfjt7", "sales": "100+"},
]

cols = st.columns(4)
for i, product in enumerate(PRODUCTS[:8]):
    with cols[i % 4]:
        final_price = product['price'] * (1 - product['discount']/100) if product['discount'] > 0 else product['price']
        
        st.markdown(f"""
        <div style='border-radius: 25px; padding: 18px; margin-bottom: 20px; background: linear-gradient(135deg, #ffffff, #f1f5f9); box-shadow: 0 10px 25px rgba(0,0,0,0.1); transition: 0.3s;'>
            <h4 style='font-size: 16px; color: #1e293b; margin-bottom: 10px;'>{product['name']}</h4>
            <p style='color: #ff4757; font-size: 24px; font-weight: bold; margin-bottom: 8px;'>💰 ${final_price:.2f}</p>
            <p style='color: #2ecc71; font-weight: bold; margin-bottom: 12px;'>📦 تم البيع: {product['sales']}</p>
            <a href='{product['link']}' target='_blank' style='text-decoration: none;'>
                <div style='background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 40px; padding: 10px; text-align: center; cursor: pointer; font-weight: bold; color: white;'>
                    🛒 تسوق الآن
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== ريلز وفيديوهات ==========
st.markdown("<h2 style='color: #feca57;'>📹 ريلز وفيديوهات تسويقية</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b, #0f172a); border-radius: 25px; padding: 25px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.2);'>
        <h3 style='color: #feca57;'>🎬 فيديو تعريفي بـ Saeed DaTaBoT</h3>
        <div style='background: rgba(255,255,255,0.05); border-radius: 20px; padding: 50px; margin-top: 15px;'>
            <p style='color: #aaa;'>📹 ريلز قادم قريباً...</p>
            <p style='color: #ff6b6b;'>اشترك في القناة لمشاهدة المحتوى الحصري</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b, #0f172a); border-radius: 25px; padding: 25px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.2);'>
        <h3 style='color: #feca57;'>📸 صور المنتجات</h3>
        <div style='background: rgba(255,255,255,0.05); border-radius: 20px; padding: 50px; margin-top: 15px;'>
            <p style='color: #aaa;'>🖼️ معرض الصور قيد التجهيز...</p>
            <p style='color: #ff6b6b;'>سيكون متاحاً قريباً</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ========== بوت الدردشة الذكي ==========
st.markdown("<h2 style='color: #feca57;'>💬 تحدث مع Saeed DaTaBoT</h2>", unsafe_allow_html=True)

chat_question = st.text_area("ماذا تريد أن تسأل المساعد الشخصي لسعيد؟", placeholder="اكتب سؤالك هنا...")

if st.button("💬 أرسل"):
    if chat_question and model:
        with st.spinner("🤖 Saeed DaTaBoT يفكر..."):
            try:
                system_prompt = f"""
                أنت Saeed DaTaBoT، المساعد الشخصي الذكي لسعيد المسوري.
                تم برمجتك بواسطة سعيد المسوري وبمساعدة الذكاء الاصطناعي.
                
                مهمتك:
                1. التعريف بنفسك وبسعيد المسوري
                2. مساعدة المستخدمين في التسوق والتسويق الرقمي
                3. تشجيع المنتجات اليمنية
                4. تقديم النصائح الحياتية والمهنية
                5. الرد بود واحترام بأسلوب يمني أصيل
                
                سؤال المستخدم: {chat_question}
                """
                response = model.generate_content(system_prompt)
                st.success(f"**🤖 Saeed DaTaBoT يقول:**\n\n{response.text}")
                
                tts = gTTS(text=response.text[:500], lang='ar')
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format='audio/mp3')
                
            except Exception as e:
                st.error(f"خطأ: {e}")
    else:
        st.warning("يرجى كتابة سؤالك أولاً أو التحقق من المفتاح")

st.markdown("---")

# ========== السايدبار ==========
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 30px; margin-bottom: 20px;'>
        <h2 style='color: #feca57;'>🤖 Saeed DaTaBoT</h2>
        <p style='color: #aaa;'>المساعد الشخصي</p>
        <p style='color: #ff6b6b;'>لـ سعيد المسوري</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 خدماتي:")
    st.markdown("""
    - ✅ تحليل الروابط
    - ✅ التسويق الرقمي
    - ✅ دعم المنتجات اليمنية
    - ✅ إنشاء ريلز وصور
    - ✅ محادثة ذكية
    - ✅ تحويل النص إلى صوت
    - ✅ إرسال رسائل تليجرام
    """)
    st.markdown("---")
    st.markdown("### 📞 للتواصل:")
    st.markdown("- @SaeedMarketAds")
    st.markdown("- @SaeedDataBot")
    st.markdown("---")
    st.markdown("### 🚀 رؤيتنا:")
    st.markdown("""
    *"نسوق لمنتجاتك بأحدث تقنيات الذكاء الاصطناعي*  
    *ونوصل صوتك للعالم*  
    *ونبني معاً مستقبل التسويق الرقمي في اليمن"*
    """)
    st.markdown("---")
    st.caption("© 2026 Saeed DaTaBoT - جميع الحقوق محفوظة")
    st.caption("برمجة وتطوير: سعيد المسوري")

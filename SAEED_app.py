import streamlit as st
import os
import google.generativeai as genai
import requests
import base64
from gtts import gTTS
import io

# ========== إعداد الصفحة ==========
st.set_page_config(page_title="Saeed DaTaBoT | سوق سعيد", page_icon="🤖", layout="wide")

# ========== تصميم خلفية الواجهة ==========
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0.2);
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
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 30px; margin-bottom: 30px;'>
    <h1 style='color: #fff; font-size: 48px;'>🤖 Saeed DaTaBoT</h1>
    <p style='color: #aaa; font-size: 20px;'>المساعد الشخصي لـ <span style='color: #ff6b6b;'>سعيد المسوري</span></p>
    <p style='color: #aaa;'>تم البرمجة بواسطة سعيد المسوري وبمساعدة الذكاء الاصطناعي 🚀</p>
    <div style='background: rgba(255,255,255,0.1); border-radius: 20px; padding: 15px; margin-top: 15px;'>
        <p style='color: #feca57;'>🇾🇪 دعم المنتجات اليمنية - التسويق الرقمي - ريلز - صور - فيديوهات 🇾🇪</p>
        <p style='color: #2ecc71;'>💪 معاً نوقف أطفال المدارس من التسول ونسجلهم في التعليم</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== تحليل الروابط ==========
st.subheader("🔗 تحليل الروابط والمساعدة الذكية")

url_input = st.text_input("أرسل رابط المنتج أو الموقع هنا (SHEIN, AliExpress, Noon, أو أي رابط):")

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
            <div style='background: #16213e; border-radius: 20px; padding: 20px; border-right: 5px solid #ff6b6b;'>
                <h4 style='color: #feca57;'>📊 نتيجة التحليل:</h4>
                <p style='color: #fff;'>{response.text}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # تحويل النص إلى صوت
            tts = gTTS(text=response.text[:500], lang='ar')
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format='audio/mp3')
            
        except Exception as e:
            st.error(f"خطأ في التحليل: {e}")

st.markdown("---")

# ========== منتجات يمنية (واجهة جديدة) ==========
st.subheader("🇾🇪 منتجات يمنية - دعم الصناعة المحلية 🇾🇪")

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
        <div style='background: linear-gradient(135deg, #1a472a, #2e7d32); border-radius: 20px; padding: 15px; text-align: center;'>
            <h1 style='font-size: 48px;'>{product['image']}</h1>
            <h3 style='color: #feca57;'>{product['name']}</h3>
            <p style='color: #aaa;'>{product['desc']}</p>
            <p style='color: #ff6b6b; font-size: 24px; font-weight: bold;'>{product['price']}</p>
            <button style='background: #ff6b6b; border: none; padding: 10px 20px; border-radius: 30px; color: white; cursor: pointer;'>
                🛒 طلب المنتج
            </button>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== منتجات SHEIN المحسّنة ==========
st.subheader(f"🛍️ متجر SHEIN")

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
        <div style='border-radius: 20px; padding: 15px; margin-bottom: 15px; background: linear-gradient(135deg, #fff, #f8f9fa); box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: 0.3s;'>
            <h4 style='font-size: 16px; color: #1e2a3e;'>{product['name']}</h4>
            <p style='color: #ff4757; font-size: 22px; font-weight: bold;'>💰 ${final_price:.2f}</p>
            <p style='color: #2ecc71; font-weight: bold;'>📦 تم البيع: {product['sales']}</p>
            <a href='{product['link']}' target='_blank'>
                <button style='background: linear-gradient(90deg, #667eea, #764ba2); color: white; border: none; padding: 10px; width: 100%; border-radius: 30px; cursor: pointer; font-weight: bold;'>
                    🛒 تسوق الآن
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== ريلز وفيديوهات تسويقية ==========
st.subheader("📹 ريلز وفيديوهات تسويقية")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style='background: #1a1a2e; border-radius: 20px; padding: 15px; text-align: center;'>
        <h3>🎬 فيديو تعريفي بـ Saeed DaTaBoT</h3>
        <div style='background: #16213e; border-radius: 15px; padding: 40px;'>
            <p style='color: #aaa;'>📹 ريلز قادم قريباً...</p>
            <p style='color: #feca57;'>اشترك في القناة لمشاهدة المحتوى الحصري</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: #1a1a2e; border-radius: 20px; padding: 15px; text-align: center;'>
        <h3>📸 صور المنتجات</h3>
        <div style='background: #16213e; border-radius: 15px; padding: 40px;'>
            <p style='color: #aaa;'>🖼️ معرض الصور قيد التجهيز...</p>
            <p style='color: #feca57;'>سيكون متاحاً قريباً</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ========== بوت الدردشة الذكي ==========
st.subheader("💬 تحدث مع Saeed DaTaBoT")

chat_question = st.text_area("ماذا تريد أن تسأل المساعد الشخصي لسعيد؟")

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
                
                # تحويل الرد إلى صوت
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
    st.image("https://via.placeholder.com/300x100?text=Saeed+DaTaBoT", use_container_width=True)
    st.markdown("## 🤖 Saeed DaTaBoT")
    st.markdown("### المساعد الشخصي لسعيد المسوري")
    st.markdown("---")
    st.markdown("""
    ### 🎯 خدماتي:
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
    st.markdown("### 🇾🇪 رسالة أمل:")
    st.markdown("""
    *"معاً نوقف أطفال المدارس من التسول*  
    *ونسجلهم في التعليم*  
    *ونبني يمن جديد"*
    """)
    st.markdown("---")
    st.caption("© 2026 Saeed DaTaBoT - جميع الحقوق محفوظة")
    st.caption("برمجة وتطوير: سعيد المسوري")

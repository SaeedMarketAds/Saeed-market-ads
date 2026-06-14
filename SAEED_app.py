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

# ========== كود خصم SHEIN ==========
st.markdown("""
<div style='background: linear-gradient(135deg, #ff6b6b, #feca57); padding: 30px; border-radius: 30px; text-align: center; margin-bottom: 30px; box-shadow: 0 15px 30px rgba(0,0,0,0.2);'>
    <h2 style='color: #fff; margin-bottom: 10px;'>🎁 عرض خاص للمستخدمين الجدد 🎁</h2>
    <div style='background: white; display: inline-block; padding: 15px 40px; border-radius: 60px; margin: 15px 0;'>
        <h1 style='color: #ff6b6b; margin: 0; font-size: 48px;'>🏷️ WL7KA</h1>
    </div>
    <p style='color: #fff; font-size: 20px; margin: 0;'>🔥 خصم يصل إلى 60% على أول طلب من SHEIN 🔥</p>
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

# ========== منتجات SHEIN الـ 51 ==========
st.markdown(f"<h2 style='color: #feca57;'>🛍️ متجر SHEIN - 51 منتج 🛍️</h2>", unsafe_allow_html=True)

# جميع المنتجات الـ 51 كاملة
PRODUCTS = [
    {"name": "معطف مبطن بغطاء رأس للفتيات", "price": 19.39, "discount": 43, "link": "https://onelink.shein.com/38/5shrzfcizjmg", "sales": "150+"},
    {"name": "قميص أنيق بتصميم هونج كونج", "price": 14.18, "discount": 37, "link": "https://onelink.shein.com/38/5shune7n90yf", "sales": "200+"},
    {"name": "نظارات حفلات مطبوعة 6 قطع", "price": 2.70, "discount": 0, "link": "https://onelink.shein.com/38/5shujg5f2ywk", "sales": "300+"},
    {"name": "حقيبة مستلزمات سفر مقاومة للماء", "price": 3.90, "discount": 17, "link": "https://onelink.shein.com/38/5shuimjyfjt7", "sales": "100+"},
    {"name": "معطف رجالي كاجوال سادة", "price": 25.67, "discount": 24, "link": "https://onelink.shein.com/38/5shui8qqn60h", "sales": "200+"},
    {"name": "أقراط زهرية بتصميم لافت", "price": 1.44, "discount": 4, "link": "https://onelink.shein.com/38/5shtox57cemc", "sales": "300+"},
    {"name": "ربطات شعر ملونة 5 قطع", "price": 1.50, "discount": 38, "link": "https://onelink.shein.com/38/5shtobfv3sxn", "sales": "800+"},
    {"name": "أحذية رياضية نسائية كاجوال", "price": 5.00, "discount": 82, "link": "https://onelink.shein.com/38/5shtl502kmcf", "sales": "200+"},
    {"name": "مجموعة خواتم زهور وردية", "price": 2.16, "discount": 6, "link": "https://onelink.shein.com/38/5shtkl9rhh8f", "sales": "500+"},
    {"name": "دلو أرز مع كوب قياس", "price": 8.84, "discount": 70, "link": "https://onelink.shein.com/38/5shtjtnbwphj", "sales": "200+"},
    {"name": "أقراط هوب مطلية بالذهب 3 أزواج", "price": 1.43, "discount": 5, "link": "https://onelink.shein.com/38/5shti8ffmexk", "sales": "50+"},
    {"name": "شعر مستعار قصير مجعد", "price": 2.70, "discount": 33, "link": "https://onelink.shein.com/38/5shthyka1fts", "sales": "100+"},
    {"name": "حذاء تزلج بإضاءة LED للأطفال", "price": 34.72, "discount": 37, "link": "https://onelink.shein.com/38/5shthetyxlby", "sales": "50+"},
    {"name": "طقم مقص أظافر احترافي", "price": 1.40, "discount": 36, "link": "https://onelink.shein.com/38/5shtg7fahsfp", "sales": "1200+"},
    {"name": "هاتف لعبة موسيقي تعليمي", "price": 3.40, "discount": 0, "link": "https://onelink.shein.com/38/5shtfvl3s22n", "sales": "50+"},
    {"name": "شريط إضاءة RGB LED", "price": 2.27, "discount": 55, "link": "https://onelink.shein.com/38/5shtfbusmt15", "sales": "200+"},
    {"name": "طقم بيسبول للأولاد", "price": 3.28, "discount": 80, "link": "https://onelink.shein.com/38/5shtek8d4572", "sales": "100+"},
    {"name": "شريط لاصق مزدوج قوي", "price": 1.05, "discount": 30, "link": "https://onelink.shein.com/38/5shtead7hrfl", "sales": "800+"},
    {"name": "طبق طعام محكم الإغلاق 24 قطعة", "price": 7.14, "discount": 60, "link": "https://onelink.shein.com/38/5shtdonvakbf", "sales": "150+"},
    {"name": "حقيبة شاطئ كبيرة السعة", "price": 2.34, "discount": 57, "link": "https://onelink.shein.com/38/5shtcj87y44e", "sales": "100+"},
    {"name": "طقم بيجامة صيفية للأولاد", "price": 6.19, "discount": 42, "link": "https://onelink.shein.com/38/5shtc1gxxmda", "sales": "600+"},
    {"name": "أظافر صناعية فرنسية 24 قطعة", "price": 1.35, "discount": 41, "link": "https://onelink.shein.com/38/5sht8yz7kfv1", "sales": "200+"},
    {"name": "تيشيرت مدرسي بقوس وردي", "price": 4.09, "discount": 47, "link": "https://onelink.shein.com/38/5sht8r3347y5", "sales": "800+"},
    {"name": "حامل هاتف قابل للطي محمول", "price": 1.30, "discount": 24, "link": "https://onelink.shein.com/38/5sht5cr65itw", "sales": "100+"},
    {"name": "طقم مناشف مخططة سريعة الجفاف", "price": 2.34, "discount": 38, "link": "https://onelink.shein.com/38/5sht12urdy18", "sales": "200+"},
    {"name": "شريط مانع لتسرب المياه", "price": 1.70, "discount": 0, "link": "https://onelink.shein.com/38/5sht0h5f61jc", "sales": "300+"},
    {"name": "مقص دجاج متعدد الاستخدامات", "price": 2.70, "discount": 23, "link": "https://onelink.shein.com/38/5shszze54ug2", "sales": "300+"},
    {"name": "طقم قميص وبنطلون رجالي", "price": 7.77, "discount": 70, "link": "https://onelink.shein.com/38/5shsz9qqou3d", "sales": "50+"},
    {"name": "طقم موس حاجب 30 قطعة", "price": 0.75, "discount": 32, "link": "https://onelink.shein.com/38/5shsyi4b2nub", "sales": "500+"},
    {"name": "فرجار رقمي 6 بوصة", "price": 1.71, "discount": 10, "link": "https://onelink.shein.com/38/5shsxydzzinl", "sales": "200+"},
    {"name": "حزام رجالي بإبزيم أوتوماتيكي", "price": 2.93, "discount": 38, "link": "https://onelink.shein.com/38/5shsxapmkr2h", "sales": "500+"},
    {"name": "شفاطات لامعة قابلة لإعادة الاستخدام", "price": 0.99, "discount": 18, "link": "https://onelink.shein.com/38/5shswb72kgum", "sales": "600+"},
    {"name": "واقي شاشة ضد التجسس", "price": 1.63, "discount": 49, "link": "https://onelink.shein.com/38/5shsw790bnla", "sales": "800+"},
    {"name": "مشط قابل للطي مع مرآة", "price": 1.90, "discount": 32, "link": "https://onelink.shein.com/38/5shsw1bwzhq8", "sales": "800+"},
    {"name": "لعبة ضغط بيضاوية مخططة", "price": 2.97, "discount": 10, "link": "https://onelink.shein.com/38/5shsvxdus31c", "sales": "200+"},
    {"name": "حزام كلب مبطن وعاكس", "price": 3.30, "discount": 25, "link": "https://onelink.shein.com/38/5shsvrgrgmbu", "sales": "50+"},
    {"name": "غطاء حماية شاحن 3 قطع", "price": 1.13, "discount": 25, "link": "https://onelink.shein.com/38/5shsvboiirzh", "sales": "900+"},
    {"name": "طقم فرش مكياج 3 قطع", "price": 1.05, "discount": 48, "link": "https://onelink.shein.com/38/5shsv5rf6m2j", "sales": "1000+"},
    {"name": "فاتحة علب 4 في 1", "price": 1.08, "discount": 23, "link": "https://onelink.shein.com/38/5shsuk22y0h7", "sales": "200+"},
    {"name": "شارة أنمي دبوس", "price": 1.65, "discount": 21, "link": "https://onelink.shein.com/38/5shstycqq3uz", "sales": "100+"},
    {"name": "رأس دش مطري عالي الضغط", "price": 12.64, "discount": 65, "link": "https://onelink.shein.com/38/5shst4ra0l06", "sales": "200+"},
    {"name": "مكواة فرد وتجعيد شعر سيراميك", "price": 26.90, "discount": 20, "link": "https://onelink.shein.com/38/5shsrzbmou3o", "sales": "100+"},
    {"name": "زجاجة رش زيت للطبخ", "price": 1.17, "discount": 22, "link": "https://onelink.shein.com/38/5shsrvdkg0tg", "sales": "500+"},
    {"name": "مشابك تثبيت لحاف 4 قطع", "price": 3.33, "discount": 5, "link": "https://onelink.shein.com/38/5shsrnhfz3p0", "sales": "200+"},
    {"name": "نظارات حجب الضوء الأزرق", "price": 5.22, "discount": 50, "link": "https://onelink.shein.com/38/5shsqvv0f19e", "sales": "100+"},
    {"name": "أداة تقليم القدم", "price": 1.10, "discount": 8, "link": "https://onelink.shein.com/38/5shspqfd1vtf", "sales": "300+"},
    {"name": "أساور خرز خشبي", "price": 1.80, "discount": 25, "link": "https://onelink.shein.com/38/5shsp8o323az", "sales": "100+"},
    {"name": "ورق زبدة للمقلاة الهوائية", "price": 1.26, "discount": 21, "link": "https://onelink.shein.com/38/5shsof2mdyzs", "sales": "300+"},
    {"name": "أظافر فرنسية للمانيكير 48 قطعة", "price": 1.30, "discount": 35, "link": "https://onelink.shein.com/38/5shso76hvn95", "sales": "300+"},
    {"name": "سوار ساعة أبل جلد أصلي", "price": 5.89, "discount": 5, "link": "https://onelink.shein.com/38/5shs5kbzkzl4", "sales": "100+"},
    {"name": "حمالة هاتف فراشة مع كريستال", "price": 2.48, "discount": 25, "link": "https://onelink.shein.com/38/5shs5gdxezhw", "sales": "150+"},
]

# عرض المنتجات في شبكة 4 أعمدة
cols = st.columns(4)
for i, product in enumerate(PRODUCTS):
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

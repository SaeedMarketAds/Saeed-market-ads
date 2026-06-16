import streamlit as st
import os
import google.generativeai as genai
import requests
import base64
from gtts import gTTS
import io
from datetime import datetime

# ========== إعداد الصفحة ==========
st.set_page_config(page_title="Saeed DaTaBoT | سوق سعيد", page_icon="🤖", layout="wide")

# ========== تعريف دالة فحص الروابط (مهمة جداً) ==========
@st.cache_data(ttl=3600)  # تخزين النتيجة لمدة ساعة لتسريع الأداء
def is_product_available(url):
    """
    تتحقق هذه الدالة من توفر المنتج قبل عرض زر الشراء
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, timeout=8, headers=headers)
        
        # فحص إذا كان المنتج غير متوفر
        unavailable_indicators = [
            "sold out", "out of stock", "غير متوفر", "نفدت الكمية",
            "unavailable", "not available", "404", "product not found"
        ]
        
        response_lower = response.text.lower()
        for indicator in unavailable_indicators:
            if indicator in response_lower:
                return False
        
        # إذا كان كود الاستجابة 200 ولم نجد مؤشرات عدم توفر
        return response.status_code == 200
        
    except requests.RequestException as e:
        print(f"خطأ في فحص الرابط {url}: {e}")
        return False  # في حالة الخطأ نعتبر المنتج غير متوفر احترازياً

# ========== تصميم خلفية الواجهة الاحترافية ==========
page_bg = """
<style>
/* تنسيق الخلفية الرئيسية */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0.2);
}

/* تنسيق الأزرار */
.stButton > button {
    background: linear-gradient(90deg, #ff6b6b, #feca57);
    color: white;
    border: none;
    border-radius: 30px;
    padding: 10px 25px;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #feca57, #ff6b6b);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

/* تنسيق حقول الإدخال */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.1);
    color: white;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.2);
}
.stTextInput > div > div > input:focus {
    border-color: #feca57;
    box-shadow: 0 0 10px rgba(254,202,87,0.3);
}

/* تنسيق حقل النص */
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.1);
    color: white;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.2);
}

/* تنسيق التحذيرات */
.stAlert {
    border-radius: 15px;
    border-right: 5px solid #ff6b6b;
}

/* إخفاء شريط التنقل العلوي لبعض العناصر */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* بطاقات المنتجات الموحدة */
.product-card {
    border-radius: 25px;
    padding: 20px;
    margin-bottom: 25px;
    background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(245,245,255,0.95));
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
    min-height: 300px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    backdrop-filter: blur(5px);
}
.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}

/* تنسيق الزر داخل البطاقة */
.product-btn {
    background: linear-gradient(90deg, #667eea, #764ba2);
    border-radius: 40px;
    padding: 12px;
    text-align: center;
    cursor: pointer;
    font-weight: bold;
    color: white;
    transition: all 0.3s ease;
    border: none;
    width: 100%;
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
    width: 100%;
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
    st.warning(f"⚠️ بعض المفاتيح غير متوفرة: {e}")

# ========== إعداد Gemini ==========
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-3.5-flash')
except Exception as e:
    model = None
    st.warning("⚠️ Gemini AI غير متوفر حالياً")

# دالة سريعة للرد بدون تأخير
def quick_response(question):
    question_lower = question.lower()
    
    # ردود سريعة مسبقة للأسئلة الشائعة
    if "من أنت" in question or "من انت" in question or "عرف نفسك" in question:
        return """وعليكم السلام ورحمة الله وبركاتة 🤖

أنا **Saeed DaTaBoT**، المساعد الشخصي الذكي لـ **سعيد المسوري**.

تم برمجتي بواسطة سعيد المسوري وبمساعدة أحدث تقنيات الذكاء الاصطناعي.

**مهامي الأساسية:**
• 🔗 تحليل الروابط والمنتجات
• 🛍️ مساعدتك في التسوق من SHEIN و AliExpress
• 🇾🇪 دعم المنتجات اليمنية
• 📹 إنشاء محتوى تسويقي (ريلز - صور - فيديوهات)
• 💬 محادثة ذكية للإجابة على استفساراتك

كيف يمكنني مساعدتك اليوم؟ 😊"""
    
    elif "السلام" in question or "اهلا" in question or "مرحبا" in question:
        return """وعليكم السلام ورحمة الله وبركاتة 🌹

أهلاً وسهلاً بك! أنا Saeed DaTaBoT في خدمتك.

ماذا تحتاج اليوم؟ هل تريد:
- تحليل رابط منتج؟
- مساعدة في التسوق؟
- معلومات عن عروض SHEIN؟
- أو أي استفسار آخر؟

أنا هنا لمساعدتك 😊"""
    
    elif "كود الخصم" in question or "خصم" in question or "كود" in question:
        return """🎁 **كود خصم SHEIN الحصري** 🎁

🏷️ **الكود: WL7KA**

🔥 **مميزات الكود:**
• خصم يصل إلى 60% على أول طلب
• ساري على جميع منتجات SHEIN
• يمكن استخدامه مع العروض الأخرى

**كيف تستخدم الكود؟**
1. اختر منتجاتك من SHEIN
2. اذهب إلى سلة المشتريات
3. أدخل الكود **WL7KA** في خانة الرموز الترويجية
4. استمتع بالخصم فوراً!

هل تريد مساعدة في اختيار المنتجات؟ 😊"""
    
    elif "شكرا" in question or "thank" in question:
        return """العفو، هذا واجبي 🤍

شكراً لثقتك بـ Saeed DaTaBoT. أنا في خدمتك دائماً.

هل تحتاج أي مساعدة أخرى؟ 😊"""
    
    return None

# ========== تعريف البوت ==========
st.markdown("""
<div style='text-align: center; padding: 50px; background: linear-gradient(135deg, rgba(26,26,46,0.9), rgba(22,33,62,0.9)); border-radius: 50px; margin-bottom: 30px; box-shadow: 0 25px 50px rgba(0,0,0,0.3); backdrop-filter: blur(10px);'>
    <h1 style='color: #fff; font-size: 64px; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>🤖 Saeed DaTaBoT</h1>
    <p style='color: #ddd; font-size: 24px;'>المساعد الشخصي لـ <span style='color: #ff6b6b; font-weight: bold;'>سعيد المسوري</span></p>
    <p style='color: #aaa; font-size: 18px;'>تم البرمجة بواسطة سعيد المسوري وبمساعدة الذكاء الاصطناعي 🚀</p>
    <div style='background: rgba(255,255,255,0.1); border-radius: 40px; padding: 20px; margin-top: 25px;'>
        <p style='color: #feca57; font-size: 20px;'>🇾🇪 دعم المنتجات اليمنية | التسويق الرقمي | ريلز | صور | فيديوهات 🇾🇪</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== كود خصم SHEIN بارز جداً ==========
st.markdown("""
<div style='background: linear-gradient(135deg, #ff0844, #ffb199); padding: 60px 30px; border-radius: 60px; text-align: center; margin-bottom: 40px; box-shadow: 0 30px 60px rgba(0,0,0,0.3);'>
    <h1 style='color: #fff; margin-bottom: 15px; font-size: 38px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>🎁 عرض خاص للمستخدمين الجدد 🎁</h1>
    <div style='background: white; display: inline-block; padding: 25px 70px; border-radius: 100px; margin: 25px 0; box-shadow: 0 15px 40px rgba(0,0,0,0.2);'>
        <h1 style='color: #ff0844; margin: 0; font-size: 72px; letter-spacing: 8px;'>🏷️ WL7KA</h1>
    </div>
    <p style='color: #fff; font-size: 32px; margin: 15px 0 0 0; font-weight: bold;'>🔥 خصم يصل إلى 60% على أول طلب من SHEIN 🔥</p>
    <p style='color: #fff; font-size: 22px; margin-top: 15px;'>✨ استخدم الكود الآن ووفر أكثر ✨</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== تحليل الروابط (سريع) ==========
st.markdown("<h2 style='color: #feca57; text-align: center; font-size: 36px;'>🔗 تحليل الروابط والمساعدة الذكية</h2>", unsafe_allow_html=True)

url_input = st.text_input("📎 أرسل رابط المنتج أو الموقع هنا (SHEIN, AliExpress, Noon, أو أي رابط):", placeholder="https://...")

if url_input:
    with st.spinner("🤖 جاري تحليل الرابط..."):
        # أولاً نفحص توفر المنتج
        is_available = is_product_available(url_input)
        
        if model:
            try:
                analysis_prompt = f"""
                أنت Saeed DaTaBoT. رد بسرعة وبثقة.
                قم بتحليل هذا الرابط باختصار: {url_input}
                
                أجب بشكل مباشر وسريع:
                1. نوع الرابط
                2. فائدته
                3. نصيحة سريعة
                """
                response = model.generate_content(analysis_prompt)
                
                # عرض نتيجة التحليل مع حالة التوفر
                availability_status = "✅ **متوفر**" if is_available else "❌ **غير متوفر حالياً**"
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 30px; padding: 30px; border-right: 6px solid #ff6b6b; box-shadow: 0 15px 30px rgba(0,0,0,0.2);'>
                    <h4 style='color: #feca57; margin-bottom: 15px;'>🤖 Saeed DaTaBoT يرد:</h4>
                    <p style='color: #e2e8f0; line-height: 1.8; font-size: 16px;'>{response.text}</p>
                    <hr style='border-color: rgba(255,255,255,0.1);'>
                    <p style='color: #2ecc71; font-size: 18px;'><strong>📦 حالة المنتج:</strong> {availability_status}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # تحويل النص إلى صوت
                try:
                    tts = gTTS(text=response.text[:300], lang='ar')
                    audio_bytes = io.BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    st.audio(audio_bytes, format='audio/mp3')
                except:
                    pass
            except Exception as e:
                st.error(f"خطأ في التحليل: {e}")
        else:
            st.info("🤖 Gemini AI غير متوفر حالياً، لا يمكن تحليل الرابط.")

st.markdown("---")

# ========== منتجات SHEIN (51 منتج) ==========
st.markdown(f"<h2 style='color: #feca57; text-align: center; font-size: 44px;'>🛍️ متجر SHEIN - 51 منتج 🛍️</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #ff6b6b; font-size: 26px; margin-bottom: 40px;'>✨ اكتشف أكثر من 50 منتج بأسعار خرافية ✨</p>", unsafe_allow_html=True)

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
        
        # فحص توفر المنتج قبل عرض الزر
        is_available = is_product_available(product['link'])
        
        if is_available:
            button_html = f"""
            <a href='{product['link']}' target='_blank' style='text-decoration: none;'>
                <div class='product-btn'>
                    🛒 تسوق الآن
                </div>
            </a>
            """
        else:
            button_html = """
            <div class='product-btn-disabled'>
                ⚠️ غير متوفر حالياً
            </div>
            """
        
        st.markdown(f"""
        <div class='product-card'>
            <div>
                <h4 style='font-size: 17px; color: #1e293b; margin-bottom: 12px; min-height: 50px;'>{product['name']}</h4>
                <p style='color: #ff4757; font-size: 28px; font-weight: bold; margin-bottom: 10px;'>💰 ${final_price:.2f}</p>
                <p style='color: #2ecc71; font-weight: bold; margin-bottom: 15px; font-size: 14px;'>📦 تم البيع: {product['sales']}</p>
                <p style='color: #ff6b6b; font-size: 12px;'>{'🔥 خصم ' + str(product['discount']) + '%' if product['discount'] > 0 else ''}</p>
            </div>
            {button_html}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== منتجات AliExpress (قادمة قريباً) ==========
st.markdown("""
<div style='text-align: center; padding: 60px; background: linear-gradient(135deg, rgba(255,107,107,0.2), rgba(254,202,87,0.2)); border-radius: 50px; margin: 30px 0; backdrop-filter: blur(5px);'>
    <h2 style='color: #feca57; font-size: 48px; margin-bottom: 20px;'>🛒 متجر AliExpress</h2>
    <div style='background: rgba(255,255,255,0.1); border-radius: 30px; padding: 40px;'>
        <p style='color: #ddd; font-size: 28px; margin-bottom: 15px;'>🚀 قادم قريباً جداً</p>
        <p style='color: #aaa; font-size: 18px;'>نستعد لإطلاق متجر AliExpress مع أفضل العروض والمنتجات</p>
        <p style='color: #ff6b6b; font-size: 20px; margin-top: 20px;'>✨ تابعونا للمزيد ✨</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== ريلز وفيديوهات ==========
st.markdown("<h2 style='color: #feca57; text-align: center; font-size: 36px;'>📹 ريلز وفيديوهات تسويقية</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b, #0f172a); border-radius: 30px; padding: 35px; text-align: center; box-shadow: 0 15px 30px rgba(0,0,0,0.2); min-height: 250px; display: flex; flex-direction: column; justify-content: center;'>
        <h3 style='color: #feca57; font-size: 28px;'>🎬 فيديو تعريفي بـ Saeed DaTaBoT</h3>
        <div style='background: rgba(255,255,255,0.05); border-radius: 25px; padding: 35px; margin-top: 20px;'>
            <p style='color: #aaa; font-size: 18px;'>📹 ريلز قادم قريباً...</p>
            <p style='color: #ff6b6b; font-size: 16px;'>اشترك في القناة لمشاهدة المحتوى الحصري</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b, #0f172a); border-radius: 30px; padding: 35px; text-align: center; box-shadow: 0 15px 30px rgba(0,0,0,0.2); min-height: 250px; display: flex; flex-direction: column; justify-content: center;'>
        <h3 style='color: #feca57; font-size: 28px;'>📸 صور المنتجات</h3>
        <div style='background: rgba(255,255,255,0.05); border-radius: 25px; padding: 35px; margin-top: 20px;'>
            <p style='color: #aaa; font-size: 18px;'>🖼️ معرض الصور قيد التجهيز...</p>
            <p style='color: #ff6b6b; font-size: 16px;'>سيكون متاحاً قريباً</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ========== بوت الدردشة الذكي ==========
st.markdown("<h2 style='color: #feca57; text-align: center; font-size: 36px;'>💬 تحدث مع Saeed DaTaBoT</h2>", unsafe_allow_html=True)

chat_question = st.text_area("📝 ماذا تريد أن تسأل المساعد الشخصي لسعيد؟", placeholder="اكتب سؤالك هنا...", height=120)

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    send_button = st.button("💬 أرسل", use_container_width=True)

if send_button and chat_question:
    if model:
        with st.spinner("🤖 Saeed DaTaBoT يرد..."):
            # التحقق من الرد السريع أولاً
            quick_ans = quick_response(chat_question)
            
            if quick_ans:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 30px; padding: 30px; border-right: 6px solid #2ecc71; box-shadow: 0 15px 30px rgba(0,0,0,0.2);'>
                    <h4 style='color: #feca57; margin-bottom: 15px;'>🤖 Saeed DaTaBoT يرد:</h4>
                    <p style='color: #e2e8f0; line-height: 1.8; font-size: 16px;'>{quick_ans}</p>
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
            else:
                try:
                    system_prompt = f"""
                    أنت Saeed DaTaBoT. رد بسرعة وبثقة.
                    ارد على هذا السؤال بشكل مباشر ومختصر: {chat_question}
                    """
                    response = model.generate_content(system_prompt)
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #1e2a3e, #0f172a); border-radius: 30px; padding: 30px; border-right: 6px solid #2ecc71; box-shadow: 0 15px 30px rgba(0,0,0,0.2);'>
                        <h4 style='color: #feca57; margin-bottom: 15px;'>🤖 Saeed DaTaBoT يرد:</h4>
                        <p style='color: #e2e8f0; line-height: 1.8; font-size: 16px;'>{response.text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    try:
                        tts = gTTS(text=response.text[:300], lang='ar')
                        audio_bytes = io.BytesIO()
                        tts.write_to_fp(audio_bytes)
                        audio_bytes.seek(0)
                        st.audio(audio_bytes, format='audio/mp3')
                    except:
                        pass
                except Exception as e:
                    st.error(f"خطأ: {e}")
    else:
        st.warning("⚠️ Gemini AI غير متوفر حالياً، يرجى المحاولة لاحقاً.")
elif send_button and not chat_question:
    st.warning("📝 يرجى كتابة سؤالك أولاً")

st.markdown("---")

# ========== السايدبار ==========
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 35px; margin-bottom: 25px;'>
        <h2 style='color: #feca57; margin-bottom: 10px;'>🤖 Saeed DaTaBoT</h2>
        <p style='color: #aaa;'>المساعد الشخصي</p>
        <p style='color: #ff6b6b; font-size: 18px;'>لـ سعيد المسوري</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎯 خدماتي:")
    st.markdown("""
    - ✅ تحليل الروابط
    - ✅ فحص توفر المنتجات
    - ✅ التسويق الرقمي
    - ✅ دعم المنتجات اليمنية
    - ✅ إنشاء ريلز وصور
    - ✅ محادثة ذكية
    - ✅ تحويل النص إلى صوت
    - ✅ إرسال رسائل تليجرام
    """)
    
    st.markdown("---")
    
    st.markdown("### 📞 للتواصل:")
    st.markdown("""
    - [@SaeedMarketAds](https://t.me/SaeedMarketAds)
    - [@SaeedDataBot](https://t.me/SaeedDataBot)
    """)
    
    st.markdown("---")
    
    st.markdown("### 🚀 رؤيتنا:")
    st.markdown("""
    > *"نسوق لمنتجاتك بأحدث تقنيات الذكاء الاصطناعي*  
    > *ونوصل صوتك للعالم*  
    > *ونبني معاً مستقبل التسويق الرقمي في اليمن"*
    """)
    
    st.markdown("---")
    
    # إحصائيات سريعة
    st.markdown("### 📊 إحصائيات سريعة:")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("🛍️ منتجات SHEIN", "51")
    with col_stat2:
        st.metric("💬 محادثات", "1000+")
    
    st.markdown("---")
    st.caption("© 2026 Saeed DaTaBoT - جميع الحقوق محفوظة")
    st.caption("برمجة وتطوير: سعيد المسوري")

import streamlit as st
import google.generativeai as genai
import gtts
from io import BytesIO
import base64
import re
import requests
from bs4 import BeautifulSoup

# ========== إعدادات البوت ==========
BOT_NAME = "Saeed DataBot"
OWNER_NAME = "سعيد المسوري"
SMART_SAEED = "سعيد الذكي"

# ========== إعداد Gemini ==========
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "ضع_مفتاحك_هنا")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ========== إعدادات الصوت ==========
def text_to_speech(text):
    """تحويل النص إلى صوت - نسخة محسنة"""
    try:
        # تنظيف النص من الإيموجيات والرموز التي قد تسبب مشاكل
        clean_text = re.sub(r'[^\w\s\.،!؟]', ' ', text)
        tts = gtts.gTTS(clean_text, lang="ar", slow=False)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        audio_base64 = base64.b64encode(audio_bytes.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    except Exception as e:
        print(f"خطأ في الصوت: {e}")
        return ""

def play_welcome_audio():
    """تشغيل صوت الترحيب"""
    try:
        with open("welcome_voice.mp3", "rb") as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    except:
        return text_to_speech("مرحباً بك في Saeed DataBot، أنا مساعدك الذكي")

# ========== قراءة الروابط (Scraper) ==========
def extract_product_from_url(url):
    """استخراج معلومات المنتج من الرابط"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        product_info = {
            'title': 'غير معروف',
            'price': 'غير معروف',
            'platform': 'غير معروف',
            'url': url
        }
        
        # تحديد المنصة من الرابط
        if 'noon.com' in url:
            product_info['platform'] = 'Noon'
            title_tag = soup.find('h1', class_=re.compile('product'))
            if title_tag:
                product_info['title'] = title_tag.text.strip()
            price_tag = soup.find('span', class_=re.compile('price'))
            if price_tag:
                product_info['price'] = price_tag.text.strip()
                
        elif 'aliexpress' in url:
            product_info['platform'] = 'AliExpress'
            title_tag = soup.find('h1', class_=re.compile('title'))
            if title_tag:
                product_info['title'] = title_tag.text.strip()
                
        elif 'shein' in url:
            product_info['platform'] = 'SHEIN'
            title_tag = soup.find('h1', class_=re.compile('product-name'))
            if title_tag:
                product_info['title'] = title_tag.text.strip()
        
        return product_info
        
    except Exception as e:
        return {'title': 'خطأ في قراءة الرابط', 'price': 'غير معروف', 'platform': 'غير معروف', 'url': url, 'error': str(e)}

def generate_post_from_url(url, platform, audience):
    """توليد منشور تسويقي من الرابط"""
    product_info = extract_product_from_url(url)
    
    prompt = f"""اكتب منشور تسويقي احترافي باللغة العربية لـ:
المنتج: {product_info['title']}
السعر: {product_info['price']}
المنصة: {platform or product_info['platform']}
الجمهور المستهدف: {audience or 'العملاء'}

المطلوب:
1. افتتاحية جذابة
2. وصف المنتج ومميزاته
3. إيموجيات مناسبة
4. هاشتاجات (3-5)
5. عبارة تحث على الشراء

المنشور:"""
    
    try:
        response = model.generate_content(prompt)
        return response.text, product_info
    except Exception as e:
        return f"⚠️ عذراً، حدث خطأ: {str(e)}", product_info

# ========== ردود البوت الذكية ==========
def get_bot_response(user_input):
    user_input_lower = user_input.lower().strip()
    
    # التحقق إذا كان المدخل رابطاً
    if user_input.startswith('http://') or user_input.startswith('https://'):
        with st.spinner("📡 جاري قراءة الرابط وتحليل المنتج..."):
            product_info = extract_product_from_url(user_input)
            if product_info.get('error'):
                return f"⚠️ عذراً، لم أتمكن من قراءة هذا الرابط. تأكد من أنه رابط صحيح من Noon أو AliExpress أو SHEIN.\n\nالخطأ: {product_info['error']}"
            else:
                prompt = f"""بناءً على هذا المنتج:
الاسم: {product_info['title']}
السعر: {product_info['price']}
المتجر: {product_info['platform']}

اكتب رداً ترحيبياً قصيراً يخبر المستخدم أنك وجدت المنتج، وتطلب منه إذا كان يريد منشوراً تسويقياً لهذا المنتج."""
                response = model.generate_content(prompt)
                return f"🔗 **تم قراءة الرابط بنجاح!**\n\n📦 **المنتج:** {product_info['title']}\n💰 **السعر:** {product_info['price']}\n🏪 **المتجر:** {product_info['platform']}\n\n{response.text}\n\n(اكتب 'منشور' لتوليد منشور تسويقي لهذا المنتج)"
    
    # ترحيب بالأسواق المختلفة
    if "سلام" in user_input_lower or "مرحباً" in user_input_lower:
        return "🎯 وعليكم السلام ورحمة الله! أنا Saeed DataBot، تحت أمرك. هل تريد عروض Noon، AliExpress، أو SHEIN؟"
    
    # من برمجك
    if "من برمجك" in user_input_lower:
        return f"🤖 أنا {BOT_NAME}، تم برمجتي بواسطة {OWNER_NAME} ({SMART_SAEED}) بمساعدة الذكاء الاصطناعي Gemini."
    
    # توليد منشور
    if "منشور" in user_input_lower or "بوست" in user_input_lower:
        if "last_url" in st.session_state and st.session_state.last_url:
            post, info = generate_post_from_url(st.session_state.last_url, None, None)
            return f"📝 **منشور تسويقي للمنتج:**\n\n{post}"
        else:
            return "📝 أريد رابط المنتج أولاً حتى أتمكن من كتابة منشور تسويقي له. أرسل لي رابطاً من Noon أو AliExpress أو SHEIN."
    
    # Noon
    if "noon" in user_input_lower:
        return "🛍️ **Noon** - أكبر سوق عربي!\n✅ خصومات تصل إلى 70%\n✅ توصيل سريع\n✅ منتجات أصلية\n\nأرسل لي رابط منتج وسأكتب لك منشوراً تسويقياً فوراً!"
    
    # AliExpress
    if "aliexpress" in user_input_lower or "علي اكسبرس" in user_input_lower:
        return "🌏 **AliExpress** - عالم من المنتجات!\n✅ أسعار المصنع\n✅ شحن دولي\n✅ حماية المشتري\n\nأرسل لي رابط المنتج الذي تريد الترويج له!"
    
    # SHEIN
    if "shein" in user_input_lower or "شي ان" in user_input_lower:
        return "👗 **SHEIN** - موضة وأزياء!\n✅ كود خصم 20%\n✅ توصيل سريع\n✅ أحدث الصيحات\n\nأرسل رابط المنتج وسأكتب منشوراً جذاباً!"
    
    # هاتف
    if "هاتف" in user_input_lower:
        return "📱 **عروض الهواتف في اليمن:**\n\n🔹 **LT** - هواتف اقتصادية من $60\n🔹 **Itel** - أداء ممتاز من $80\n🔹 **VIVO** - كاميرات احترافية من $120\n\n📍 متوفرة في **المركز الدولي للهواتف الذكية** مع ضمان.\n\nأي ماركة تهمك؟"
    
    # LT
    if "lt" in user_input_lower:
        return "📱 **هواتف LT:**\n• LT P10 - $80\n• LT X5 - $120\n• LT Pro Max - $200\n📍 متوفرة في المركز الدولي مع ضمان 6 شهور."
    
    # Itel
    if "itel" in user_input_lower:
        return "📱 **هواتف Itel:**\n• Itel A25 - $60\n• Itel P37 - $90\n• Itel S18 - $150\n📍 اقتصادية وعملية، متوفرة الآن."
    
    # VIVO
    if "vivo" in user_input_lower:
        return "📱 **هواتف VIVO:**\n• VIVO Y16 - $120\n• VIVO V25 - $250\n• VIVO X90 - $450\n📍 كاميرات رائعة، متوفرة في المركز الدولي."
    
    # رد افتراضي
    return f"🎯 أنا {BOT_NAME}، كيف أخدمك؟\n\n📌 **أرسل لي رابط منتج** من Noon, AliExpress, أو SHEIN وسأكتب لك منشوراً تسويقياً فوراً!\n\nأو اكتب:\n• Noon - لعروض noon\n• AliExpress - لعروض علي اكسبرس\n• SHEIN - لعروض شي ان\n• هاتف - لعروض الهواتف"

# ========== توليد منشور يدوي ==========
def generate_post(product, platform, audience):
    prompt = f"""اكتب منشور تسويقي احترافي بالعربية لـ:
المنتج: {product}
المنصة: {platform}
الجمهور: {audience}

المطلوب: نص جذاب مع إيموجيات وهاشتاجات."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "⚠️ عذراً، حدث خطأ. تأكد من مفتاح API."

# ========== الواجهة الرئيسية ==========
st.set_page_config(page_title="Saeed MarketAds", page_icon="🤖", layout="wide")

# تشغيل الصوت الترحيبي
if "welcome_played" not in st.session_state:
    audio_html = play_welcome_audio()
    if audio_html:
        st.markdown(audio_html, unsafe_allow_html=True)
    st.session_state.welcome_played = True

# عنوان الصفحة
st.markdown("""
<div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px;">
    <h1 style="color: white;">🤖 Saeed DataBot</h1>
    <p style="color: #e0e0e0;">صنع بواسطة سعيد المسوري | الذكاء الاصطناعي للتسويق والهواتف</p>
    <p style="color: #ffd700;">✨ أرسل رابط منتج وسأكتب لك منشوراً تسويقياً فوراً! ✨</p>
</div>
""", unsafe_allow_html=True)

# إنشاء التبويبات (Tabs)
tab1, tab2, tab3 = st.tabs(["🌍 التسويق بالعمولة", "📱 عرض الهواتف", "💬 تحدث مع البوت"])

# ========== TAB 1: التسويق بالعمولة ==========
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🛍️ تحليل المتاجر")
        st.info("🛒 **Noon** - خصومات تصل إلى 70%")
        st.info("🌏 **AliExpress** - شحن دولي مجاني")
        st.info("👗 **SHEIN** - كود خصم 20%")
        
        st.markdown("### 🔗 رابط المنتج")
        product_url = st.text_input("أدخل رابط المنتج من Noon, AliExpress, أو SHEIN", placeholder="https://www.noon.com/...")
        
        if product_url:
            st.session_state.last_url = product_url
            if st.button("📊 تحليل المنتج", use_container_width=True):
                with st.spinner("جاري قراءة الرابط..."):
                    info = extract_product_from_url(product_url)
                    st.session_state.bot_response = f"🔍 **نتيجة التحليل:**\n\n📦 المنتج: {info['title']}\n💰 السعر: {info['price']}\n🏪 المتجر: {info['platform']}\n\nهل تريد مني كتابة منشور تسويقي لهذا المنتج؟ اكتب 'منشور'"
    
    with col2:
        st.markdown("### ✍️ توليد المنشورات")
        product_name = st.text_input("اسم المنتج (بدون رابط)", placeholder="مثال: هاتف Samsung")
        platform = st.selectbox("المنصة", ["Facebook", "Instagram", "Twitter", "TikTok"])
        target_audience = st.text_input("الجمهور المستهدف", placeholder="مثال: شباب 18-25")
        
        if st.button("🚀 توليد منشور تسويقي", use_container_width=True):
            if product_name and platform:
                with st.spinner("جاري توليد منشور احترافي..."):
                    post = generate_post(product_name, platform, target_audience or "العملاء")
                st.success(post)
            else:
                st.warning("يرجى إدخال اسم المنتج")

# ========== TAB 2: عرض الهواتف ==========
with tab2:
    st.markdown("### 📱 المتاجر المحلية - الهواتف")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="border: 2px solid #667eea; border-radius: 15px; padding: 15px; text-align: center;">
            <h2 style="color: #667eea;">📱 LT</h2>
            <p>هواتف اقتصادية</p>
            <p>💰 LT P10: $80</p>
            <p>💰 LT X5: $120</p>
            <p>💰 LT Pro: $200</p>
            <p style="color: green;">✅ متوفر في المركز الدولي</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("استفسر عن LT"):
            st.session_state.bot_response = "📱 هواتف LT متوفرة في المركز الدولي للهواتف الذكية بأسعار تبدأ من $80 مع ضمان 6 شهور."
    
    with col2:
        st.markdown("""
        <div style="border: 2px solid #764ba2; border-radius: 15px; padding: 15px; text-align: center;">
            <h2 style="color: #764ba2;">📱 Itel</h2>
            <p>أداء ممتاز</p>
            <p>💰 Itel A25: $60</p>
            <p>💰 Itel P37: $90</p>
            <p>💰 Itel S18: $150</p>
            <p style="color: green;">✅ متوفر في المركز الدولي</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("استفسر عن Itel"):
            st.session_state.bot_response = "📱 هواتف Itel عملية واقتصادية، متوفرة في المركز الدولي للهواتف الذكية."
    
    with col3:
        st.markdown("""
        <div style="border: 2px solid #ff6b6b; border-radius: 15px; padding: 15px; text-align: center;">
            <h2 style="color: #ff6b6b;">📱 VIVO</h2>
            <p>كاميرات احترافية</p>
            <p>💰 VIVO Y16: $120</p>
            <p>💰 VIVO V25: $250</p>
            <p>💰 VIVO X90: $450</p>
            <p style="color: green;">✅ متوفر في المركز الدولي</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("استفسر عن VIVO"):
            st.session_state.bot_response = "📱 هواتف VIVO بتقنيات متطورة وكاميرات رائعة، متوفرة في المركز الدولي."
    
    st.divider()
    
    st.markdown("### 📦 إدارة المخزون")
    st.info("""
    | الماركة | الموديلات المتوفرة | الكمية |
    |---------|-------------------|--------|
    | **LT** | P10, X5, Pro Max | 28 قطعة |
    | **Itel** | A25, P37, S18 | 39 قطعة |
    | **VIVO** | Y16, V25, X90 | 19 قطعة |
    """)

# ========== TAB 3: محادثة البوت ==========
with tab3:
    st.markdown("### 💬 تحدث مع Saeed DataBot")
    
    # تهيئة سجل المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "🎯 مرحباً بك في Saeed DataBot!\n\n✨ **ميزة جديدة:** أرسل لي رابط منتج من Noon, AliExpress, أو SHEIN وسأكتب لك منشوراً تسويقياً فوراً! ✨\n\nأو اكتب:\n• Noon, AliExpress, SHEIN\n• هاتف, LT, Itel, VIVO"})
    
    if "bot_response" in st.session_state and st.session_state.bot_response:
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.bot_response})
        st.session_state.bot_response = None
    
    # عرض المحادثة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # إدخال المستخدم
    user_input = st.chat_input("✍️ اكتب سؤالك أو أرسل رابط المنتج هنا...")
    
    if user_input:
        # تخزين الرابط إذا وجد
        if user_input.startswith('http://') or user_input.startswith('https://'):
            st.session_state.last_url = user_input
        
        # إضافة رسالة المستخدم
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # الحصول على رد البوت
        with st.spinner("🤖 جاري التفكير..."):
            response = get_bot_response(user_input)
        
        # إضافة رد البوت
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
        
        # تشغيل الصوت
        audio_html = text_to_speech(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
        
        st.rerun()

# شريط جانبي للخصوصية
with st.sidebar:
    st.markdown("### 🔒 الخصوصية وسياسة الاستخدام")
    st.markdown("""
    **Saeed MarketAds**
    
    صنع بواسطة: **سعيد المسوري (سعيد الذكي)**
    
    - جميع البيانات مشفرة
    - لا نشارك معلوماتك
    - للتسويق بالعمولة فقط
    """)
    
    if st.button("🎵 تشغيل الترحيب الصوتي"):
        audio_html = play_welcome_audio()
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
    
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.clear()
        st.rerun()

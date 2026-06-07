import streamlit as st
import google.generativeai as genai
import gtts
from io import BytesIO
import base64
import re
import requests
from bs4 import BeautifulSoup

# ========== إعدادات البوت ==========
BOT_NAME = "Saeed DaTaBoT"
OWNER_NAME = "سعيد المسوري"
SMART_SAEED = "سعيد الذكي"

# ========== إعداد Gemini ==========
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "ضع_مفتاحك_هنا")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.5-flash')

# ========== إعدادات الصوت ==========
def text_to_speech(text):
    """تحويل النص إلى صوت"""
    try:
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
        return text_to_speech("السلام عليكم ورحمة الله وبركاته، أنا سعيد داتابوت، كيف أخدمك؟")

# ========== قراءة الروابط ==========
def extract_product_from_url(url):
    """استخراج معلومات المنتج من الرابط"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        product_info = {'title': 'غير معروف', 'price': 'غير معروف', 'platform': 'غير معروف', 'url': url}
        
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
        return {'title': 'خطأ في القراءة', 'price': 'غير معروف', 'platform': 'غير معروف', 'url': url, 'error': str(e)}

# ========== ردود البوت الذكية والمحترمة ==========
def get_bot_response(user_input):
    user_input_lower = user_input.lower().strip()
    
    # ====== ردود السلام المحترمة ======
    if "السلام عليكم" in user_input_lower or "سلام عليكم" in user_input_lower:
        return "وعليكم السلام ورحمة الله وبركاته، أنا Saeed DaTaBoT، مرحباً بك. كيف أقدر أساعدك اليوم؟"
    
    if "سلام" in user_input_lower and len(user_input_lower) < 10:
        return "وعليكم السلام ورحمة الله وبركاته، أهلاً بك."
    
    if "مرحباً" in user_input_lower or "اهلا" in user_input_lower:
        return "الله يحييك، مرحباً بك في Saeed DaTaBoT. كيف أخدمك؟"
    
    # ====== من برمجك ======
    if "من برمجك" in user_input_lower or "من برمجة" in user_input_lower or "who programmed" in user_input_lower:
        return f"أنا Saeed DaTaBoT، تم برمجتي بواسطة المبرمج القدير {OWNER_NAME} ({SMART_SAEED})، بمساعدة الذكاء الاصطناعي. أنا هنا لخدمتك."
    
    # ====== من أنت ======
    if "من انت" in user_input_lower or "who are you" in user_input_lower:
        return f"أنا Saeed DaTaBoT، مساعدك الذكي. برمجني {OWNER_NAME} ({SMART_SAEED}) لأخدمك في التسويق وشراء الهواتف. كيف أقدر أفيدك؟"
    
    # ====== التحقق من الرابط ======
    if user_input.startswith('http://') or user_input.startswith('https://'):
        product_info = extract_product_from_url(user_input)
        if product_info.get('error'):
            return f"عذراً، لم أتمكن من قراءة هذا الرابط. تأكد من أنه رابط صحيح من Noon أو AliExpress أو SHEIN."
        else:
            st.session_state.last_url = user_input
            return f"""تم قراءة الرابط بنجاح ✅

📦 **المنتج:** {product_info['title']}
💰 **السعر:** {product_info['price']}
🏪 **المتجر:** {product_info['platform']}

هل تريد مني كتابة منشور تسويقي لهذا المنتج؟ اكتب "منشور" وسأقوم بذلك فوراً."""
    
    # ====== توليد منشور ======
    if "منشور" in user_input_lower or "بوست" in user_input_lower:
        if "last_url" in st.session_state and st.session_state.last_url:
            product_info = extract_product_from_url(st.session_state.last_url)
            prompt = f"""اكتب منشور تسويقي احترافي وجذاب باللغة العربية لهذا المنتج:
المنتج: {product_info['title']}
السعر: {product_info['price']}
المتجر: {product_info['platform']}

المطلوب: نص قصير وجذاب مع إيموجيات وهاشتاجات مناسبة."""
            try:
                response = model.generate_content(prompt)
                return f"📝 هذا منشور تسويقي مقترح:\n\n{response.text}"
            except:
                return "عذراً، حدث خطأ في توليد المنشور. حاول مرة أخرى."
        else:
            return "أرسل لي رابط المنتج أولاً، ثم اكتب 'منشور' وسأكتب لك منشوراً تسويقياً."
    
    # ====== Noon ======
    if "noon" in user_input_lower:
        return "🛍️ متجر Noon من أفضل المتاجر العربية. فيه خصومات يومية تصل إلى 70%. أرسل لي رابط المنتج الذي تريده وسأكتب لك منشوراً تسويقياً له."
    
    # ====== AliExpress ======
    if "aliexpress" in user_input_lower or "علي اكسبرس" in user_input_lower:
        return "🌏 AliExpress يوفر منتجات من كل العالم بأسعار تنافسية. أرسل لي رابط المنتج وسأقوم بتحليله وكتابة منشور له."
    
    # ====== SHEIN ======
    if "shein" in user_input_lower or "شي ان" in user_input_lower:
        return "👗 متجر SHEIN متخصص في الأزياء والموضة. فيه كود خصم 20% للمستخدمين الجدد. أرسل رابط المنتج وسأكتب لك منشوراً جذاباً."
    
    # ====== الهواتف ======
    if "هاتف" in user_input_lower or "جوال" in user_input_lower or "موبايل" in user_input_lower:
        return """📱 **عروض الهواتف في اليمن:**

• **LT** - هواتف اقتصادية (LT P10: $80, LT X5: $120, LT Pro: $200)
• **Itel** - أداء ممتاز (Itel A25: $60, Itel P37: $90, Itel S18: $150)
• **VIVO** - كاميرات احترافية (VIVO Y16: $120, VIVO V25: $250, VIVO X90: $450)

📍 جميعها متوفرة في **المركز الدولي للهواتف الذكية** مع ضمان.
أي ماركة تهمك؟"""
    
    # ====== LT ======
    if "lt" in user_input_lower and len(user_input_lower) < 10:
        return "📱 هواتف LT متوفرة في المركز الدولي للهواتف الذكية. الأسعار: LT P10 ($80)، LT X5 ($120)، LT Pro Max ($200). مع ضمان 6 شهور."
    
    # ====== Itel ======
    if "itel" in user_input_lower:
        return "📱 هواتف Itel عملية واقتصادية. متوفرة في المركز الدولي: Itel A25 ($60)، Itel P37 ($90)، Itel S18 ($150)."
    
    # ====== VIVO ======
    if "vivo" in user_input_lower:
        return "📱 هواتف VIVO بتقنيات متطورة وكاميرات رائعة. متوفرة في المركز الدولي: VIVO Y16 ($120)، VIVO V25 ($250)، VIVO X90 ($450)."
    
    # ====== المركز الدولي ======
    if "المركز الدولي" in user_input_lower or "مركز الهواتف" in user_input_lower:
        return "🏢 المركز الدولي للهواتف الذكية هو المتجر الموثوق في اليمن. يوفر ضماناً على جميع المنتجات ومدة الضمان متفق عليها مع العميل. يقع في شارع التعاون، صنعاء."
    
    # ====== شكراً ======
    if "شكرا" in user_input_lower or "شكراً" in user_input_lower:
        return "العفو، هذا واجبي. أنا موجود لخدمتك في أي وقت. تفضل بأي سؤال آخر."
    
    # ====== مع السلامة ======
    if "مع السلامة" in user_input_lower or "باي" in user_input_lower or "وداعا" in user_input_lower:
        return "في أمان الله، تشرفت بخدمتك. عد في أي وقت."
    
    # ====== رد افتراضي ذكي ======
    return f"""أنا Saeed DaTaBoT، كيف أقدر أساعدك؟

📌 **أرسل لي رابط منتج** من Noon أو AliExpress أو SHEIN وسأكتب لك منشوراً تسويقياً فوراً.

أو اسأل عن:
• Noon - عروض noon
• AliExpress - عروض علي اكسبرس  
• SHEIN - عروض شي ان
• هاتف - عروض الهواتف
• LT / Itel / VIVO - هواتف معينة"""

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
st.set_page_config(page_title="Saeed DaTaBoT", page_icon="🤖", layout="wide")

# تشغيل الصوت الترحيبي
if "welcome_played" not in st.session_state:
    audio_html = play_welcome_audio()
    if audio_html:
        st.markdown(audio_html, unsafe_allow_html=True)
    st.session_state.welcome_played = True

# عنوان الصفحة
st.markdown("""
<div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px;">
    <h1 style="color: white;">🤖 Saeed DaTaBoT</h1>
    <p style="color: #e0e0e0;">صنع بواسطة سعيد المسوري | الذكاء الاصطناعي للتسويق والهواتف</p>
    <p style="color: #ffd700;">✨ أرسل رابط منتج وسأكتب لك منشوراً تسويقياً فوراً ✨</p>
</div>
""", unsafe_allow_html=True)

# تبويبات
tab1, tab2, tab3 = st.tabs(["🌍 التسويق بالعمولة", "📱 عرض الهواتف", "💬 تحدث مع Saeed DaTaBoT"])

# ========== TAB 1 ==========
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🛍️ تحليل المتاجر")
        st.info("🛒 **Noon** - خصومات تصل إلى 70%")
        st.info("🌏 **AliExpress** - شحن دولي مجاني")
        st.info("👗 **SHEIN** - كود خصم 20%")
        
        st.markdown("### 🔗 رابط المنتج")
        product_url = st.text_input("أدخل رابط المنتج", placeholder="https://www.noon.com/...")
        if product_url:
            st.session_state.last_url = product_url
            if st.button("📊 تحليل المنتج"):
                with st.spinner("جاري قراءة الرابط..."):
                    info = extract_product_from_url(product_url)
                    st.session_state.bot_response = f"📦 المنتج: {info['title']}\n💰 السعر: {info['price']}\n🏪 المتجر: {info['platform']}"
    
    with col2:
        st.markdown("### ✍️ توليد المنشورات")
        product_name = st.text_input("اسم المنتج", placeholder="هاتف Samsung")
        platform = st.selectbox("المنصة", ["Facebook", "Instagram", "Twitter", "TikTok"])
        target_audience = st.text_input("الجمهور المستهدف", placeholder="شباب 18-25")
        if st.button("🚀 توليد منشور تسويقي"):
            if product_name:
                with st.spinner("جاري التوليد..."):
                    post = generate_post(product_name, platform, target_audience or "العملاء")
                st.success(post)

# ========== TAB 2 ==========
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
        </div>
        """, unsafe_allow_html=True)
        if st.button("استفسر عن LT"):
            st.session_state.bot_response = "هواتف LT متوفرة في المركز الدولي بأسعار تبدأ من $80 مع ضمان."
    
    with col2:
        st.markdown("""
        <div style="border: 2px solid #764ba2; border-radius: 15px; padding: 15px; text-align: center;">
            <h2 style="color: #764ba2;">📱 Itel</h2>
            <p>أداء ممتاز</p>
            <p>💰 Itel A25: $60</p>
            <p>💰 Itel P37: $90</p>
            <p>💰 Itel S18: $150</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("استفسر عن Itel"):
            st.session_state.bot_response = "هواتف Itel عملية واقتصادية، متوفرة في المركز الدولي."
    
    with col3:
        st.markdown("""
        <div style="border: 2px solid #ff6b6b; border-radius: 15px; padding: 15px; text-align: center;">
            <h2 style="color: #ff6b6b;">📱 VIVO</h2>
            <p>كاميرات احترافية</p>
            <p>💰 VIVO Y16: $120</p>
            <p>💰 VIVO V25: $250</p>
            <p>💰 VIVO X90: $450</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("استفسر عن VIVO"):
            st.session_state.bot_response = "هواتف VIVO بتقنيات متطورة، متوفرة في المركز الدولي."

# ========== TAB 3: المحادثة ==========
with tab3:
    st.markdown("### 💬 تحدث مع Saeed DaTaBoT")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "السلام عليكم ورحمة الله وبركاته، أنا Saeed DaTaBoT. كيف أقدر أساعدك اليوم؟"})
    
    if "bot_response" in st.session_state and st.session_state.bot_response:
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.bot_response})
        st.session_state.bot_response = None
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    user_input = st.chat_input("✍️ اكتب سؤالك هنا...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.spinner("🤖 جاري التفكير..."):
            response = get_bot_response(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
        
        audio_html = text_to_speech(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
        
        st.rerun()

# ========== الشريط الجانبي ==========
with st.sidebar:
    st.markdown("### 🔒 Saeed MarketAds")
    st.markdown(f"""
    **المطور:** {OWNER_NAME} ({SMART_SAEED})
    
    - تسويق بالعمولة
    - عروض الهواتف
    - ضمان المنتجات
    """)
    
    if st.button("🎵 تشغيل الترحيب"):
        audio_html = play_welcome_audio()
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
    
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.clear()
        st.rerun()

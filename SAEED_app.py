import streamlit as st
import google.generativeai as genai
import gtts
from io import BytesIO
import base64

# ========== إعدادات البوت ==========
BOT_NAME = "Saeed DataBot"
OWNER_NAME = "سعيد المسوري"
SMART_SAEED = "سعيد الذكي"

# ========== إعداد Gemini ==========
GEMINI_API_KEY = "ضع_مفتاحك_هنا"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.5-flash')

# ========== إعدادات الصوت ==========
def text_to_speech(text):
    try:
        tts = gtts.gTTS(text, lang="ar")
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        audio_base64 = base64.b64encode(audio_bytes.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    except:
        return ""

# ========== ردود البوت الذكية ==========
def get_bot_response(user_input):
    user_input_lower = user_input.lower().strip()
    
    # ترحيب بالأسواق المختلفة
    if "سلام" in user_input_lower or "مرحباً" in user_input_lower:
        return "🎯 وعليكم السلام ورحمة الله! أنا Saeed DataBot، تحت أمرك. هل تريد عروض Noon، AliExpress، أو SHEIN؟"
    
    # من برمجك
    if "من برمجك" in user_input_lower:
        return f"🤖 أنا {BOT_NAME}، تم برمجتي بواسطة {OWNER_NAME} ({SMART_SAEED}) بمساعدة الذكاء الاصطناعي Gemini."
    
    # Noon
    if "noon" in user_input_lower:
        return "🛍️ **Noon** - أكبر سوق عربي!\n✅ خصومات تصل إلى 70%\n✅ توصيل سريع\n✅ منتجات أصلية\n\nما المنتج الذي تبحث عنه؟"
    
    # AliExpress
    if "aliexpress" in user_input_lower or "علي اكسبرس" in user_input_lower:
        return "🌏 **AliExpress** - عالم من المنتجات!\n✅ أسعار المصنع\n✅ شحن دولي\n✅ حماية المشتري\n\nأخبرني ماذا تريد أن أبحث لك؟"
    
    # SHEIN
    if "shein" in user_input_lower or "شي ان" in user_input_lower:
        return "👗 **SHEIN** - موضة وأزياء!\n✅ كود خصم 20%\n✅ توصيل سريع\n✅ أحدث الصيحات\n\nهل تريد مساعدة في اختيار منتج؟"
    
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
    return f"🎯 أنا {BOT_NAME}، كيف أخدمك؟\n\nاكتب:\n• Noon - لعروض noon\n• AliExpress - لعروض علي اكسبرس\n• SHEIN - لعروض شي ان\n• هاتف - لعروض الهواتف\n• LT / Itel / VIVO - لهواتف معينة"

# ========== توليد منشور ==========
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

# عنوان الصفحة
st.markdown("""
<div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px;">
    <h1 style="color: white;">🤖 Saeed DataBot</h1>
    <p style="color: #e0e0e0;">صنع بواسطة سعيد المسوري | الذكاء الاصطناعي للتسويق والهواتف</p>
</div>
""", unsafe_allow_html=True)

# إنشاء التبويبات (Tabs) مثل ما في مخططك
tab1, tab2, tab3 = st.tabs(["🌍 التسويق بالعمولة", "📱 عرض الهواتف", "💬 تحدث مع البوت"])

# ========== TAB 1: التسويق بالعمولة ==========
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🛍️ تحليل المتاجر")
        st.info("🛒 **Noon** - خصومات تصل إلى 70%")
        st.info("🌏 **AliExpress** - شحن دولي مجاني")
        st.info("👗 **SHEIN** - كود خصم 20%")
        
        # أزرار سريعة للمتاجر
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("🛍️ Noon", use_container_width=True):
                st.session_state.bot_response = "🛍️ Noon: خصومات تصل إلى 70% على آلاف المنتجات! ما الذي تبحث عنه؟"
        with col_btn2:
            if st.button("🌏 AliExpress", use_container_width=True):
                st.session_state.bot_response = "🌏 AliExpress: منتجات من كل العالم بأسعار المصنع! أخبرني ماذا تريد؟"
        with col_btn3:
            if st.button("👗 SHEIN", use_container_width=True):
                st.session_state.bot_response = "👗 SHEIN: كود خصم 20% على أول طلب! هل تريد مساعدة؟"
    
    with col2:
        st.markdown("### ✍️ توليد المنشورات")
        product_name = st.text_input("اسم المنتج", placeholder="مثال: هاتف Samsung")
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
    
    # عرض الهواتف في أعمدة
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
    
    # إدارة المخزون
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
        st.session_state.messages.append({"role": "assistant", "content": "🎯 مرحباً بك في Saeed DataBot! أنا مساعدك الذكي للتسويق والهواتف. كيف أخدمك اليوم؟\n\nاكتب: Noon, AliExpress, SHEIN, هاتف, LT, Itel, VIVO"})
    
    if "bot_response" in st.session_state and st.session_state.bot_response:
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.bot_response})
        st.session_state.bot_response = None
    
    # عرض المحادثة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # إدخال المستخدم
    user_input = st.chat_input("✍️ اكتب سؤالك هنا...")
    
    if user_input:
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
    
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.clear()
        st.rerun()

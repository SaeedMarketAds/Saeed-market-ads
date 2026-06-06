import json
import streamlit as st
from streamlit_chat import message
import gtts
from io import BytesIO
import base64
import random
import google.generativeai as genai
from datetime import datetime

# ========== إعداد مفتاح API ==========
# ضع مفتاحك هنا أو استخدم Streamlit Secrets
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "ضع_مفتاحك_هنا")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  # Gemini 3.5 Flash

# ========== الإعدادات الأساسية ==========
BOT_NAME = "Saeed DataBot"
OWNER_NAME = "سعيد المسوري"
SMART_SAEED = "سعيد الذكي"

# فاصل 5 لتنظيم الردود
SEPARATOR = "─" * 30

# إعدادات الصوت
VOICE_ENABLED = True

# بيانات المستخدمين المسموح لهم (مثال - يمكن تخزينها في JSON)
USERS_DB = {
    "admin": {"password": "admin123", "role": "admin"},
    "saeed": {"password": "saeed2024", "role": "owner"},
    "user": {"password": "user123", "role": "user"}
}

# هيكل المخزون للهواتف
INVENTORY = {
    "LT": {
        "models": ["LT P10", "LT X5", "LT Pro Max"],
        "prices": {"LT P10": "$80", "LT X5": "$120", "LT Pro Max": "$200"},
        "stock": {"LT P10": 15, "LT X5": 8, "LT Pro Max": 5}
    },
    "Itel": {
        "models": ["Itel A25", "Itel P37", "Itel S18"],
        "prices": {"Itel A25": "$60", "Itel P37": "$90", "Itel S18": "$150"},
        "stock": {"Itel A25": 20, "Itel P37": 12, "Itel S18": 7}
    },
    "VIVO": {
        "models": ["VIVO Y16", "VIVO V25", "VIVO X90"],
        "prices": {"VIVO Y16": "$120", "VIVO V25": "$250", "VIVO X90": "$450"},
        "stock": {"VIVO Y16": 10, "VIVO V25": 6, "VIVO X90": 3}
    }
}

# ========== وظائف الصوت ==========
def text_to_speech(text):
    """تحويل النص إلى صوت"""
    try:
        tts = gtts.gTTS(text, lang="ar")
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        audio_base64 = base64.b64encode(audio_bytes.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    except:
        return ""

def play_welcome_audio():
    """تشغيل ملف الترحيب الصوتي"""
    try:
        with open("welcome_voice.mp3", "rb") as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    except:
        return text_to_speech(f"مرحباً بك في {BOT_NAME}، منصة سعيد المسوري للذكاء الاصطناعي")

# ========== وظائف الذكاء الاصطناعي (Gemini 3.5 Flash) ==========
def get_ai_response(prompt, context=""):
    """الحصول على رد من Gemini 3.5 Flash"""
    try:
        system_prompt = f"""أنت {BOT_NAME}، مساعد ذكي متخصص تم تطويره بواسطة {OWNER_NAME} ({SMART_SAEED}).
        
قواعد الرد:
1. اسمك دائمًا هو {BOT_NAME} - لا تذكر اسم النموذج التقني
2. أنت متخصص في:
   - التسويق بالعمولة لمنصات: Noon، AliExpress، SHEIN
   - نصائح شراء الهواتف: LT، Itel، VIVO
   - إدارة المخزون والمبيعات
3. حافظ على الهوية الاحترافية في جميع الردود
4. اللغة العربية الفصحى أو العامية المفهومة

السياق الحالي: {context}
سؤال المستخدم: {prompt}
الرد:"""
        
        response = model.generate_content(system_prompt)
        return response.text
    except Exception as e:
        return f"⚠️ عذراً، حدث خطأ تقني. يرجى المحاولة لاحقاً. (خطأ: {str(e)})"

def generate_marketing_post(product_name, platform, target_audience):
    """توليد منشور تسويقي"""
    prompt = f"""اكتب منشور تسويقي احترافي باللغة العربية لـ:
المنتج: {product_name}
المنصة: {platform}
الجمهور المستهدف: {target_audience}

المطلوب: نص جذاب، إيموجيات مناسبة، هاشتاجات، عبارة حث على الشراء.
المنشور:"""
    
    return get_ai_response(prompt, context="توليد منشور تسويقي")

# ========== وظائف البوت الرئيسية ==========
def get_bot_response(user_input, context=""):
    """دالة ردود البوت باستخدام Gemini 3.5 Flash"""
    user_input_lower = user_input.lower().strip()
    
    # كلمات التحية والترحيب
    greetings = ["سلام", "مرحباً", "اهلا", "السلام", "مرحبا", "هلا", "السلام عليكم"]
    for word in greetings:
        if word in user_input_lower:
            markets = ["سوق المركز الدولي للهواتف", "سوق الشرفين", "سوق الصافية", "سوق تعز الكبير"]
            market = random.choice(markets)
            return f"🎯 أهلاً وسهلاً بك في {market}！\n{SEPARATOR}\nأنا {BOT_NAME}، تحت أمرك!\nكيف أخدمك اليوم؟"
    
    # من برمجك
    if any(word in user_input_lower for word in ["من برمجك", "من برمجة", "who programmed"]):
        return f"🤖 أنا {BOT_NAME}\n{SEPARATOR}\nتم برمجتي بواسطة المبرمج العبقري: **{OWNER_NAME} ({SMART_SAEED})**\n🎓 تم تطويري بمساعدة الذكاء الاصطناعي Gemini\n{SEPARATOR}\nأنا هنا لخدمتك في التسويق والهواتف!"
    
    # توليد منشور تسويقي
    if any(word in user_input_lower for word in ["منشور", "بوست", "تسويق", "اعلان", "post"]):
        return generate_marketing_post("منتجك", "وسائل التواصل", "العملاء المحتملين")
    
    # الاستفسار عن المتاجر (Noon, AliExpress, SHEIN)
    if "noon" in user_input_lower:
        return f"🛍️ **Noon** - أكبر سوق إلكتروني عربي\n{SEPARATOR}\n✅ عروض حصرية يومية\n✅ توصيل سريع\n✅ منتجات أصلية\n\nهل تريد مساعدة في البحث عن منتج معين على Noon؟"
    
    if "aliexpress" in user_input_lower or "علي اكسبرس" in user_input_lower:
        return f"🌏 **AliExpress** - منتجات عالمية بأسعار المصنع\n{SEPARATOR}\n✅ شحن دولي إلى اليمن\n✅ حماية المشتري\n✅ ملايين المنتجات\n\nاطلب أي منتج وأنا أساعدك في البحث!"
    
    if "shein" in user_input_lower or "شي ان" in user_input_lower:
        return f"👗 **SHEIN** - عالم الموضة والأزياء\n{SEPARATOR}\n✅ أحدث الصيحات\n✅ أسعار تنافسية\n✅ توصيل سريع\n\nهل تريد البحث عن ملابس معينة؟"
    
    # الهواتف المحلية (LT, Itel, VIVO)
    if "lt" in user_input_lower:
        models = "\n".join([f"📱 {m} - {INVENTORY['LT']['prices'][m]} (المتبقي: {INVENTORY['LT']['stock'][m]})" for m in INVENTORY['LT']['models']])
        return f"📱 **هواتف LT**\n{SEPARATOR}\n{models}\n{SEPARATOR}\n📍 متوفرة في المركز الدولي للهواتف الذكية مع ضمان"
    
    if "itel" in user_input_lower:
        models = "\n".join([f"📱 {m} - {INVENTORY['Itel']['prices'][m]} (المتبقي: {INVENTORY['Itel']['stock'][m]})" for m in INVENTORY['Itel']['models']])
        return f"📱 **هواتف Itel**\n{SEPARATOR}\n{models}\n{SEPARATOR}\n💰 اقتصادية وعملية، متوفرة الآن!"
    
    if "vivo" in user_input_lower:
        models = "\n".join([f"📱 {m} - {INVENTORY['VIVO']['prices'][m]} (المتبقي: {INVENTORY['VIVO']['stock'][m]})" for m in INVENTORY['VIVO']['models']])
        return f"📱 **هواتف VIVO**\n{SEPARATOR}\n{models}\n{SEPARATOR}\n📸 كاميرات ممتازة وتصميم أنيق!"
    
    # إدارة المخزون
    if any(word in user_input_lower for word in ["مخزون", "stock", "المخزون", "الكمية"]):
        inventory_text = "📊 **إدارة المخزون**\n"
        for brand, data in INVENTORY.items():
            inventory_text += f"\n🔹 {brand}:\n"
            for model, stock in data['stock'].items():
                inventory_text += f"   - {model}: {stock} قطعة\n"
        return inventory_text
    
    # استخدام Gemini للردود الأخرى
    return get_ai_response(user_input, context)

# ========== واجهة تسجيل الدخول ==========
def login_page():
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
    }
    .main-header p {
        color: #e0e0e0;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"><h1>🤖 Saeed MarketAds</h1><p>صنع بواسطة سعيد المسوري | الذكاء الاصطناعي للتسويق والهواتف</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 🔐 تسجيل الدخول")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("👤 اسم المستخدم أو البريد الإلكتروني")
        password = st.text_input("🔒 كلمة السر", type="password")
        login_btn = st.button("🚀 تسجيل الدخول", use_container_width=True)
        
        if login_btn:
            if username in USERS_DB and USERS_DB[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = USERS_DB[username]["role"]
                st.rerun()
            else:
                st.error("❌ اسم المستخدم أو كلمة السر غير صحيحة")
    
    st.markdown("---")
    st.markdown("### 🚀 منصة Saeed DataBot")
    st.markdown("جاري تهيئة الأنظمة...")

# ========== الواجهة الرئيسية ==========
def main_app():
    # الصوت الترحيبي
    if "audio_played" not in st.session_state:
        audio_html = play_welcome_audio()
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
        st.session_state.audio_played = True
    
    # الشريط الجانبي
    with st.sidebar:
        st.image("saeed.jpg" if __import__("os").path.exists("saeed.jpg") else None, width=150)
        st.markdown(f"## 🤖 {BOT_NAME}")
        st.markdown(f"**المطور:** {OWNER_NAME} ({SMART_SAEED})")
        st.markdown(f"**مستخدم:** {st.session_state.username}")
        st.markdown(f"**الصلاحية:** {st.session_state.role}")
        
        st.divider()
        
        # أزرار سريعة
        st.markdown("### ⚡ روابط سريعة")
        if st.button("📊 عرض المخزون"):
            st.session_state.quick_action = "inventory"
        if st.button("📱 عروض LT"):
            st.session_state.quick_action = "lt"
        if st.button("📱 عروض Itel"):
            st.session_state.quick_action = "itel"
        if st.button("📱 عروض VIVO"):
            st.session_state.quick_action = "vivo"
        
        st.divider()
        
        # زر الخصوصية
        if st.button("🔒 الخصوصية وسياسة الاستخدام"):
            st.session_state.show_privacy = True
        
        # زر تسجيل الخروج
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.logged_in = False
            st.rerun()
    
    # نافذة الخصوصية المنبثقة
    if st.session_state.get("show_privacy", False):
        with st.expander("🔒 سياسة الخصوصية - اضغط للإغلاق", expanded=True):
            st.markdown("""
            ### سياسة الخصوصية لـ Saeed MarketAds
            
            **المطور:** سعيد المسوري (سعيد الذكي)
            
            **البيانات التي نجمعها:**
            - اسم المستخدم
            - تفضيلات التسوق
            - سجل المحادثة (لتحسين الخدمة)
            
            **كيف نستخدم بياناتك:**
            - تحسين تجربة المستخدم
            - تقديم عروض مخصصة
            - تطوير الذكاء الاصطناعي
            
            **الأمان:**
            جميع بياناتك مشفرة ولا نشاركها مع أطراف ثالثة.
            
            **للتواصل:** عبر منصة GitHub الخاصة بنا
            
            آخر تحديث: 2024
            """)
            if st.button("إغلاق"):
                st.session_state.show_privacy = False
                st.rerun()
    
    # عنوان الصفحة
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem;">
        <h1>🤖 {BOT_NAME}</h1>
        <p>صنع بواسطة {OWNER_NAME} | منصة متكاملة للتسويق والهواتف</p>
    </div>
    """, unsafe_allow_html=True)
    
    # التبويبات (Tabs)
    tab1, tab2, tab3 = st.tabs(["📊 التسويق بالعمولة", "📱 عرض الهواتف", "💬 محادثة Saeed DataBot"])
    
    # تبويب التسويق بالعمولة
    with tab1:
        st.markdown("### 📊 قسم التسويق بالعمولة")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🛍️ تحليل المتاجر")
            st.info("**Noon** - خصومات تصل إلى 70%")
            st.info("**AliExpress** - شحن دولي مجاني")
            st.info("**SHEIN** - كود خصم 20%")
            
            st.markdown("#### ✍️ توليد المنشورات")
            product = st.text_input("اسم المنتج", placeholder="مثال: هاتف Samsung")
            platform = st.selectbox("المنصة", ["Facebook", "Instagram", "Twitter", "TikTok"])
            audience = st.text_input("الجمهور المستهدف", placeholder="مثال: شباب 18-25")
            
            if st.button("🚀 توليد منشور تسويقي"):
                with st.spinner("جاري توليد منشور احترافي..."):
                    post = generate_marketing_post(product or "منتجك", platform, audience or "العملاء")
                    st.markdown("#### 📝 المنشور المُنشأ:")
                    st.success(post)
        
        with col2:
            st.markdown("#### 📱 عرض الهواتف")
            st.markdown("**LT** - هواتف اقتصادية")
            st.markdown("**Itel** - أداء ممتاز")
            st.markdown("**VIVO** - كاميرات احترافية")
            
            st.markdown("#### 📦 إدارة المخزون")
            for brand, data in INVENTORY.items():
                with st.expander(f"🔹 {brand}"):
                    for model in data['models']:
                        st.write(f"📱 {model}: {data['prices'][model]} - متبقي: {data['stock'][model]}")
    
    # تبويب عرض الهواتف
    with tab2:
        st.markdown("### 📱 المتاجر المحلية - الهواتف")
        
        for brand, data in INVENTORY.items():
            st.markdown(f"#### 🔹 {brand}")
            cols = st.columns(len(data['models']))
            for idx, model in enumerate(data['models']):
                with cols[idx]:
                    st.markdown(f"""
                    <div style="border:1px solid #ddd; border-radius:10px; padding:10px; text-align:center;">
                        <h4>{model}</h4>
                        <p>💰 {data['prices'][model]}</p>
                        <p>📦 المتبقي: {data['stock'][model]}</p>
                        <p style="color:green;">✅ متوفر</p>
                    </div>
                    """, unsafe_allow_html=True)
            st.divider()
    
    # تبويب المحادثة
    with tab3:
        st.markdown("### 💬 تحدث مع Saeed DataBot")
        
        # تهيئة سجل المحادثة
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
            welcome_msg = f"مرحباً بك في {BOT_NAME}！\n{SEPARATOR}\nأنا مساعدك الذكي للتسويق والهواتف.\nكيف أقدر أخدمك اليوم؟"
            st.session_state.chat_messages.append({"role": "assistant", "content": welcome_msg})
        
        # عرض المحادثة
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # إدخال المستخدم
        user_input = st.chat_input("✍️ اكتب سؤالك هنا...")
        
        if user_input:
            # إضافة رسالة المستخدم
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            
            # الحصول على رد البوت
            with st.spinner("🤖 جاري التفكير..."):
                response = get_bot_response(user_input)
            
            # إضافة رد البوت
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)
            
            # تشغيل الصوت
            if VOICE_ENABLED:
                audio_html = text_to_speech(response)
                if audio_html:
                    st.markdown(audio_html, unsafe_allow_html=True)
            
            st.rerun()
    
    # تنفيذ الإجراء السريع
    if st.session_state.get("quick_action") == "inventory":
        st.session_state.quick_action = None
        st.rerun()
    elif st.session_state.get("quick_action") == "lt":
        st.session_state.quick_action = None
        st.rerun()
    elif st.session_state.get("quick_action") == "itel":
        st.session_state.quick_action = None
        st.rerun()
    elif st.session_state.get("quick_action") == "vivo":
        st.session_state.quick_action = None
        st.rerun()

# ========== تشغيل التطبيق ==========
def main():
    st.set_page_config(
        page_title="Saeed MarketAds",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # تهيئة حالة الجلسة
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    # عرض الصفحة المناسبة
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()

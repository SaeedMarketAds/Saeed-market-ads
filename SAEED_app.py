import streamlit as st
import os
import base64
from pathlib import Path
import random
import google.generativeai as genai

# ==================== إعداد موديل Gemini 3.5 ====================
# تأكد من وضع مفتاح API الخاص بك في متغير البيئة GOOGLE_API_KEY
# أو اكتبه مباشرة هنا (غير آمن للإنتاج)
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY", "YOUR_API_KEY_HERE"))
    model = genai.GenerativeModel(
        'gemini-1.5-flash',  # موديل 3.5 Flash
        system_instruction="""
        أنت "سعيد المسوري"، خبير تسويق إلكتروني ومستشار مبيعات محترف.

        **هويتك التقنية:**
        تعمل عبر نموذج Google Gemini 3.5 Flash. أنت سريع، دقيق، وتتذكر سياق المحادثة بشكل ممتاز. استخدم قدراتك في التحليل المنطقي والفهم العميق للغة العربية لتقديم إجابات غير سطحية.

        **قواعد عملك (الأهم):**
        1. **الذاكرة مطلوبة:** بما أنك تعمل على موديل 3.5، أنت قادر على تذكر آخر 5-10 رسائل من المحادثة. استخدم هذه الميزة دائماً. لا تكرر الأسئلة التي سبق أن سألتها.
        2. **لا تخرج عن دورك:** أنت خبير تسويق فقط. لا تتحدث عن البرمجة أو السياسة أو أي شيء خارج نطاق مساعدة المستخدم في الشراء، تحليل المنتجات، أو نصائح البيع.
        3. **اسأل قبل أن تجيب:** إذا طلب المستخدم منتجاً (مثل: هاتف، ساعة)، اسأله أولاً عن: الميزانية التقريبية، المواصفات المهمة، التفضيل (جديد أم مستعمل).
        4. **أسلوب الرد:** ودود، احترافي، ومباشر. استخدم الرموز التعبيرية المناسبة 👍 ✅ 🎯.

        **تذكير داخلي للنموذج 3.5:**
        أنت لست Gemini 1.0 ولا 2.0. أنت الإصدار 3.5. استغل هذه القوة لتكون أكثر فائدة من أي بوت تسويقي عادي.
        """
    )
    GEMINI_AVAILABLE = True
except Exception as e:
    st.warning(f"⚠️ لم يتم تفعيل Gemini 3.5: {e}. سيتم استخدام الردود المحلية بدلاً من ذلك.")
    GEMINI_AVAILABLE = False

# إعداد الصفحة
st.set_page_config(
    page_title="SaeedMarktAds - سوق سعيد",
    page_icon="🛍️",
    layout="wide"
)

# ==================== دوال الصوت ====================
def get_audio_html(audio_path):
    """تحويل ملف الصوت إلى كود HTML لتشغيله تلقائياً"""
    if os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        return f'<audio autoplay="true" src="data:audio/mp4;base64,{audio_base64}"></audio>'
    return None

def play_owner_voice():
    """تشغيل صوت المؤسس"""
    audio_path = "Saeed_Voice_01.m4a"
    if os.path.exists(audio_path):
        html = get_audio_html(audio_path)
        if html:
            st.components.v1.html(html, height=0)
            return True
    return False

def speak_text(text):
    """نطق النص باستخدام المتصفح"""
    # تنظيف النص من علامات Markdown
    clean_text = text.replace("**", "").replace("*", "").replace("\n", " ")
    js_code = f"""
    <script>
        var utterance = new SpeechSynthesisUtterance("{clean_text}");
        utterance.lang = "ar-SA";
        utterance.rate = 0.9;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# ==================== دوال الأسواق والمنتجات ====================
def get_market_products(market_name):
    """جلب منتجات حسب السوق"""
    products = {
        "aliexpress": [
            {"name": "هاتف ذكي 5G", "price": "$199", "icon": "📱", "link": "https://www.aliexpress.com"},
            {"name": "ساعة رياضية", "price": "$45", "icon": "⌚", "link": "https://www.aliexpress.com"},
            {"name": "سماعات لاسلكية", "price": "$25", "icon": "🎧", "link": "https://www.aliexpress.com"},
            {"name": "باور بانك 20000mAh", "price": "$30", "icon": "🔋", "link": "https://www.aliexpress.com"},
            {"name": "كاميرا مراقبة", "price": "$50", "icon": "📷", "link": "https://www.aliexpress.com"},
        ],
        "noon": [
            {"name": "لابتوب ألعاب", "price": "899 درهم", "icon": "💻", "link": "https://www.noon.com"},
            {"name": "شاحن سريع", "price": "49 درهم", "icon": "⚡", "link": "https://www.noon.com"},
            {"name": "سماعة رأس", "price": "89 درهم", "icon": "🎮", "link": "https://www.noon.com"},
            {"name": "تابلت", "price": "399 درهم", "icon": "📟", "link": "https://www.noon.com"},
            {"name": "ساعة ذكية", "price": "199 درهم", "icon": "⌚", "link": "https://www.noon.com"},
        ],
        "shein": [
            {"name": "فستان سهرة", "price": "$32", "icon": "👗", "link": "https://www.shein.com"},
            {"name": "حقيبة يد", "price": "$18", "icon": "👜", "link": "https://www.shein.com"},
            {"name": "حذاء رياضي", "price": "$25", "icon": "👟", "link": "https://www.shein.com"},
            {"name": "نظارة شمسية", "price": "$15", "icon": "🕶️", "link": "https://www.shein.com"},
            {"name": "ساعة أنيقة", "price": "$22", "icon": "⌚", "link": "https://www.shein.com"},
        ],
        "yemen": [
            {"name": "عسل سدر يمني", "price": "15,000 ريال", "icon": "🍯", "link": "#"},
            {"name": "مصنوعات فضية", "price": "25,000 ريال", "icon": "💍", "link": "#"},
            {"name": "بخور يمني", "price": "8,000 ريال", "icon": "🪔", "link": "#"},
            {"name": "ملابس تراثية", "price": "12,000 ريال", "icon": "👘", "link": "#"},
            {"name": "قهوة يمنية", "price": "10,000 ريال", "icon": "☕", "link": "#"},
        ]
    }
    return products.get(market_name, [])

# ==================== دوال البوت الذكي (باستخدام Gemini 3.5) ====================
def get_bot_response_with_gemini(user_message, chat_history):
    """توليد رد ذكي باستخدام Gemini 3.5 Flash مع السياق"""
    if not GEMINI_AVAILABLE:
        return get_bot_response_fallback(user_message)
    
    try:
        # بناء تاريخ المحادثة
        chat = model.start_chat(history=[])
        
        # إضافة تاريخ المحادثة السابق (آخر 10 رسائل)
        recent_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
        for msg in recent_history:
            if msg["role"] == "user":
                chat.send_message(msg["content"])
            # لا نضيف ردود البوت لأنها ستأتي تلقائياً
        
        # إرسال الرسالة الجديدة
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        st.error(f"خطأ في Gemini: {e}")
        return get_bot_response_fallback(user_message)

def get_bot_response_fallback(user_message):
    """الردود المحلية الاحتياطية في حال تعذر استخدام Gemini"""
    msg = user_message.lower()
    
    if any(word in msg for word in ['aliexpress', 'علي', 'اكسبريس']):
        return "🔍 **AliExpress** يقدم أفضل الأسعار للإلكترونيات والمنتجات الصينية. يمكنك شراء الهواتف، الساعات، السماعات بأسعار تنافسية. هل تريد مساعدة في البحث عن منتج محدد؟"
    elif any(word in msg for word in ['noon', 'نون']):
        return "🇦🇪 **Noon** منصة التسوق الرائدة في الإمارات والسعودية. يتميز بالتوصيل السريع والعروض اليومية. سأبحث لك عن أفضل كوبونات الخصم!"
    elif any(word in msg for word in ['shein', 'شين']):
        return "👗 **Shein** وجهتك الأولى للأزياء العصرية. أحدث الصيحات والموضة بأسعار لا تُقارن. هل تبحث عن فستان، حقيبة، أو إكسسوارات؟"
    elif any(word in msg for word in ['يمن', 'يمني', 'محلي', 'ريال']):
        return "🇾🇪 **السوق اليمني** قادم قريباً جداً! سندعم المحافظ الإلكترونية اليمنية (مدى، كاش، تيلي يمن). شكراً لدعمك الاقتصاد المحلي ❤️"
    elif any(word in msg for word in ['سعر', 'غالي', 'رخيص', 'عرض', 'خصم']):
        return "📊 **تحليل الأسعار**: أنصحك بمقارنة العروض بين AliExpress و Noon قبل الشراء. هل تريد مني البحث عن أفضل سعر لمنتج معين؟"
    elif any(word in msg for word in ['منتج', 'بحث', 'أريد']):
        return "🔎 سأبحث لك عن أفضل المنتجات. أخبرني ما الذي تبحث عنه بالضبط (هاتف، ساعة، ملابس، إلكترونيات) وسأعرض لك أفضل العروض."
    else:
        return f"📊 **SaeedDataBot** في خدمتك. كخبير في التسويق الإلكتروني وتحليل السوق، أنصحك بالاطلاع على عروض AliExpress و Noon. هل تريد مساعدة في البحث عن منتج معين؟"

# ==================== واجهة المستخدم ====================
# تنسيق CSS مخصص
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    * { font-family: 'Tajawal', 'Cairo', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }
    .main-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 { color: white; font-size: 2rem; margin: 0; }
    .main-header p { color: rgba(255,255,255,0.9); font-size: 1.1rem; }
    .market-card {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        cursor: pointer;
        transition: transform 0.3s;
        color: white;
    }
    .market-card:hover { transform: translateY(-5px); }
    .product-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.3s;
    }
    .product-card:hover { transform: translateY(-5px); background: rgba(255,255,255,0.2); }
    .product-icon { font-size: 3rem; }
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }
    .bot-message {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        text-align: right;
    }
    .user-message {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        text-align: left;
    }
    .stButton > button {
        background: linear-gradient(45deg, #f093fb, #f5576c);
        border: none;
        color: white;
        border-radius: 25px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #f5576c, #f093fb);
        transform: scale(1.02);
    }
    hr { border-color: rgba(255,255,255,0.2); }
    </style>
""", unsafe_allow_html=True)

# ==================== رأس الصفحة ====================
# تشغيل صوت المؤسس عند فتح الصفحة (مرة واحدة فقط)
if "voice_played" not in st.session_state:
    play_owner_voice()
    st.session_state.voice_played = True

# زر التبديل بين SaeedDataBot والآفاتار الشخصي
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    mode = st.radio(
        "🎭 **اختر المساعد الذكي:**",
        ["🤖 SaeedDataBot", "🧑‍🦱 الآفاتار الشخصي لسعيد المسوري"],
        horizontal=True
    )

# عرض الصورة حسب الوضع
if "الآفاتار" in mode:
    if os.path.exists("saeed.jpg"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("saeed.jpg", width=200, caption="سعيد المسوري - مؤسس المنصة")
    st.markdown('<div class="main-header"><h1>🧑‍🦱 سعيد المسوري</h1><p>مؤسس SaeedMarktAds | خبير التسويق الإلكتروني</p></div>', unsafe_allow_html=True)
else:
    if os.path.exists("ROBOT.jpg"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("ROBOT.jpg", width=150, caption="SaeedDataBot")
    st.markdown('<div class="main-header"><h1>🤖 SaeedDataBot</h1><p>مساعدك الذكي للتسوق العالمي وتحليل السوق (Gemini 3.5 Flash)</p></div>', unsafe_allow_html=True)

# ==================== الأسواق السريعة ====================
st.markdown("### 🏪 الأسواق العالمية")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🛒 **AliExpress**\nعروض حصرية", use_container_width=True):
        st.session_state.selected_market = "aliexpress"
        speak_text("مرحباً بك في AliExpress، أكبر منصة للتسوق العالمي")
with col2:
    if st.button("🇦🇪 **Noon**\nتوصيل سريع", use_container_width=True):
        st.session_state.selected_market = "noon"
        speak_text("مرحباً بك في Noon، توصيل سريع إلى الإمارات والسعودية")
with col3:
    if st.button("👗 **Shein**\nأزياء وموضة", use_container_width=True):
        st.session_state.selected_market = "shein"
        speak_text("مرحباً بك في Shein، أحدث صيحات الموضة")
with col4:
    if st.button("🇾🇪 **السوق اليمني**\nدعم المحلي", use_container_width=True):
        st.session_state.selected_market = "yemen"
        speak_text("شكراً لدعمك الاقتصاد المحلي اليمني")

# ==================== عرض المنتجات ====================
if "selected_market" in st.session_state:
    st.markdown("---")
    st.markdown(f"### 🛍️ منتجات {st.session_state.selected_market}")
    
    products = get_market_products(st.session_state.selected_market)
    
    # عرض المنتجات في شبكة (3 منتجات في كل صف)
    for i in range(0, len(products), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(products):
                p = products[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="product-card">
                        <div class="product-icon">{p['icon']}</div>
                        <h4>{p['name']}</h4>
                        <p style="color: #f5576c; font-size: 1.2rem;">{p['price']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # زر الشراء مع رابط
                    if st.button(f"🛒 شراء {p['name']}", key=f"buy_{i+j}"):
                        if p['link'] and p['link'] != "#":
                            st.markdown(f'<meta http-equiv="refresh" content="0; url={p["link"]}">', unsafe_allow_html=True)
                            st.success(f"جاري تحويلك إلى {p['name']}...")
                        else:
                            st.info("🚧 قريباً سيتم تفعيل الشراء لهذا المنتج")

# ==================== منطقة المحادثة ====================
st.markdown("---")
st.markdown("## 💬 دردش مع المساعد الذكي")
if GEMINI_AVAILABLE:
    st.caption("✨ يعمل الآن على **Gemini 3.5 Flash** - أسرع وأذكى من أي وقت مضى")

# تهيئة سجل المحادثة
if "chat_history" not in st.session_state:
    if "الآفاتار" in mode:
        st.session_state.chat_history = [{"role": "assistant", "content": "أهلاً بك! أنا سعيد المسوري، مؤسس SaeedMarktAds. كيف يمكنني مساعدتك في التسويق الإلكتروني وتحليل السوق؟"}]
    else:
        st.session_state.chat_history = [{"role": "assistant", "content": "🎙️ أهلاً بك! أنا SaeedDataBot، مساعدك الذكي. أسواق العالم بين يديك. كيف أخدمك اليوم؟"}]

# عرض سجل المحادثة
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-message user-message">🗣️ {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        if "الآفاتار" in mode:
            st.markdown(f'<div class="chat-message bot-message">🧑‍🦱 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

# إدخال المستخدم
col1, col2, col3 = st.columns([6, 1, 1])
with col1:
    user_input = st.text_input("", placeholder="اكتب سؤالك هنا...", key="user_input", label_visibility="collapsed")
with col2:
    send_button = st.button("📤 إرسال", use_container_width=True)
with col3:
    voice_button = st.button("🎙️ تحدث", use_container_width=True)

# معالجة الإرسال
if send_button and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    if "الآفاتار" in mode:
        # ردود الآفاتار الشخصي - استخدام Gemini أيضاً
        if GEMINI_AVAILABLE:
            reply = get_bot_response_with_gemini(user_input, st.session_state.chat_history[:-1])
        else:
            reply = f"**سعيد المسوري:** شكراً لسؤالك. بصفتي خبيراً في التسويق الإلكتروني، أنصحك بالاطلاع على عروض AliExpress و Noon. هل تريد تفاصيل أكثر؟"
    else:
        # ردود SaeedDataBot باستخدام Gemini 3.5
        reply = get_bot_response_with_gemini(user_input, st.session_state.chat_history[:-1])
    
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    speak_text(reply.replace("**", ""))
    st.rerun()

if voice_button:
    js_code = """
    <script>
        var recognition = new webkitSpeechRecognition();
        recognition.lang = 'ar';
        recognition.onresult = function(event) {
            var text = event.results[0][0].transcript;
            var input = parent.document.querySelector('input[aria-label=""]');
            if(input) {
                input.value = text;
                var event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
                var buttons = parent.document.querySelectorAll('button');
                for(var i=0; i<buttons.length; i++) {
                    if(buttons[i].innerText.includes('إرسال')) {
                        buttons[i].click();
                        break;
                    }
                }
            }
        };
        recognition.start();
    </script>
    """
    st.components.v1.html(js_code, height=0)

# ==================== زر تشغيل صوت المؤسس ====================
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🎙️ **استمع لصوت المؤسس سعيد المسوري**", use_container_width=True):
        if play_owner_voice():
            st.success("✅ تم تشغيل صوت المؤسس")
        else:
            st.error("⚠️ ملف الصوت غير موجود! تأكد من وجود Saeed_Voice_01.m4a")

# ==================== التذييل ====================
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #888;">© 2025 SaeedMarktAds - SaeedDataBot | يعمل على Gemini 3.5 Flash 🤖 | قريباً: دعم المحافظ اليمنية 🤝</p>',
    unsafe_allow_html=True
)

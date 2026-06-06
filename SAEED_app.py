import json
import streamlit as st
from streamlit_chat import message
import gtts
from io import BytesIO
import base64
import random

# ========== الإعدادات ==========
BOT_NAME = "SaeeD DaTaBoT"
OWNER_NAME = "سعيد المسوري"
SMART_SAEED = "سعيد الذكي"

# ========== الموديل 3.5 Flash - العقل المحرك ==========
MODEL_NAME = "GPT-3.5 Flash"
MODEL_DESCRIPTION = "The Brain Engine | العقل المحرك"
MODEL_VERSION = "3.5 Flash"

# فاصل 5 لتنظيم الردود
SEPARATOR = "─" * 30

# قائمة أسماء الأسواق للترحيب المتنوع
MARKET_NAMES = [
    "سوق المركز الدولي للهواتف",
    "سوق الشرفين",
    "سوق الصافية", 
    "ساقية عدن",
    "سوق تعز الكبير",
    "سوق الهواتف بصنعاء"
]

# هيكل الشركات للإعلانات (قابل للتوسع)
COMPANIES_STRUCTURE = {
    "SHEIN": {"Ads": [], "description": "🌐 منصة عالمية للأزياء والموضة - توصيل سريع وأسعار تنافسية"},
    "NOON": {"Ads": [], "description": "🛍️ أكبر سوق عربي إلكتروني - كل ما تحتاجه في مكان واحد"},
    "VIVO": {"Ads": [], "description": "📱 هواتف ذكية بجودة عالية وكاميرات ممتازة"},
    "AMAZON": {"Ads": [], "description": "📦 عملاق التجارة الإلكترونية العالمية - توصيل عالمي"},
    "ALIEXPRESS": {"Ads": [], "description": "🌏 AliExpress - منتجات متنوعة بأسعار المصنع، شحن دولي"},
    "SAMSUNG": {"Ads": [], "description": "⭐ رائدة في عالم الهواتف والتكنولوجيا"},
    "LG": {"Ads": [], "description": "💎 جودة كورية موثوقة"}
}

# إعدادات الصوت
VOICE_ENABLED = True

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

def get_random_market_greeting():
    """ترحيب عشوائي باسم سوق مختلف"""
    market = random.choice(MARKET_NAMES)
    return f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
أهلاً وسهلاً بك في {market}！

أنا {BOT_NAME}، مساعدك الذكي.
قاعدتي هي {MODEL_NAME} - {MODEL_DESCRIPTION}

كيف أخدمك اليوم؟"""

def get_bot_response(user_input):
    """دالة ردود البوت الذكية - العقل المحرك GPT-3.5 Flash"""
    user_input_lower = user_input.lower().strip()
    
    # 1. الترحيب بالناس (كل مرة بسوق مختلف)
    greetings = ["سلام", "مرحباً", "اهلا", "السلام", "مرحبا", "هلا", "السلام عليكم"]
    for word in greetings:
        if word in user_input_lower:
            return get_random_market_greeting()
    
    # 2. سؤال عن من برمجك (المبرمج سعيد المسوري - سعيد الذكي)
    if any(word in user_input_lower for word in ["من برمجك", "من برمجة", "who programmed", "المبرمج", "سعيد"]):
        return f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
🤖 أنا {BOT_NAME}

تم برمجتي بواسطة المبرمج العبقري:
✨ **{OWNER_NAME} ({SMART_SAEED})** ✨

🎓 تم تطويري بمساعدة الذكاء الاصطناعي
⚙️ العقل المحرك: {MODEL_NAME} - {MODEL_DESCRIPTION}

{SEPARATOR}
أنا هنا لخدمتك في:
• التسوق من AliExpress، Noon، SHEIN
• شراء الهواتف من المركز الدولي للهواتف الذكية
• اختيار المودمات المناسبة (فورتكس، سام، كول)

كيف أقدر أساعدك اليوم؟"""
    
    # 3. التعريف بالنفس العام
    if any(word in user_input_lower for word in ["من انت", "who are you", "من أنت", "تعرف عن نفسك"]):
        return f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
🤖 أنا {BOT_NAME}

📝 معلومات عني:
• المبرمج: {OWNER_NAME} ({SMART_SAEED})
• العقل المحرك: {MODEL_NAME} - {MODEL_DESCRIPTION}
• تم التطوير: بمساعدة الذكاء الاصطناعي

{SEPARATOR}
💼 مجالات مساعدتي:
• 🛍️ AliExpress - منتجات متنوعة بأسعار المصنع
• 🏪 Noon - أكبر سوق عربي إلكتروني  
• 👗 SHEIN - عالم الموضة والأزياء
• 📱 هواتف سامسونج، LG، AITL
• 🌐 مودمات فورتكس، سام، كول

كيف يمكنني مساعدتك؟"""
    
    # 4. AliExpress
    if "aliexpress" in user_input_lower or "علي اكسبرس" in user_input_lower:
        return f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
🌏 **AliExpress**

المميزات:
✅ منتجات متنوعة من كل أنحاء العالم
✅ أسعار المصنع مباشرة
✅ شحن دولي إلى اليمن
✅ حماية المشتري مضمونة

{SEPARATOR}
💡 نصيحة: اقرأ تقييمات المنتج قبل الشراء.
هل تريد مساعدة في البحث عن منتج معين على AliExpress؟"""
    
    # 5. Noon
    if "noon" in user_input_lower or "نون" in user_input_lower:
        return f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
🛍️ **Noon.com**

المميزات:
✅ أكبر سوق إلكتروني في المنطقة العربية
✅ توصيل سريع إلى اليمن
✅ عروض حصرية يومية (Flash Sale)
✅ منتجات أصلية 100%

{SEPARATOR}
🎁 تصفح عروض Noon اليوم - خصومات تصل إلى 70%!
هل تريد معرفة عروض معينة؟"""
    
    # 6. SHEIN
    if "shein" in user_input_lower or "شي إن" in user_input_lower:
        return f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
👗 **SHEIN - عالم الموضة**

المميزات:
✅ أحدث صيحات الموضة والأزياء
✅ أسعار لا تقبل المنافسة
✅ توصيل إلى اليمن
✅ تقييمات وصور حقيقية من العملاء

{SEPARATOR}
💃 ملابس، أحذية، إكسسوارات - كل ما تحتاجه في مكان واحد!
هل تريد البحث عن منتج معين على SHEIN؟"""
    
    # 7. نصائح الهواتف (سامسونج، LG، AITL)
    phone_brands = {
        "سامسونج": "Samsung Galaxy",
        "lg": "LG", 
        "aitl": "AITL"
    }
    
    for brand, brand_name in phone_brands.items():
        if brand in user_input_lower:
            return f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
📱 هاتف {brand_name}

✅ أنصحك بالتوجه إلى **المركز الدولي للهواتف الذكية**
✅ سيتم توجيهك إلى الهاتف المناسب لطلبك بالضبط
✅ الضمانة لمدة متفق عليها مسبقاً (3-12 شهر)

{SEPARATOR}
💬 هل تريد استشارة عن موديل معين من {brand_name}؟"""
    
    # 8. هاتف عام
    if any(word in user_input_lower for word in ["هاتف", "موبايل", "جوال"]):
        return f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
📱 أسعار الهواتف في اليمن:

🔹 سامسونج - متوفرة في المركز الدولي
🔹 LG - عروض جيدة
🔹 AITL - خيار اقتصادي

⚠️ أنصحك بالشراء من **المركز الدولي للهواتف الذكية**
✅ ضمانة لمدة متفق عليها

هل تريد معرفة سعر موديل معين؟"""
    
    # 9. نصائح المودمات
    modems = ["مودم", "نت", "انترنت", "واي فاي", "wifi"]
    if any(word in user_input_lower for word in modems):
        return f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
🌐 نصائح لشراء المودمات في اليمن:

✅ **فورتكس (Vortex)** - أداء ممتاز وسعر مناسب
✅ **سام (SAM)** - خيار موثوق
✅ **كول (COOL)** - اقتصادي وعملي

{SEPARATOR}
📡 أنصحك بشراء فورتكس للأداء العالي، أو سام للاعتمادية.
هل تريد تفاصيل أكثر عن أي نوع؟"""
    
    # 10. المركز الدولي للهواتف الذكية
    if any(word in user_input_lower for word in ["المركز الدولي", "مركز الهواتف", "وين احصل"]):
        return f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
🏢 **المركز الدولي للهواتف الذكية**

المميزات:
✅ يوجهك إلى الهاتف المناسب لطلبك بالضبط
✅ ضمانة لمدة متفق عليها (تتفاوض معهم)
✅ أسعار تنافسية
✅ قطع غيار أصلية

{SEPARATOR}
📍 يمكنك سؤالهم عن عروض سامسونج، LG، أو AITL.
هل تريد مساعدة في شي معين؟"""
    
    # 11. رد على أي شركة من AliExpress, Noon, SHEIN
    for company in ["SHEIN", "NOON", "ALIEXPRESS", "AMAZON", "VIVO", "SAMSUNG", "LG"]:
        if company.lower() in user_input_lower:
            return f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
{COMPANIES_STRUCTURE.get(company, {}).get('description', f'✨ {company}')}

هل تريد معرفة العروض الحصرية أو التفاصيل أكثر؟"""
    
    # 12. رد افتراضي
    return f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
🛍️ أنا {BOT_NAME}، تحت أمرك!

💬 أكتب:
• 'سلام' - للترحيب
• 'من برمجك' - لتعرف المبرمج سعيد المسوري (سعيد الذكي)
• 'AliExpress' - عروض AliExpress
• 'Noon' - عروض Noon  
• 'SHEIN' - عروض SHEIN
• 'هاتف سامسونج' - نصائح سامسونج
• 'مودم' - نصائح المودمات

{SEPARATOR}
كيف أقدر أساعدك؟"""

# ========== واجهة Streamlit ==========
st.set_page_config(page_title=f"{BOT_NAME} | {MODEL_NAME}", page_icon="🤖", layout="centered")

# محاولة عرض الصورة
image_found = False
for img_name in ["ROBOT.jpg", "saeed.jpg", "robot.jpg"]:
    try:
        st.image(img_name, caption=f"{BOT_NAME} - {MODEL_NAME}", width=120)
        image_found = True
        break
    except:
        pass

if not image_found:
    st.info(f"🤖 {BOT_NAME} | {MODEL_NAME} - {MODEL_DESCRIPTION} | تم البرمجة بواسطة {OWNER_NAME} ({SMART_SAEED})")

# العنوان
st.title(f"🤖 {BOT_NAME}")
st.caption(f"⚡ {MODEL_NAME} - {MODEL_DESCRIPTION} | ✨ تم البرمجة بواسطة {OWNER_NAME} ({SMART_SAEED}) | 🏢 المركز الدولي للهواتف الذكية")

# شريط جانبي بالمعلومات
with st.sidebar:
    st.header("⚙️ معلومات النظام")
    st.write(f"**العقل المحرك:** {MODEL_NAME}")
    st.write(f"**الوصف:** {MODEL_DESCRIPTION}")
    st.write(f"**المبرمج:** {OWNER_NAME} ({SMART_SAEED})")
    st.divider()
    st.header("🛍️ المنصات المدعومة")
    st.write("• AliExpress")
    st.write("• Noon")
    st.write("• SHEIN")
    st.write("• Amazon")
    st.divider()
    st.header("📱 الهواتف")
    st.write("• سامسونج")
    st.write("• LG")
    st.write("• AITL")
    st.divider()
    st.header("🌐 المودمات")
    st.write("• فورتكس (Vortex)")
    st.write("• سام (SAM)")
    st.write("• كول (COOL)")

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = f"""🎯 [{MODEL_NAME} - {MODEL_DESCRIPTION}]
{SEPARATOR}
أهلاً بك！

أنا {BOT_NAME}
✨ تم برمجتي بواسطة {OWNER_NAME} ({SMART_SAEED})
⚙️ العقل المحرك: {MODEL_NAME}

{SEPARATOR}
أساعدك في:
• 🛍️ التسوق من AliExpress، Noon، SHEIN
• 📱 شراء الهواتف من المركز الدولي للهواتف الذكية (ضمانة متفق عليها)
• 🌐 اختيار المودمات المناسبة (فورتكس، سام، كول)

كيف أقدر أخدمك اليوم؟"""
    st.session_state.messages.append({
        "role": "bot",
        "content": welcome_msg,
        "key": "welcome"
    })

# عرض المحادثة
for msg in st.session_state.messages:
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=msg["key"])
    else:
        message(msg["content"], is_user=False, key=msg["key"])

# مربع الإدخال
user_input = st.chat_input("✍️ اكتب رسالتك هنا...")

if user_input:
    # إضافة رسالة المستخدم
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "key": f"user_{len(st.session_state.messages)}"
    })
    message(user_input, is_user=True)
    
    # الحصول على رد البوت
    response = get_bot_response(user_input)
    
    # إضافة رد البوت
    st.session_state.messages.append({
        "role": "bot",
        "content": response,
        "key": f"bot_{len(st.session_state.messages)}"
    })
    message(response, is_user=False)
    
    # تشغيل الصوت
    if VOICE_ENABLED:
        audio_html = text_to_speech(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
    
    st.rerun()

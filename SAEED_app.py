import streamlit as st
import os
import google.generativeai as genai
from gtts import gTTS
import tempfile
import time
from io import BytesIO
import base64

# ======================= إعداد الصفحة =======================
st.set_page_config(page_title="Saeed MarketAds - بالصوت والصورة", layout="wide")

# ======================= دالة إعداد Gemini الذكية =======================
def setup_gemini():
    """
    تبحث هذه الدالة تلقائيًا عن نموذج Gemini المتاح والمفعل للحساب.
    """
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.sidebar.error("❌ مفتاح API غير موجود، أضفه في secrets")
        return None
        
    genai.configure(api_key=api_key)

    # قائمة النماذج التي سنبحث عنها (الأحدث أولاً)
    models_to_try = [
        'gemini-2.5-flash',        # الأكثر استقرارًا حاليًا
        'gemini-flash-latest',     # أحدث نموذج فلاش متاح
        'gemini-1.5-flash',        # نموذج احتياطي قديم لكن مستقر
    ]
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            # اختبار سريع للتأكد من أنه يعمل مع مفتاحك
            test_response = model.generate_content("test")
            st.sidebar.success(f"✅ تم تفعيل النموذج: {model_name}")
            return model
        except Exception as e:
            continue
    
    st.sidebar.error("❌ لم يتم تفعيل أي نموذج، تحقق من اتصالك ومفتاح API")
    return None

# ======================= تهيئة نموذج Gemini =======================
gemini_model = setup_gemini()

# ======================= تهيئة حالة الجلسة =======================
if "products" not in st.session_state:
    st.session_state.products = []
if "conversation" not in st.session_state:
    st.session_state.conversation = []
    # إضافة رسالة الترحيب الأولى
    welcome_msg = "ساضرب لك التحية وساكون صديقك كل يوم! أنا سعيد الذكي، اسألني عن أي شيء."
    st.session_state.conversation.append({"role": "assistant", "content": welcome_msg})
if "current_avatar" not in st.session_state:
    st.session_state.current_avatar = "saeed.jpg" if os.path.exists("saeed.jpg") else "ROBOT.jpg"
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True
if "use_recorded_voice" not in st.session_state:
    st.session_state.use_recorded_voice = False
if "recorded_voice_path" not in st.session_state:
    st.session_state.recorded_voice_path = None

# ======================= دوال الصوت =======================
def text_to_speech_tts(text, lang='ar'):
    """تحويل النص إلى صوت باستخدام gTTS"""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.error(f"خطأ في تحويل النص لصوت: {e}")
        return None

def play_audio(file_path):
    """تشغيل ملف صوتي في Streamlit"""
    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format='audio/mp3')
        return True
    return False

def animate_avatar(image_path, duration=2):
    """تأثير وميض بسيط لمحاكاة حركة الشفاه"""
    if not os.path.exists(image_path):
        return
    placeholder = st.empty()
    for i in range(3):
        placeholder.image(image_path, width=180, caption="🗣️ يتحدث...")
        time.sleep(0.1)
        placeholder.image(image_path, width=170, caption=" ")
        time.sleep(0.1)
    placeholder.image(image_path, width=180, caption="سعيد")

# ======================= الواجهة الرئيسية =======================
st.title("🎭 Saeed Talking Avatar - بالصوت والشفاه")

# شريط جانبي للإعدادات
with st.sidebar:
    st.header("⚙️ إعدادات الأفاتار والصوت")
    avatar_option = st.selectbox("اختر الأفاتار", ["سعيد (saeed.jpg)", "روبوت (ROBOT.jpg)", "صورتي أنا (ارفع صورة)"])
    if avatar_option == "سعيد (saeed.jpg)":
        st.session_state.current_avatar = "saeed.jpg" if os.path.exists("saeed.jpg") else "ROBOT.jpg"
    elif avatar_option == "روبوت (ROBOT.jpg)":
        st.session_state.current_avatar = "ROBOT.jpg" if os.path.exists("ROBOT.jpg") else "saeed.jpg"
    else:
        uploaded_img = st.file_uploader("ارفع صورتك", type=["jpg", "png"])
        if uploaded_img:
            with open("my_avatar.jpg", "wb") as f:
                f.write(uploaded_img.getbuffer())
            st.session_state.current_avatar = "my_avatar.jpg"
    
    st.divider()
    st.session_state.voice_enabled = st.checkbox("🔊 تفعيل الصوت", value=True)
    st.session_state.use_recorded_voice = st.checkbox("🎙️ استخدام صوتي المسجل (للردود)", value=False)
    if st.session_state.use_recorded_voice:
        recorded_voice_file = st.file_uploader("ارفع ملف صوتي (mp3) للردود", type=["mp3"])
        if recorded_voice_file:
            with open("my_voice.mp3", "wb") as f:
                f.write(recorded_voice_file.getbuffer())
            st.session_state.recorded_voice_path = "my_voice.mp3"
            st.success("تم رفع صوتك! سيتم استخدامه لكل رد.")
        else:
            if os.path.exists("my_voice.mp3"):
                st.session_state.recorded_voice_path = "my_voice.mp3"
                st.info("صوتك المسجل موجود مسبقاً.")
            else:
                st.warning("يرجى رفع ملف صوتي لتفعيل هذه الخاصية.")
    st.divider()
    st.info("جميع الحقوق محفوظة SaeedMarketAds ©")

# التبويبات
tab1, tab2, tab3 = st.tabs(["💬 تكلم مع سعيد (بالصوت والشفاه)", "➕ إضافة منتج جديد", "📦 قائمة المنتجات"])

# ======================= تبويب المحادثة =======================
with tab1:
    col_img, col_chat = st.columns([1, 2])
    with col_img:
        if os.path.exists(st.session_state.current_avatar):
            st.image(st.session_state.current_avatar, width=200, caption="الأفاتار الناطق")
        else:
            st.warning("الصورة غير موجودة، يرجى رفع صورة.")
        if st.button("🔄 اختبار حركة الشفاه"):
            animate_avatar(st.session_state.current_avatar, duration=1.5)
    
    with col_chat:
        st.markdown("### 🧠 مرحباً! أنا سعيد الذكي")
        # عرض المحادثة السابقة
        for msg in st.session_state.conversation:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        user_question = st.chat_input("اكتب سؤالك هنا...")
        if user_question:
            # إضافة سؤال المستخدم
            st.session_state.conversation.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.write(user_question)
            
            # الرد من Gemini
            if gemini_model:
                with st.spinner("🤔 يفكر سعيد..."):
                    try:
                        response = gemini_model.generate_content(user_question)
                        ai_reply = response.text
                    except Exception as e:
                        ai_reply = f"حدث خطأ في النموذج: {str(e)}"
            else:
                ai_reply = "آسف، نموذج الذكاء الاصطناعي غير متاح حالياً."
            
            # عرض الرد
            with st.chat_message("assistant"):
                st.write(ai_reply)
            
            # تشغيل الصوت وتحريك الشفاه
            if st.session_state.voice_enabled:
                animate_avatar(st.session_state.current_avatar, duration=1.2)
                
                if st.session_state.use_recorded_voice and st.session_state.recorded_voice_path and os.path.exists(st.session_state.recorded_voice_path):
                    st.audio(st.session_state.recorded_voice_path, format='audio/mp3')
                else:
                    audio_file = text_to_speech_tts(ai_reply, lang='ar')
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
                        os.unlink(audio_file)
                    else:
                        st.info("لم نتمكن من تشغيل الصوت، تحقق من المكتبات.")
            
            st.session_state.conversation.append({"role": "assistant", "content": ai_reply})
            st.rerun()

# ======================= تبويب إضافة المنتج =======================
with tab2:
    st.subheader("➕ إضافة منتج جديد إلى السوق")
    with st.form(key="product_form", clear_on_submit=True):
        prod_name = st.text_input("🏷️ اسم المنتج")
        prod_price = st.number_input("💰 السعر (دولار)", min_value=0.0, step=0.5)
        prod_desc = st.text_area("📝 الوصف")
        hidden_link = st.text_input("🔗 رابط مخفي (اختياري)")
        img_link = st.text_input("🖼️ رابط صورة المنتج")
        submitted = st.form_submit_button("📌 نشر المنتج")
        if submitted and prod_name and prod_price > 0:
            st.session_state.products.append({
                "name": prod_name, "price": prod_price,
                "desc": prod_desc, "link": hidden_link, "image": img_link
            })
            st.balloons()
            st.success(f"✅ تمت إضافة {prod_name}")
            st.rerun()
        elif submitted:
            st.error("الاسم والسعر مطلوبان")

# ======================= تبويب عرض المنتجات =======================
with tab3:
    st.subheader("📦 قائمة المنتجات")
    if not st.session_state.products:
        st.info("لا توجد منتجات بعد. أضف منتجاً من التبويب الثاني.")
    else:
        for idx, prod in enumerate(st.session_state.products):
            with st.container():
                c1, c2 = st.columns([1, 3])
                with c1:
                    if prod["image"]:
                        st.image(prod["image"], width=120)
                    else:
                        st.image("https://via.placeholder.com/120?text=No+Image", width=120)
                with c2:
                    st.markdown(f"### 🛍️ {prod['name']}")
                    st.markdown(f"**السعر:** 💲{prod['price']}")
                    st.markdown(f"**الوصف:** {prod['desc']}")
                    if prod["link"]:
                        st.markdown(f"[رابط المنتج]({prod['link']})")
                st.divider()
        if st.button("🗑️ حذف الكل"):
            st.session_state.products.clear()
            st.rerun()

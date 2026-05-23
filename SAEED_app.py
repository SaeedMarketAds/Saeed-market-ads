import streamlit as st
import google.generativeai as genai
import requests

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Saeed DataBot 2026", layout="centered")

# --- إعداد المفاتيح ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"] 
except:
    st.error("تنبيه: تأكد من ضبط Secrets في Streamlit.")

st.title("🤖 Saeed DataBot 2026 - لوحة الإدارة")

# --- الإدخال النصي (للحفاظ على بطارية الهاتف) ---
user_input = st.text_area("أدخل فكرتك أو المنتج المراد تسويقه:", height=150)

if st.button("🚀 توليد الإعلان والمشهد البصري"):
    if user_input:
        with st.spinner("جاري صياغة المحتوى الخارق..."):
            model = genai.GenerativeModel("gemini-1.5-flash") # تم الاعتماد على النسخة فائقة السرعة
            
            # توجيه البوت ليعطيك نصاً وفكرة تصوير جاهزة للأفاتار
            prompt = (
                f"أنت (Saeed DataBot) الذكاء الاصطناعي المبتكر للمطور سعيد المسوري. "
                f"صغ منشوراً تسويقياً جذاباً ومحترفاً لمنتج: {user_input}. "
                "بعد المنشور، اكتب (وصف مشهد بصري) بسيط ومحدد يمكنني استخدامه في موقع D-ID "
                "ليتحدث الأفاتار الخاص بي ويجذب المتابعين. "
                "حلل البيانات، استخدم جداول إذا لزم الأمر، واختم بـ: 'يمكنكم البحث في كل مكان عن: saeedmarketads' والوسم #saeedmarketads."
            )
            
            response = model.generate_content(prompt)
            result = response.text
            
            # --- حفظ وعرض النتيجة ---
            st.session_state.bot_response = result
            st.markdown("### 📝 المخرجات:")
            st.write(result)
            
            # --- إرسال تلقائي للتليجرام ---
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": result, "parse_mode": "Markdown"})
            
            st.success("✅ تم الإرسال إلى التليجرام وجاهز للنشر!")
    else:
        st.warning("الرجاء كتابة المحتوى أولاً.")

# --- عرض آخر نتيجة ---
if "bot_response" in st.session_state and st.session_state.bot_response:
    if st.button("إعادة إرسال للتليجرام"):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": st.session_state.bot_response, "parse_mode": "Markdown"})
        st.info("تم إعادة الإرسال!")

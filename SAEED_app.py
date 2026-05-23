import streamlit as st
import google.generativeai as genai
import requests

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Saeed DataBot 2026", layout="centered")

# --- إعداد المفاتيح ---
def get_secrets():
    try:
        return st.secrets["GEMINI_API_KEY"], st.secrets["TELEGRAM_BOT_TOKEN"], st.secrets["TELEGRAM_CHAT_ID"]
    except Exception:
        return None, None, None

api_key, bot_token, chat_id = get_secrets()

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("مفتاح GEMINI_API_KEY مفقود في الإعدادات.")

st.title("🤖 Saeed DataBot 2026")

user_input = st.text_area("أدخل فكرتك أو المنتج:", height=150)

if st.button("🚀 توليد الإعلان"):
    if user_input and api_key and bot_token and chat_id:
        with st.spinner("جاري التوليد..."):
            try:
                # استخدام التعريف المحدث
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                
                prompt = (
                    f"صغ منشوراً تسويقياً لمنتج: {user_input}. "
                    "أضف وصفاً لمشهد بصري. "
                    "اختم بـ: 'يمكنكم البحث في كل مكان عن: saeedmarketads' والوسم #saeedmarketads."
                )
                
                response = model.generate_content(prompt)
                
                if response.text:
                    result = response.text
                    st.session_state.bot_response = result
                    st.markdown("### 📝 المخرجات:")
                    st.write(result)
                    
                    # إرسال للتليجرام مع ترميز صحيح
                    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                    payload = {"chat_id": chat_id, "text": result}
                    res = requests.post(url, json=payload)
                    
                    if res.status_code == 200:
                        st.success("✅ تم الإرسال للتليجرام!")
                    else:
                        st.error(f"خطأ في إرسال التليجرام: {res.text}")
                else:
                    st.error("لم يقم النموذج بتوليد أي نص.")
                    
            except Exception as e:
                st.error(f"خطأ برمجي: {str(e)}")
    else:
        st.warning("تأكد من إدخال النص وإعداد المفاتيح في Secrets.")

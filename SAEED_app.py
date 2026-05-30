import streamlit as st
import google.generativeai as genai

# 1. إعداد الـ API
genai.configure(api_key="YOUR_API_KEY_HERE")

# إعداد النموذج مع ضبط الإبداع (Temperature)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # يفضل استخدام الإصدارات الأحدث مثل flash أو pro
    generation_config={"temperature": 0.7}
)

# 2. تهيئة محرك الدردشة في الذاكرة (لضمان استمرارية السياق)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 3. عرض الرسائل السابقة عند تحديث الصفحة
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- واجهة المساعد الذكي ---
st.title("نظام سعيد المتكامل 🚀")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة إدخال الرسائل
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # إضافة رسالة المستخدم للسجل
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # الرد الذكي
    with st.chat_message("assistant"):
        with st.spinner("سعيد يفكّر..."):
            try:
                # استخدام chat_session لإرسال الرسالة مع الاحتفاظ بالسياق
                response = st.session_state.chat_session.send_message(prompt)
                full_response = response.text
                
                st.markdown(full_response)
                # إضافة رد الروبوت للسجل
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

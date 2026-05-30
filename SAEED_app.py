import streamlit as st
import google.generativeai as genai

# إعداد مفتاح API
api_key = st.secrets["GOOGLE_API_KEY"]

# إعداد API
genai.configure(api_key=api_key)

# إعداد النموذج
model = genai.GenerativeModel(
    mصحيح# غيّر السطر الموجود في الكود الخاص بك إلى هذا:
model_name="models/gemini-3.5-flash"
صحيح
    generation_config={"temperature": 0.7}
)

# إذا لم تكن موجودة إنشاء الجلسة
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# إعداد سجل الرسائل
if 'messages' not in st.session_state:
    st.session_state.messages = []

# عرض واجهة التطبيق
st.title("سعيد ماركت")

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم
if prompt := st.chat_input("ما الذي تحتاجه؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("سعيد يجيب..."):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

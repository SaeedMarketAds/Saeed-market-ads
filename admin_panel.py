import streamlit as st
import json
import os

SUBMISSIONS_FILE = 'pending_submissions.json'

def load_submissions():
    if os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, 'r') as f:
            return json.load(f)
    return []

st.title("لوحة تحكم المدير - saeedmarketads")

submissions = load_submissions()

if not submissions:
    st.info("لا توجد طلبات جديدة من التجار حالياً.")
else:
    for i, sub in enumerate(submissions):
        with st.expander(f"طلب من: {sub['merchant']} - المنتج: {sub['product']}"):
            st.write(f"رابط المنتج: {sub['link']}")
            st.write(f"وسيلة التواصل: {sub['contact']}")
            
            if st.button(f"موافقة على الطلب {i}"):
                # هنا ستضيف كود نقل البيانات للملف المعتمد
                st.success("تمت الموافقة! سيظهر المنتج في المنصة.")


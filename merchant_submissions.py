import streamlit as st
import json
import os

# 1. إعداد مسار ملف التخزين المؤقت (قاعدة بيانات التجار)
SUBMISSIONS_FILE = 'pending_submissions.json'

def save_submission(data):
    # حفظ طلب التاجر في ملف انتظار للمراجعة
    submissions = []
    if os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, 'r') as f:
            submissions = json.load(f)
    
    submissions.append(data)
    with open(SUBMISSIONS_FILE, 'w') as f:
        json.dump(submissions, f)

# 2. واجهة التاجر (النموذج)
st.title("بوابة التجار - saeedmarketads")
with st.form("merchant_form"):
    merchant_name = st.text_input("اسم المتجر")
    product_name = st.text_input("اسم المنتج")
    product_link = st.text_input("رابط المنتج")
    contact_info = st.text_input("وسيلة التواصل الرسمية")
    
    submit = st.form_submit_button("إرسال المنتج للمراجعة")
    
    if submit:
        submission_data = {
            "merchant": merchant_name,
            "product": product_name,
            "link": product_link,
            "contact": contact_info,
            "status": "pending"
        }
        save_submission(submission_data)
        st.success("تم استلام طلبك بنجاح! سيقوم فريق saeedmarketads بمراجعته.")


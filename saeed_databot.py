import streamlit as st
import pandas as pd
import os

st.title("📦 لوحة تحكم سعيد ماركت")
st.subheader("إضافة منتج جديد")

# إنشاء نموذج إدخال
with st.form("product_form", clear_on_submit=True):
    product_name = st.text_input("اسم المنتج")
    product_price = st.number_input("السعر", min_value=0.0)
    product_desc = st.text_area("وصف المنتج")
    submitted = st.form_submit_button("نشر المنتج")

    if submitted:
        if product_name and product_price:
            # حفظ البيانات (يمكنك لاحقاً ربطها بقاعدة بيانات)
            new_data = pd.DataFrame([[product_name, product_price, product_desc]], 
                                    columns=["الاسم", "السعر", "الوصف"])
            
            # إضافة البيانات لملف CSV
            file_path = "products.csv"
            if os.path.exists(file_path):
                new_data.to_csv(file_path, mode='a', header=False, index=False, encoding='utf-8-sig')
            else:
                new_data.to_csv(file_path, index=False, encoding='utf-8-sig')
            
            st.success(f"تم إضافة المنتج '{product_name}' بنجاح!")
        else:
            st.error("يرجى ملء البيانات الأساسية.")

# عرض المنتجات الموجودة
st.divider()
st.subheader("قائمة المنتجات الحالية")
if os.path.exists("products.csv"):
    df = pd.read_csv("products.csv")
    st.table(df)
else:
    st.info("لا توجد منتجات حالياً.")

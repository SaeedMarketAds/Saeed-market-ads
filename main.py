import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="SaeeD DaTaBoT", page_icon="🛒", layout="wide")

# 2. وظيفة تحميل البيانات (من ملف products.csv)
@st.cache_data
def load_data():
    # تأكد أن ملف products.csv موجود في نفس المجلد
    return pd.read_csv('products.csv')

# 3. واجهة المستخدم
st.title("🛒 SaeeD DaTaBoT - لوحة التحكم")

try:
    df = load_data()
    
    # عرض البيانات في جدول تفاعلي
    st.subheader("قائمة المنتجات المتاحة")
    st.dataframe(df, use_container_width=True)

    # فلترة العروض الذهبية (خصم 50% فأكثر)
    st.header("🔥 العروض الذهبية")
    deals = df[df['discount'] >= 50]
    
    if not deals.empty:
        st.table(deals[['name', 'price', 'discount', 'link']])
    else:
        st.write("لا توجد عروض حالياً.")

except FileNotFoundError:
    st.error("خطأ: لم يتم العثور على ملف products.csv. يرجى التأكد من رفعه!")
except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")

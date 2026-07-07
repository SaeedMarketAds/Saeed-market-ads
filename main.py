hereimport pandas as pd

def load_products(file_path):
    try:
        # قراءة ملف CSV
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        return "خطأ: الملف غير موجود."

# تشغيل البرنامج
if __name__ == "__main__":
    file_name = 'products.csv'
    products = load_products(file_name)
    
    if isinstance(products, pd.DataFrame):
        print("تم تحميل المنتجات بنجاح:")
        print(products.head()) # عرض أول 5 منتجات
    else:
        print(products)

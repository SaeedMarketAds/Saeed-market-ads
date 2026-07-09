# data_center.py

# 1. إعدادات النظام
CONFIG = {
    "app_name": "Saeed MarketAds",
    "version": "1.0",
    "developer": "Saeed Al-Maswari"
}

# 2. قائمة المنتجات الرئيسية (للاستيراد)
PRODUCTS = [
    {"sku": "SH-001", "name": "معطف شتوي", "price": 19.99, "store": "SHEIN", "type": "Global", "image": ""},
    {"sku": "N-001", "name": "ساعة يد رقمية", "price": 89.00, "store": "Noon", "type": "Global", "image": ""},
    {"sku": "AE-101", "name": "مكنسة كهربائية", "price": 96.50, "store": "AliExpress", "type": "Global", "image": ""},
    {"sku": "AE-102", "name": "سماعات TWS", "price": 2.48, "store": "AliExpress", "type": "Global", "image": ""},
    {"sku": "YEM-001", "name": "عسل سدر طبيعي", "price": 50000, "store": "Yemeni_Local", "type": "Local", "image": ""},
]

# 3. منتجات SHEIN (للعرض المباشر)
SHEIN_PRODUCTS = [
    {"code": "SH001", "name": "معطف مبطن بغطاء رأس للفتيات", "price": 19.39, "discount": 43, "link": "https://onelink.shein.com/38/5shrzfcizjmg", "sales": "150+"},
    {"code": "SH002", "name": "قميص أنيق بتصميم هونج كونج", "price": 14.18, "discount": 37, "link": "https://onelink.shein.com/38/5shune7n90yf", "sales": "200+"},
    {"code": "SH003", "name": "نظارات حفلات مطبوعة 6 قطع", "price": 2.70, "discount": 0, "link": "https://onelink.shein.com/38/5shujg5f2ywk", "sales": "300+"},
    {"code": "SH004", "name": "حقيبة مستلزمات سفر مقاومة للماء", "price": 3.90, "discount": 17, "link": "https://onelink.shein.com/38/5shuimjyfjt7", "sales": "100+"},
    {"code": "SH005", "name": "معطف رجالي كاجوال سادة", "price": 25.67, "discount": 24, "link": "https://onelink.shein.com/38/5shui8qqn60h", "sales": "200+"},
]

# 4. العروض الذهبية
GOLDEN_DEALS = [
    {"name": "Men Ice Silk Polo Shirt", "price": 4.71, "discount": 60, "link": "#", "sales": "500+"},
    {"name": "Pajama Set Button Front", "price": 6.91, "discount": 69, "link": "#", "sales": "300+"},
    {"name": "Shower Curtain Set", "price": 4.47, "discount": 70, "link": "#", "sales": "200+"},
    {"name": "Sports Waist Belt", "price": 5.12, "discount": 61, "link": "#", "sales": "400+"},
]

# -*- coding: utf-8 -*-

# 1. قسم الإعدادات الشاملة (للبوت والتطبيق والأسواق)
CONFIG = {
    "app_name": "Saeed MarketAds",
    "version": "3.5",
    "default_currency": "SAR",
    "yemen_currency": "YER",
    "admin_email": "admin@saeedmarket.com",
    # الأسواق المدعومة (يمكنك إضافة أي سوق جديد هنا بسهولة)
    "supported_markets": ["SHEIN", "Noon", "AliExpress", "Yemeni_Local"],
}

# 2. قاعدة بيانات المنتجات (مبنية بنظام التصنيف للمرونة)
PRODUCTS = [
    # --- منتجات عالمية ---
    {"sku": "SH001", "name": "معطف مبطن", "price": 19.39, "store": "SHEIN", "type": "Global"},
    {"sku": "N001", "name": "ساعة ذكية", "price": 89.99, "store": "Noon", "type": "Global"},
    
    # --- منتجات تجار اليمن (هنا ستتم إضافة بيانات الـ merchant_submissions.py) ---
    {"sku": "YEM-001", "name": "عسل سدر أصلي", "price": 50000, "store": "Yemeni_Local", "type": "Local"},
    {"sku": "YEM-002", "name": "بن خولاني فاخر", "price": 15000, "store": "Yemeni_Local", "type": "Local"},
]

# 3. قسم تجار اليمن (سجل المتاجر المحلية المعتمدة)
MERCHANTS = [
    {"merchant_id": "M001", "name": "مؤسسة التاجر اليمني", "category": "Food", "status": "Verified"},
    {"merchant_id": "M002", "name": "أزياء صنعاء", "category": "Fashion", "status": "Pending"},
]


import os

# ========== جميع منتجات SHEIN مترجمة للعربية (50+ منتج) ==========
SHEIN_PRODUCTS = [
    {"name": "معطف مبطن بغطاء رأس للفتيات", "price": 19.39, "discount": 43, "link": "https://onelink.shein.com/38/5shrzfcizjmg", "sales": "150+"},
    {"name": "قميص أنيق بتصميم هونج كونج", "price": 14.18, "discount": 37, "link": "https://onelink.shein.com/38/5shune7n90yf", "sales": "200+"},
    {"name": "نظارات حفلات مطبوعة 6 قطع", "price": 2.70, "discount": 0, "link": "https://onelink.shein.com/38/5shujg5f2ywk", "sales": "300+"},
    {"name": "حقيبة مستلزمات سفر مقاومة للماء", "price": 3.90, "discount": 17, "link": "https://onelink.shein.com/38/5shuimjyfjt7", "sales": "100+"},
    {"name": "معطف رجالي كاجوال سادة", "price": 25.67, "discount": 24, "link": "https://onelink.shein.com/38/5shui8qqn60h", "sales": "200+"},
    {"name": "أقراط زهرية بتصميم لافت", "price": 1.44, "discount": 4, "link": "https://onelink.shein.com/38/5shtox57cemc", "sales": "300+"},
    {"name": "ربطات شعر ملونة 5 قطع", "price": 1.50, "discount": 38, "link": "https://onelink.shein.com/38/5shtobfv3sxn", "sales": "800+"},
    {"name": "أحذية رياضية نسائية كاجوال", "price": 5.00, "discount": 82, "link": "https://onelink.shein.com/38/5shtl502kmcf", "sales": "200+"},
    {"name": "مجموعة خواتم زهور وردية", "price": 2.16, "discount": 6, "link": "https://onelink.shein.com/38/5shtkl9rhh8f", "sales": "500+"},
    {"name": "دلو أرز مع كوب قياس", "price": 8.84, "discount": 70, "link": "https://onelink.shein.com/38/5shtjtnbwphj", "sales": "200+"},
    {"name": "أقراط هوب مطلية بالذهب 3 أزواج", "price": 1.43, "discount": 5, "link": "https://onelink.shein.com/38/5shti8ffmexk", "sales": "50+"},
    {"name": "شعر مستعار قصير مجعد", "price": 2.70, "discount": 33, "link": "https://onelink.shein.com/38/5shthyka1fts", "sales": "100+"},
    {"name": "حذاء تزلج بإضاءة LED للأطفال", "price": 34.72, "discount": 37, "link": "https://onelink.shein.com/38/5shthetyxlby", "sales": "50+"},
    {"name": "طقم مقص أظافر احترافي", "price": 1.40, "discount": 36, "link": "https://onelink.shein.com/38/5shtg7fahsfp", "sales": "1200+"},
    {"name": "هاتف لعبة موسيقي تعليمي", "price": 3.40, "discount": 0, "link": "https://onelink.shein.com/38/5shtfvl3s22n", "sales": "50+"},
    {"name": "شريط إضاءة RGB LED", "price": 2.27, "discount": 55, "link": "https://onelink.shein.com/38/5shtfbusmt15", "sales": "200+"},
    {"name": "طقم بيسبول للأولاد تيشيرت وشورت", "price": 3.28, "discount": 80, "link": "https://onelink.shein.com/38/5shtek8d4572", "sales": "100+"},
    {"name": "شريط لاصق مزدوج قوي", "price": 1.05, "discount": 30, "link": "https://onelink.shein.com/38/5shtead7hrfl", "sales": "800+"},
    {"name": "طبق طعام محكم الإغلاق 24 قطعة", "price": 7.14, "discount": 60, "link": "https://onelink.shein.com/38/5shtdonvakbf", "sales": "150+"},
    {"name": "حقيبة شاطئ كبيرة السعة", "price": 2.34, "discount": 57, "link": "https://onelink.shein.com/38/5shtcj87y44e", "sales": "100+"},
    {"name": "طقم بيجامة صيفية للأولاد", "price": 6.19, "discount": 42, "link": "https://onelink.shein.com/38/5shtc1gxxmda", "sales": "600+"},
    {"name": "أظافر صناعية فرنسية 24 قطعة", "price": 1.35, "discount": 41, "link": "https://onelink.shein.com/38/5sht8yz7kfv1", "sales": "200+"},
    {"name": "تيشيرت مدرسي بقوس وردي", "price": 4.09, "discount": 47, "link": "https://onelink.shein.com/38/5sht8r3347y5", "sales": "800+"},
    {"name": "حامل هاتف قابل للطي محمول", "price": 1.30, "discount": 24, "link": "https://onelink.shein.com/38/5sht5cr65itw", "sales": "100+"},
    {"name": "طقم مناشف مخططة سريعة الجفاف", "price": 2.34, "discount": 38, "link": "https://onelink.shein.com/38/5sht12urdy18", "sales": "200+"},
    {"name": "شريط مانع لتسرب المياه", "price": 1.70, "discount": 0, "link": "https://onelink.shein.com/38/5sht0h5f61jc", "sales": "300+"},
    {"name": "مقص دجاج متعدد الاستخدامات", "price": 2.70, "discount": 23, "link": "https://onelink.shein.com/38/5shszze54ug2", "sales": "300+"},
    {"name": "طقم قميص وبنطلون رجالي", "price": 7.77, "discount": 70, "link": "https://onelink.shein.com/38/5shsz9qqou3d", "sales": "50+"},
    {"name": "طقم موس حاجب 30 قطعة", "price": 0.75, "discount": 32, "link": "https://onelink.shein.com/38/5shsyi4b2nub", "sales": "500+"},
    {"name": "فرجار رقمي 6 بوصة", "price": 1.71, "discount": 10, "link": "https://onelink.shein.com/38/5shsxydzzinl", "sales": "200+"},
    {"name": "حزام رجالي بإبزيم أوتوماتيكي", "price": 2.93, "discount": 38, "link": "https://onelink.shein.com/38/5shsxapmkr2h", "sales": "500+"},
    {"name": "شفاطات لامعة قابلة لإعادة الاستخدام", "price": 0.99, "discount": 18, "link": "https://onelink.shein.com/38/5shswb72kgum", "sales": "600+"},
    {"name": "واقي شاشة ضد التجسس", "price": 1.63, "discount": 49, "link": "https://onelink.shein.com/38/5shsw790bnla", "sales": "800+"},
    {"name": "مشط قابل للطي مع مرآة", "price": 1.90, "discount": 32, "link": "https://onelink.shein.com/38/5shsw1bwzhq8", "sales": "800+"},
    {"name": "لعبة ضغط بيضاوية مخططة", "price": 2.97, "discount": 10, "link": "https://onelink.shein.com/38/5shsvxdus31c", "sales": "200+"},
    {"name": "حزام كلب مبطن وعاكس", "price": 3.30, "discount": 25, "link": "https://onelink.shein.com/38/5shsvrgrgmbu", "sales": "50+"},
    {"name": "غطاء حماية شاحن 3 قطع", "price": 1.13, "discount": 25, "link": "https://onelink.shein.com/38/5shsvboiirzh", "sales": "900+"},
    {"name": "طقم فرش مكياج 3 قطع", "price": 1.05, "discount": 48, "link": "https://onelink.shein.com/38/5shsv5rf6m2j", "sales": "1000+"},
    {"name": "فاتحة علب 4 في 1", "price": 1.08, "discount": 23, "link": "https://onelink.shein.com/38/5shsuk22y0h7", "sales": "200+"},
    {"name": "شارة أنمي دبوس", "price": 1.65, "discount": 21, "link": "https://onelink.shein.com/38/5shstycqq3uz", "sales": "100+"},
    {"name": "رأس دش مطري عالي الضغط", "price": 12.64, "discount": 65, "link": "https://onelink.shein.com/38/5shst4ra0l06", "sales": "200+"},
    {"name": "مكواة فرد وتجعيد شعر سيراميك", "price": 26.90, "discount": 20, "link": "https://onelink.shein.com/38/5shsrzbmou3o", "sales": "100+"},
    {"name": "زجاجة رش زيت للطبخ", "price": 1.17, "discount": 22, "link": "https://onelink.shein.com/38/5shsrvdkg0tg", "sales": "500+"},
    {"name": "مشابك تثبيت لحاف 4 قطع", "price": 3.33, "discount": 5, "link": "https://onelink.shein.com/38/5shsrnhfz3p0", "sales": "200+"},
    {"name": "نظارات حجب الضوء الأزرق", "price": 5.22, "discount": 50, "link": "https://onelink.shein.com/38/5shsqvv0f19e", "sales": "100+"},
    {"name": "أداة تقليم القدم", "price": 1.10, "discount": 8, "link": "https://onelink.shein.com/38/5shspqfd1vtf", "sales": "300+"},
    {"name": "أساور خرز خشبي", "price": 1.80, "discount": 25, "link": "https://onelink.shein.com/38/5shsp8o323az", "sales": "100+"},
    {"name": "ورق زبدة للمقلاة الهوائية", "price": 1.26, "discount": 21, "link": "https://onelink.shein.com/38/5shsof2mdyzs", "sales": "300+"},
    {"name": "أظافر فرنسية للمانيكير 48 قطعة", "price": 1.30, "discount": 35, "link": "https://onelink.shein.com/38/5shso76hvn95", "sales": "300+"},
    {"name": "سوار ساعة أبل جلد أصلي", "price": 5.89, "discount": 5, "link": "https://onelink.shein.com/38/5shs5kbzkzl4", "sales": "100+"},
    {"name": "حمالة هاتف فراشة مع كريستال", "price": 2.48, "discount": 25, "link": "https://onelink.shein.com/38/5shs5gdxezhw", "sales": "150+"},
]

# ========== توليد ملف HTML ==========
def generate_full_html():
    products_html = ""
    for p in SHEIN_PRODUCTS:
        final_price = p['price'] * (1 - p['discount']/100) if p['discount'] > 0 else p['price']
        sales_html = f'<div class="sales">🛍️ {p.get("sales", "50+")} تم البيع</div>'
        discount_html = f'<span class="discount">-{p["discount"]}%</span>' if p['discount'] > 0 else ''
        old_price_html = f'<span class="old-price">${p["price"]:.2f}</span>' if p['discount'] > 0 else ''
        
        products_html += f'''
        <div class="product-card" onclick="window.open('{p['link']}', '_blank')">
            <div class="product-image">📦</div>
            <div class="product-info">
                <h3>{p['name']}</h3>
                <div class="price">
                    ${final_price:.2f} {old_price_html} {discount_html}
                </div>
                {sales_html}
                <button class="buy-btn">🛒 تسوق الآن</button>
            </div>
        </div>
        '''
    
    return f'''<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>متجر سعيد | منتجات SHEIN</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Cairo', 'Tajawal', Arial, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); padding: 20px; }}
        .container {{ max-width: 1200px; margin: auto; }}
        .header {{ text-align: center; color: white; margin-bottom: 30px; }}
        .header h1 {{ font-size: 35px; }}
        .coupon-box {{ background: white; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 30px; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
        .coupon-code {{ background: #ff4757; color: white; display: inline-block; padding: 8px 20px; border-radius: 50px; font-size: 22px; margin-top: 10px; }}
        .products-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
        .product-card {{ background: white; border-radius: 15px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); cursor: pointer; transition: transform 0.3s; }}
        .product-card:hover {{ transform: translateY(-5px); }}
        .product-image {{ font-size: 48px; text-align: center; padding: 10px; }}
        .product-info h3 {{ font-size: 16px; margin-bottom: 10px; color: #333; }}
        .price {{ color: #ff4757; font-weight: bold; font-size: 22px; margin: 10px 0; }}
        .old-price {{ text-decoration: line-through; color: #999; font-size: 14px; margin-right: 8px; }}
        .discount {{ background: #ff4757; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; margin-right: 8px; }}
        .sales {{ color: #28a745; font-size: 12px; margin: 5px 0; }}
        .buy-btn {{ background: linear-gradient(90deg, #667eea, #764ba2); color: white; border: none; width: 100%; padding: 10px; border-radius: 8px; margin-top: 10px; cursor: pointer; font-weight: bold; }}
        .footer {{ text-align: center; color: white; margin-top: 40px; padding: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛍️ متجر سعيد - منتجات SHEIN</h1>
            <p>أحدث الصيحات بأفضل الأسعار</p>
        </div>
        <div class="coupon-box" onclick="copyCoupon()">
            🎁 عرض خاص للمستخدمين الجدد 🎁
            <div class="coupon-code">🏷️ كود الخصم: WL7KA</div>
            <div>🔥 خصم يصل إلى 60% - اضغط لنسخ الكود</div>
        </div>
        <div class="products-grid">
            {products_html}
        </div>
        <div class="footer">
            <p>© 2026 سوق سعيد - كود الخصم WL7KA | خصم 60% للمستخدمين الجدد</p>
        </div>
    </div>
    <script>
        function copyCoupon() {{
            navigator.clipboard.writeText('WL7KA');
            alert('✅ تم نسخ كود الخصم: WL7KA\\nاستخدمه عند الدفع للحصول على خصم 60%');
        }}
    </script>
</body>
</html>'''

# ========== حفظ الملف ==========
with open('shein_store.html', 'w', encoding='utf-8') as f:
    f.write(generate_full_html())

print("=" * 55)
print("✅ تم تحديث المتجر بنجاح!")
print(f"📊 عدد المنتجات: {len(SHEIN_PRODUCTS)} منتج")
print("🎁 كود الخصم: WL7KA (خصم 60%)")
print("📁 الملف: shein_store.html")
print("=" * 55)

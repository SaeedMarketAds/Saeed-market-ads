import os

# ========== جميع منتجات SHEIN مترجمة للعربية ==========
SHEIN_PRODUCTS = [
    {"name": "معطف مبطن مقنّع للبنات الصغيرات - Playful Pals", "price": 19.39, "discount": 43, "link": "https://onelink.shein.com/38/5shrzfcizjmg", "sales": "150+"},
    {"name": "قميص أنيق طويل الأكمام بأزرار أمامية - موضة هونغ كونغ", "price": 14.18, "discount": 37, "link": "https://onelink.shein.com/38/5shune7n90yf", "sales": "200+"},
    {"name": "نظارات حفلات K-POP مطبوعة - 6 قطع", "price": 2.70, "discount": 0, "link": "https://onelink.shein.com/38/5shujg5f2ywk", "sales": "300+"},
    {"name": "حقيبة سفر متعددة الألوان - مقاومة للماء", "price": 3.90, "discount": 17, "link": "https://onelink.shein.com/38/5shuimjyfjt7", "sales": "100+"},
    {"name": "معطف رجالي بقصة عادية - Manfinity", "price": 25.67, "discount": 24, "link": "https://onelink.shein.com/38/5shui8qqn60h", "sales": "200+"},
    {"name": "أقراط زهور بتصميم مبالغ فيه - زوج واحد", "price": 1.44, "discount": 4, "link": "https://onelink.shein.com/38/5shtox57cemc", "sales": "300+"},
    {"name": "أربطة شعر بألوان قوس قزح - 5 قطع", "price": 1.50, "discount": 38, "link": "https://onelink.shein.com/38/5shtobfv3sxn", "sales": "800+"},
    {"name": "حذاء رياضي كاجوال نسائي - 2025", "price": 5.00, "discount": 82, "link": "https://onelink.shein.com/38/5shtl502kmcf", "sales": "200+"},
    {"name": "طقم خواتم وردي زهري قابل للتعديل - 4 قطع", "price": 2.16, "discount": 6, "link": "https://onelink.shein.com/38/5shtkl9rhh8f", "sales": "500+"},
    {"name": "وعاء أرز مع كوب قياس - سعة كبيرة", "price": 8.84, "discount": 70, "link": "https://onelink.shein.com/38/5shtjtnbwphj", "sales": "200+"},
    {"name": "أقراط هوب مطلية بالذهب عيار 18 - 3 أزواج", "price": 1.43, "discount": 5, "link": "https://onelink.shein.com/38/5shti8ffmexk", "sales": "50+"},
    {"name": "شعر مستعار قصير مجعد - ذيل حصان", "price": 2.70, "discount": 33, "link": "https://onelink.shein.com/38/5shthyka1fts", "sales": "100+"},
    {"name": "حذاء تزلج بإضاءة LED - للأطفال", "price": 34.72, "discount": 37, "link": "https://onelink.shein.com/38/5shthetyxlby", "sales": "50+"},
    {"name": "طقم مقص أظافر - 18/9/6 قطع", "price": 1.40, "discount": 36, "link": "https://onelink.shein.com/38/5shtg7fahsfp", "sales": "1200+"},
    {"name": "هاتف لعبة نحلة موسيقي - تعليمي", "price": 3.40, "discount": 0, "link": "https://onelink.shein.com/38/5shtfvl3s22n", "sales": "50+"},
    {"name": "شريط إضاءة RGB LED - USB", "price": 2.27, "discount": 55, "link": "https://onelink.shein.com/38/5shtfbusmt15", "sales": "200+"},
    {"name": "طقم بيسبول للأولاد - تيشيرت وشورت", "price": 3.28, "discount": 80, "link": "https://onelink.shein.com/38/5shtek8d4572", "sales": "100+"},
    {"name": "شريط لاصق مزدوج الوجه - قوي", "price": 1.05, "discount": 30, "link": "https://onelink.shein.com/38/5shtead7hrfl", "sales": "800+"},
    {"name": "طبق طعام محكم الإغلاق - 24 قطعة", "price": 7.14, "discount": 60, "link": "https://onelink.shein.com/38/5shtdonvakbf", "sales": "150+"},
    {"name": "حقيبة شاطئ كبيرة السعة", "price": 2.34, "discount": 57, "link": "https://onelink.shein.com/38/5shtcj87y44e", "sales": "100+"},
    {"name": "طقم بيجامة صيفية للأولاد", "price": 6.19, "discount": 42, "link": "https://onelink.shein.com/38/5shtc1gxxmda", "sales": "600+"},
    {"name": "أظافر صناعية فرنسية - 24 قطعة", "price": 1.35, "discount": 41, "link": "https://onelink.shein.com/38/5sht8yz7kfv1", "sales": "200+"},
    {"name": "تيشيرت مدرسي أبيض للبنات - بقوس وردي", "price": 4.09, "discount": 47, "link": "https://onelink.shein.com/38/5sht8r3347y5", "sales": "800+"},
    {"name": "حامل هاتف قابل للطي - محمول", "price": 1.30, "discount": 24, "link": "https://onelink.shein.com/38/5sht5cr65itw", "sales": "100+"},
    {"name": "طقم مناشف مخططة - سريعة الجفاف", "price": 2.34, "discount": 38, "link": "https://onelink.shein.com/38/5sht12urdy18", "sales": "200+"},
    {"name": "شريط مانع لتسرب المياه - للحمام", "price": 1.70, "discount": 0, "link": "https://onelink.shein.com/38/5sht0h5f61jc", "sales": "300+"},
    {"name": "مقص دجاج متعدد الاستخدامات - مطبخ", "price": 2.70, "discount": 23, "link": "https://onelink.shein.com/38/5shszze54ug2", "sales": "300+"},
    {"name": "طقم قميص وبنطلون رجالي - 2 قطعة", "price": 7.77, "discount": 70, "link": "https://onelink.shein.com/38/5shsz9qqou3d", "sales": "50+"},
    {"name": "طقم موس حاجب - 30 قطعة", "price": 0.75, "discount": 32, "link": "https://onelink.shein.com/38/5shsyi4b2nub", "sales": "500+"},
    {"name": "فرجار رقمي - 6 بوصة", "price": 1.71, "discount": 10, "link": "https://onelink.shein.com/38/5shsxydzzinl", "sales": "200+"},
    {"name": "حزام رجالي بإبزيم أوتوماتيكي", "price": 2.93, "discount": 38, "link": "https://onelink.shein.com/38/5shsxapmkr2h", "sales": "500+"},
    {"name": "شفاطات لامعة قابلة لإعادة الاستخدام - 12 قطعة", "price": 0.99, "discount": 18, "link": "https://onelink.shein.com/38/5shswb72kgum", "sales": "600+"},
    {"name": "واقي شاشة هاتف - ضد التجسس", "price": 1.63, "discount": 49, "link": "https://onelink.shein.com/38/5shsw790bnla", "sales": "800+"},
    {"name": "مشط قابل للطي مع مرآة", "price": 1.90, "discount": 32, "link": "https://onelink.shein.com/38/5shsw1bwzhq8", "sales": "800+"},
    {"name": "لعبة ضغط بيضاوية مخططة", "price": 2.97, "discount": 10, "link": "https://onelink.shein.com/38/5shsvxdus31c", "sales": "200+"},
    {"name": "حزام كلب - مبطن وعاكس", "price": 3.30, "discount": 25, "link": "https://onelink.shein.com/38/5shsvrgrgmbu", "sales": "50+"},
    {"name": "غطاء حماية شاحن - 3 قطع", "price": 1.13, "discount": 25, "link": "https://onelink.shein.com/38/5shsvboiirzh", "sales": "900+"},
    {"name": "طقم فرش مكياج - 3 قطع", "price": 1.05, "discount": 48, "link": "https://onelink.shein.com/38/5shsv5rf6m2j", "sales": "1000+"},
    {"name": "فاتحة علب 4 في 1 - متعددة الاستخدام", "price": 1.08, "discount": 23, "link": "https://onelink.shein.com/38/5shsuk22y0h7", "sales": "200+"},
    {"name": "شارة أنمي BEASTARS - دبوس", "price": 1.65, "discount": 21, "link": "https://onelink.shein.com/38/5shstycqq3uz", "sales": "100+"},
    {"name": "رأس دش مطري - عالي الضغط", "price": 12.64, "discount": 65, "link": "https://onelink.shein.com/38/5shst4ra0l06", "sales": "200+"},
    {"name": "مكواة فرد وتجعيد شعر - سيراميك", "price": 26.90, "discount": 20, "link": "https://onelink.shein.com/38/5shsrzbmou3o", "sales": "100+"},
    {"name": "زجاجة رش زيت - للطبخ", "price": 1.17, "discount": 22, "link": "https://onelink.shein.com/38/5shsrvdkg0tg", "sales": "500+"},
    {"name": "مشابك تثبيت لحاف - 4 قطع", "price": 3.33, "discount": 5, "link": "https://onelink.shein.com/38/5shsrnhfz3p0", "sales": "200+"},
    {"name": "نظارات حجب الضوء الأزرق - 3 قطع", "price": 5.22, "discom": 50, "link": "https://onelink.shein.com/38/5shsqvv0f19e", "sales": "100+"},
    {"name": "أداة تقليم القدم - مبرد", "price": 1.10, "discount": 8, "link": "https://onelink.shein.com/38/5shspqfd1vtf", "sales": "300+"},
    {"name": "أساور خرز خشبي - 5/6/11/17 قطعة", "price": 1.80, "discount": 25, "link": "https://onelink.shein.com/38/5shsp8o323az", "sales": "100+"},
    {"name": "ورق زبدة للمقلاة الهوائية - 100 قطعة", "price": 1.26, "discount": 21, "link": "https://onelink.shein.com/38/5shsof2mdyzs", "sales": "300+"},
    {"name": "أظافر فرنسية للمانيكير - 48 قطعة", "price": 1.30, "discount": 35, "link": "https://onelink.shein.com/38/5shso76hvn95", "sales": "300+"},
    {"name": "سوار ساعة أبل - جلد أصلي", "price": 5.89, "discount": 5, "link": "https://onelink.shein.com/38/5shs5kbzkzl4", "sales": "100+"},
    {"name": "حمالة هاتف فراشة - مع كريستال", "price": 2.48, "discount": 25, "link": "https://onelink.shein.com/38/5shs5gdxezhw", "sales": "150+"},
]

# ========== توليد ملف HTML ==========
def generate_full_html():
    products_html = ""
    for p in SHEIN_PRODUCTS:
        final_price = p['price'] * (1 - p['discount']/100) if p['discount'] > 0 else p['price']
        sales_html = f'<div class="sales">🛍️ {p.get("sales", "50+")} تم البيع</div>' if p.get('sales') else ''
        discount_html = f'<span class="discount">-{p["discount"]}%</span>' if p['discount'] > 0 else ''
        old_price_html = f'<span class="old-price">${p["price"]:.2f}</span>' if p['discount'] > 0 else ''
        
        products_html += f'''
        <div class="product-card" onclick="window.open('{p['link']}', '_blank')">
            <div class="product-image">🛍️</div>
            <div class="product-info">
                <h3>{p['name']}</h3>
                <div class="price">
                    ${final_price:.2f}
                    {old_price_html}
                    {discount_html}
                </div>
                {sales_html}
                <button class="buy-btn">🛒 تسوق الآن</button>
            </div>
        </div>
        '''
    
    html = f'''<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>متجر سعيد | منتجات SHEIN</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Cairo', 'Tajawal', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{ max-width: 1300px; margin: 0 auto; }}
        .header {{ text-align: center; color: white; margin-bottom: 30px; }}
        .header h1 {{ font-size: 42px; margin-bottom: 10px; }}
        .coupon-box {{
            background: linear-gradient(90deg, #ff6b6b, #feca57);
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            margin-bottom: 30px;
            cursor: pointer;
        }}
        .coupon-code {{
            background: white;
            display: inline-block;
            padding: 12px 35px;
            border-radius: 50px;
            font-size: 28px;
            font-weight: bold;
            color: #ff6b6b;
            margin: 10px 0;
        }}
        .products-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; }}
        .product-card {{
            background: white;
            border-radius: 20px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        .product-card:hover {{ transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.2); }}
        .product-image {{
            height: 150px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 64px;
        }}
        .product-info {{ padding: 20px; }}
        .product-info h3 {{ font-size: 15px; margin-bottom: 10px; color: #333; }}
        .price {{ font-size: 22px; color: #ff4757; font-weight: bold; margin: 10px 0; }}
        .old-price {{ text-decoration: line-through; color: #999; font-size: 14px; margin-right: 8px; }}
        .discount {{ background: #ff4757; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; margin-right: 8px; }}
        .sales {{ color: #28a745; font-size: 12px; margin: 5px 0; }}
        .buy-btn {{
            background: linear-gradient(90deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 10px;
            width: 100%;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }}
        .footer {{ text-align: center; color: white; margin-top: 40px; padding: 20px; }}
        @media (max-width: 768px) {{
            .products-grid {{ grid-template-columns: 1fr; }}
            .coupon-code {{ font-size: 18px; padding: 8px 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛍️ سوق سعيد | تشكيلة SHEIN</h1>
            <p>أحدث الصيحات بأفضل الأسعار - توصيل سريع</p>
        </div>
        
        <div class="coupon-box" onclick="copyCoupon()">
            <div>🎁 عرض خاص للمستخدمين الجدد 🎁</div>
            <div class="coupon-code">🏷️ كود الخصم: WL7KA 🏷️</div>
            <div>🔥 خصم يصل إلى 60% على أول طلب - اضغط لنسخ الكود</div>
        </div>
        
        <div class="products-grid">
            {products_html}
        </div>
        
        <div class="footer">
            <p>© 2026 سوق سعيد - تسوق واستمتع بأفضل العروض</p>
            <p>كود الخصم: WL7KA | خصم 60% للمستخدمين الجدد</p>
        </div>
    </div>
    
    <script>
        function copyCoupon() {{
            navigator.clipboard.writeText('WL7KA');
            alert('✅ تم نسخ كود الخصم: WL7KA\\n\\nاستخدمه عند الدفع للحصول على خصم 60%');
        }}
    </script>
</body>
</html>
    '''
    
    return html

# ========== حفظ الملف ==========
def save_and_open():
    html_content = generate_full_html()
    
    with open('shein_store.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("=" * 55)
    print("✅ تم إنشاء ملف shein_store.html بنجاح!")
    print(f"📂 المسار: {os.path.abspath('shein_store.html')}")
    print(f"📊 عدد المنتجات: {len(SHEIN_PRODUCTS)} منتج")
    print("📁 يمكنك فتح الملف من مدير الملفات في هاتفك")
    print("🌐 أو فتحه في المتصفح لمشاهدة المتجر العربي")
    print("=" * 55)

# ========== تشغيل الملف ==========
if __name__ == "__main__":
    save_and_open()

import json
import re
from typing import List, Dict

# قائمة منتجات SHEIN (أضفت أول 10 منتجات كمثال، يمكنك إضافة الباقي)
SHEIN_PRODUCTS = [
    {
        "name": "SHEIN Playful Pals Young Girl Hooded Padded Coat",
        "price": 19.39,
        "discount": 43,
        "link": "https://onelink.shein.com/38/5shrzfcizjmg",
        "coupon": "WL7KA"
    },
    {
        "name": "Elegant Design Sense Mature Hong Kong Style Shirt",
        "price": 14.18,
        "discount": 37,
        "link": "https://onelink.shein.com/38/5shune7n90yf",
        "coupon": "WL7KA"
    },
    {
        "name": "6pcs K-POP Idol Printed Party Glasses",
        "price": 2.70,
        "discount": 0,
        "link": "https://onelink.shein.com/38/5shujg5f2ywk",
        "coupon": "WL7KA",
        "sales": "300+"
    },
    {
        "name": "Multicolor Waterproof Travel Toiletry Bag",
        "price": 3.90,
        "discount": 17,
        "link": "https://onelink.shein.com/38/5shuimjyfjt7",
        "coupon": "WL7KA",
        "sales": "100+"
    },
    {
        "name": "Manfinity Men Solid Color Casual Overcoat",
        "price": 25.67,
        "discount": 24,
        "link": "https://onelink.shein.com/38/5shui8qqn60h",
        "coupon": "WL7KA"
    },
    {
        "name": "Exaggerated Floral Ball Earrings",
        "price": 1.44,
        "discount": 4,
        "link": "https://onelink.shein.com/38/5shtox57cemc",
        "coupon": "WL7KA",
        "sales": "300+"
    },
    {
        "name": "5pcs Candy Color Scrunchies",
        "price": 1.50,
        "discount": 38,
        "link": "https://onelink.shein.com/38/5shtobfv3sxn",
        "coupon": "WL7KA",
        "sales": "800+"
    },
    {
        "name": "Women's Casual Sports Shoes",
        "price": 5.00,
        "discount": 82,
        "link": "https://onelink.shein.com/38/5shtl502kmcf",
        "coupon": "WL7KA",
        "sales": "200+"
    },
    {
        "name": "Pink Rose Flower Adjustable Rings Set",
        "price": 2.16,
        "discount": 6,
        "link": "https://onelink.shein.com/38/5shtkl9rhh8f",
        "coupon": "WL7KA",
        "sales": "500+"
    },
    {
        "name": "Rice Bucket With Measuring Cup",
        "price": 8.84,
        "discount": 70,
        "link": "https://onelink.shein.com/38/5shtjtnbwphj",
        "coupon": "WL7KA",
        "sales": "200+"
    }
]

def generate_product_card(product: Dict) -> str:
    """توليد بطاقة منتج HTML واحدة"""
    final_price = product['price'] * (1 - product['discount']/100) if product['discount'] > 0 else product['price']
    sales_text = f'<div class="sales">🛍️ {product.get("sales", "50+")} تم البيع</div>' if product.get("sales") else ''
    
    return f'''
    <div class="product-card" onclick="window.open('{product['link']}', '_blank')">
        <div class="product-image">📦</div>
        <div class="product-info">
            <h3>{product['name'][:50]}</h3>
            <div class="price">
                ${final_price:.2f}
                {f'<span class="old-price">${product["price"]:.2f}</span>' if product["discount"] > 0 else ''}
                {f'<span class="discount-badge">-{product["discount"]}%</span>' if product["discount"] > 0 else ''}
            </div>
            {sales_text}
            <button class="buy-btn">🛒 تسوق الآن</button>
        </div>
    </div>
    '''

def generate_full_html() -> str:
    """توليد صفحة HTML كاملة"""
    products_html = ''.join([generate_product_card(p) for p in SHEIN_PRODUCTS])
    
    return f'''<!DOCTYPE html>
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
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        .header h1 {{ font-size: 42px; margin-bottom: 10px; }}
        
        .coupon-box {{
            background: linear-gradient(90deg, #ff6b6b, #feca57);
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            margin-bottom: 30px;
            cursor: pointer;
            transition: transform 0.3s;
        }}
        .coupon-box:hover {{ transform: scale(1.02); }}
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
        
        .products-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
        }}
        
        .product-card {{
            background: white;
            border-radius: 20px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        .product-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }}
        .product-image {{
            height: 200px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 64px;
        }}
        .product-info {{ padding: 20px; }}
        .product-info h3 {{ font-size: 16px; margin-bottom: 10px; color: #333; }}
        .price {{ font-size: 24px; color: #ff4757; font-weight: bold; margin: 10px 0; }}
        .old-price {{ text-decoration: line-through; color: #999; font-size: 14px; margin-right: 8px; }}
        .discount-badge {{ background: #ff4757; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; margin-right: 8px; }}
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛍️ Saeed Market | SHEIN Collection</h1>
            <p>أحدث الصيحات بأفضل الأسعار</p>
        </div>
        
        <div class="coupon-box" onclick="copyCoupon()">
            <div>🎁 عرض خاص للمستخدمين الجدد 🎁</div>
            <div class="coupon-code">🏷️ كود الخصم: WL7KA 🏷️</div>
            <div>خصم يصل إلى 60% على أول طلب - اضغط لنسخ الكود</div>
        </div>
        
        <div class="products-grid">
            {products_html}
        </div>
        
        <div class="footer">
            <p>© 2026 Saeed Market - تسوق واستمتع بأفضل العروض</p>
        </div>
    </div>
    
    <script>
        function copyCoupon() {{
            navigator.clipboard.writeText('WL7KA');
            alert('✅ تم نسخ كود الخصم: WL7KA\\nاستخدمه عند الدفع للحصول على خصم 60%');
        }}
    </script>
</body>
</html>
    '''

def save_and_open():
    """حفظ الملف وفتحه في المتصفح"""
    html_content = generate_full_html()
    
    with open('shein_store.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ تم إنشاء ملف shein_store.html بنجاح!")
    print("📂 يمكنك فتحه في المتصفح لمشاهدة المتجر")
    
    import os
    os.system('start shein_store.html' if os.name == 'nt' else 'open shein_store.html')

def add_more_products(products_text: str):
    """إضافة منتجات جديدة من النص الخام"""
    pattern = r'💰Price\[(\$?[\d\.]+)\].*?🛒(.*?)(?:\n|$)'
    matches = re.findall(pattern, products_text)
    
    for price, name in matches:
        SHEIN_PRODUCTS.append({
            "name": name.strip(),
            "price": float(price.replace('$', '')),
            "discount": 0,
            "link": "#",
            "coupon": "WL7KA"
        })
    
    print(f"✅ تم إضافة {len(matches)} منتج جديد")

if __name__ == "__main__":
    save_and_open()

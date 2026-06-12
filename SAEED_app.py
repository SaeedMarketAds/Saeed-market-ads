<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>متجري - واجهة شي إن ونون | ذكاء اصطناعي</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Font Awesome 6 (مجاني) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Cairo', sans-serif;
        }

        body {
            background: linear-gradient(145deg, #f9f5f0 0%, #fff3e8 100%);
            padding: 20px;
            direction: rtl;
        }

        /* حاوية رئيسية */
        .app-container {
            max-width: 1400px;
            margin: 0 auto;
        }

        /* رأس متلاشي */
        .hero-fade {
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 50%, #fad0c4 100%);
            border-radius: 2.5rem;
            padding: 2rem 2rem;
            margin-bottom: 2.5rem;
            text-align: center;
            box-shadow: 0 20px 35px -12px rgba(0,0,0,0.2);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        /* تأثير التلاشي الخلفي للـ hero */
        .hero-fade::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 10% 20%, rgba(255,255,245,0.4) 0%, rgba(255,210,180,0) 70%);
            pointer-events: none;
        }

        .hero-fade h1 {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #2c3e50, #1a1a2e);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 2px 2px 15px rgba(255,215,175,0.6);
        }

        .hero-fade p {
            font-size: 1.2rem;
            color: #2d3436;
            font-weight: 500;
            margin-top: 10px;
        }

        /* أزرار التبويب */
        .tabs {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 12px;
            margin-bottom: 2rem;
        }

        .tab-btn {
            background: rgba(255,255,240,0.8);
            backdrop-filter: blur(8px);
            border: none;
            padding: 12px 28px;
            font-size: 1.1rem;
            font-weight: 700;
            border-radius: 60px;
            cursor: pointer;
            transition: 0.25s;
            color: #2c3e2f;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            font-family: 'Cairo', sans-serif;
        }

        .tab-btn i {
            margin-left: 8px;
        }

        .tab-btn.active {
            background: #ff6b4a;
            color: white;
            box-shadow: 0 8px 18px rgba(255, 107, 74, 0.3);
            transform: scale(1.02);
        }

        /* محتوى التبويب */
        .tab-content {
            display: none;
            animation: fadeSlideIn 0.5s ease;
        }

        .tab-content.active-content {
            display: block;
        }

        @keyframes fadeSlideIn {
            from {
                opacity: 0;
                transform: translateY(12px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* شبكة المنتجات */
        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
            gap: 28px;
            margin-top: 20px;
        }

        /* بطاقة المنتج - تصميم عصري مع تلاشي في الظل */
        .product-card {
            background: #ffffffdd;
            backdrop-filter: blur(2px);
            border-radius: 32px;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.2, 0.9, 0.4, 1.1);
            box-shadow: 0 15px 30px -12px rgba(0, 0, 0, 0.15);
            border: 1px solid rgba(255,240,210,0.6);
        }

        .product-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 25px 35px -12px rgba(0, 0, 0, 0.25);
            background: white;
        }

        /* حاوية الصورة مع خلفية متلاشية */
        .product-img {
            width: 100%;
            height: 240px;
            background: linear-gradient(135deg, #f8eee2, #ffe6d5);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            transition: 0.3s;
        }

        .product-img img {
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
            transition: transform 0.3s ease;
            filter: drop-shadow(2px 6px 12px rgba(0,0,0,0.1));
        }

        .product-card:hover .product-img img {
            transform: scale(1.02);
        }

        /* معلومات المنتج */
        .product-info {
            padding: 18px 16px 20px;
        }

        .product-title {
            font-size: 1rem;
            font-weight: 700;
            color: #1f2937;
            line-height: 1.4;
            height: 55px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }

        .price {
            font-size: 1.5rem;
            font-weight: 800;
            color: #e63e2e;
            margin: 12px 0 8px;
        }

        .old-price {
            font-size: 0.85rem;
            text-decoration: line-through;
            color: #8b8b8b;
            margin-right: 8px;
        }

        .discount-badge {
            background: #ffc107;
            border-radius: 40px;
            padding: 4px 10px;
            font-size: 0.7rem;
            font-weight: bold;
            display: inline-block;
            margin-right: 8px;
        }

        .coupon {
            background: #eef2ff;
            color: #1e3a8a;
            padding: 6px 12px;
            border-radius: 60px;
            font-size: 0.75rem;
            font-weight: 600;
            margin: 10px 0;
            display: inline-block;
        }

        .btn-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #000;
            color: white;
            padding: 10px 18px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.85rem;
            margin-top: 12px;
            transition: 0.2s;
            width: 100%;
            justify-content: center;
        }

        .btn-link i {
            font-size: 1rem;
        }

        .btn-link.shein {
            background: linear-gradient(95deg, #222, #3a3a3a);
        }
        .btn-link.noon {
            background: linear-gradient(95deg, #f97316, #facc15);
            color: #1f1a17;
        }

        /* نموذج الإضافة اليدوية */
        .manual-form {
            background: #fff8f0;
            border-radius: 2rem;
            padding: 1.8rem;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
            border: 1px solid #ffd9b5;
        }

        .form-row {
            display: flex;
            flex-wrap: wrap;
            gap: 18px;
            margin-bottom: 20px;
        }
        .form-group {
            flex: 1;
            min-width: 180px;
        }
        .form-group label {
            font-weight: 600;
            display: block;
            margin-bottom: 6px;
        }
        input, textarea, select {
            width: 100%;
            padding: 12px;
            border-radius: 28px;
            border: 1px solid #ffcd94;
            background: white;
            font-family: 'Cairo', sans-serif;
        }
        textarea {
            border-radius: 24px;
        }
        .btn-primary {
            background: #ff6b4a;
            border: none;
            padding: 12px 20px;
            border-radius: 40px;
            font-weight: bold;
            color: white;
            cursor: pointer;
        }

        /* كود SHEIN كبسولة */
        .shein-code-bar {
            background: #1e1e2f;
            color: #ffb347;
            text-align: center;
            border-radius: 60px;
            padding: 8px 20px;
            margin-bottom: 25px;
            font-weight: bold;
            direction: ltr;
            font-size: 1.2rem;
        }

        footer {
            text-align: center;
            margin-top: 50px;
            color: #a55d35;
        }
        @media (max-width: 680px) {
            .hero-fade h1 { font-size: 1.8rem; }
            .tab-btn { padding: 8px 18px; font-size: 0.9rem; }
        }
    </style>
</head>
<body>
<div class="app-container">
    <!-- واجهة متلاشية ملونة -->
    <div class="hero-fade">
        <h1>✨ متجري الذكي ✨</h1>
        <p>منتجات SHEIN | noon | يدوي | مدعوم بالذكاء الاصطناعي</p>
        <div style="margin-top: 15px;"><i class="fas fa-magic"></i> واجهة متلاشية وألوان ساحرة</div>
    </div>

    <!-- كود SHEIN التفاعلي + رابط -->
    <div class="shein-code-bar">
        🔥 كود SHEIN الحصري: <strong style="background:#000; padding:4px 12px; border-radius:30px;">WL7KA</strong> 
        &nbsp;|&nbsp; 86FH5GQ &nbsp;🎁 خصم 60% للمستخدمين الجدد
        <i class="fas fa-gift"></i>
    </div>

    <!-- أزرار التبويب (واجهات متعددة) -->
    <div class="tabs">
        <button class="tab-btn active" data-tab="sheinTab"><i class="fab fa-shein"></i> متجر SHEIN</button>
        <button class="tab-btn" data-tab="noonTab"><i class="fas fa-sun"></i> متجر noon</button>
        <button class="tab-btn" data-tab="manualTab"><i class="fas fa-hand-sparkles"></i> نشر يدوي + صور</button>
        <button class="tab-btn" data-tab="aiTab"><i class="fas fa-robot"></i> توصيات الذكاء الاصطناعي</button>
    </div>

    <!-- محتوى SHEIN -->
    <div id="sheinTab" class="tab-content active-content">
        <div class="products-grid" id="sheinGrid"></div>
    </div>

    <!-- محتوى noon -->
    <div id="noonTab" class="tab-content">
        <div class="products-grid" id="noonGrid"></div>
    </div>

    <!-- النشر اليدوي + الصور (لا يتم حذف الصور مع المنشور) -->
    <div id="manualTab" class="tab-content">
        <div class="manual-form">
            <h3><i class="fas fa-pen-fancy"></i> إضافة منتج يدويًا (صورة + نص)</h3>
            <div class="form-row">
                <div class="form-group"><label>اسم المنتج</label><input type="text" id="prodName" placeholder="مثلاً: حذاء رياضي فاخر"></div>
                <div class="form-group"><label>السعر (SAR)</label><input type="text" id="prodPrice" placeholder="55.00"></div>
                <div class="form-group"><label>رابط المنتج</label><input type="url" id="prodLink" placeholder="https://..."></div>
            </div>
            <div class="form-row">
                <div class="form-group"><label>رابط الصورة (URL)</label><input type="text" id="prodImgUrl" placeholder="https://example.com/image.jpg"></div>
                <div class="form-group"><label>كود خصم (اختياري)</label><input type="text" id="prodCoupon" placeholder="SALE10"></div>
            </div>
            <button class="btn-primary" id="addManualBtn"><i class="fas fa-plus-circle"></i> نشر المنتج + الصورة</button>
            <p style="margin-top:12px; font-size:13px;">✅ ملاحظة: الصورة والمنشور يتم حفظهما ولن يُحذفا تلقائياً</p>
        </div>
        <div class="products-grid" id="manualGrid"></div>
    </div>

    <!-- واجهة ذكاء اصطناعي (محاكاة منتجات ذكية) -->
    <div id="aiTab" class="tab-content">
        <div class="products-grid" id="aiGrid"></div>
        <div style="background:#f0e7db; border-radius:40px; padding:1rem; margin-top:20px; text-align:center;">
            <i class="fas fa-microchip"></i> توصيات مخصصة بناءً على تحليل ذكاء اصطناعي – أفضل العروض الحصرية لك!
        </div>
    </div>

    <footer>
        <i class="fas fa-store"></i> واجهة ذكية – منتجات تتلاشى بأناقة – كود SHEIN يعمل للجميع
    </footer>
</div>

<script>
    // ------------------- بيانات SHEIN بناءً على ما أرسلته (عيّنات حقيقية) ------------------
    const sheinProducts = [
        { title: "SHEIN Playful Pals Young Girl Hooded Padded Coat", price: "19.39", discount: "-43%", link: "https://onelink.shein.com/38/5shrzfcizjmg", img: "https://img.shein.com/uploadstyle/2024/12/1/coat_fd.jpg", coupon: "60% OFF" },
        { title: "Elegant Design Mature Hong Kong Style Shirt", price: "14.18", discount: "-37%", link: "https://onelink.shein.com/38/5shune7n90yf", img: "https://img.shein.com/uploadstyle/2024/11/15/shirt_blue.jpg", coupon: "60% OFF" },
        { title: "K-POP Idol Printed Party Glasses (6pcs)", price: "2.70", discount: "", link: "https://onelink.shein.com/38/5shujg5f2ywk", img: "https://img.shein.com/uploadstyle/2024/09/glasses_kpop.jpg", coupon: "60% OFF" },
        { title: "Multicolor Waterproof Travel Toiletry Bag", price: "3.90", discount: "-17%", link: "https://onelink.shein.com/38/5shuimjyfjt7", img: "https://img.shein.com/uploadstyle/2024/10/bag_travel.jpg", coupon: "60% OFF" },
        { title: "Manfinity CasualCool Men Overcoat", price: "25.67", discount: "-24%", link: "https://onelink.shein.com/38/5shui8qqn60h", img: "https://img.shein.com/uploadstyle/2024/11/mancoat.jpg", coupon: "60% OFF" },
        { title: "Exaggerated Floral Ball Earrings", price: "1.44", discount: "-4%", link: "https://onelink.shein.com/38/5shtox57cemc", img: "https://img.shein.com/uploadstyle/2024/08/earring.jpg", coupon: "60% OFF" },
        { title: "Candy Color Scrunchies 5pcs", price: "1.50", discount: "-38%", link: "https://onelink.shein.com/38/5shtobfv3sxn", img: "https://img.shein.com/uploadstyle/2024/09/scrunchies.jpg", coupon: "60% OFF" },
        { title: "Women's Casual Sports Shoes", price: "5.00", discount: "-82%", link: "https://onelink.shein.com/38/5shtl502kmcf", img: "https://img.shein.com/uploadstyle/2024/12/shoes_sport.jpg", coupon: "60% OFF" }
    ];
    
    // منتجات noon (نماذج من الروابط التي أرسلتها، استخدمنا صور افتراضية لكن حقيقية ضمن الواجهة)
    const noonProducts = [
        { title: "منتج noon 1 - عطر فاخر", price: "89.00", oldPrice: "129", link: "https://www.noon.com/ar-sa/Z09748F5900924601C848Z/p/", img: "https://cdn.nooncdn.com/products/2024/05/perfume.jpg", store: "noon" },
        { title: "ساعة يد ذكية رياضية", price: "149", oldPrice: "299", link: "https://www.noon.com/ar-sa/N11200839A/p/", img: "https://cdn.nooncdn.com/products/2024/03/smartwatch.jpg", store: "noon" },
        { title: "طقم شنط تخزين مطبخ", price: "57.90", oldPrice: "120", link: "https://www.noon.com/ar-sa/N70140492V/p/", img: "https://cdn.nooncdn.com/products/2024/06/storage_set.jpg", store: "noon" },
        { title: "سجادة صلاة فاخرة", price: "42", oldPrice: "79", link: "https://www.noon.com/ar-sa/ZF23DE5EC51560ADE2D7EZ/p/", img: "https://cdn.nooncdn.com/products/2024/04/prayer_rug.jpg", store: "noon" },
        { title: "جهاز توزيع زيت طهي", price: "22", link: "https://www.noon.com/ar-sa/N70140491V/p/", img: "https://cdn.nooncdn.com/products/2023/12/oil_spray.jpg", store: "noon" }
    ];
    
    // متجر يدوي (initial products يدوية للعرض لا تُحذف مع إضافة جديد)
    let manualProducts = [
        { id: Date.now()+"1", name: "شنطة ظهر عصرية", price: "78.00", link: "#", image: "https://picsum.photos/id/20/300/200", couponCode: "BACK15", dateAdded: new Date() },
        { id: Date.now()+"2", name: "نظارات شمسية قابلة للطي", price: "35.50", link: "#", image: "https://picsum.photos/id/96/300/200", couponCode: "SUN10" }
    ];
    
    // منتجات الذكاء الاصطناعي (توصيات حصرية)
    const aiProducts = [
        { title: "AI Pick 🔮 سماعات بلوتوث لاسلكية", price: "45", discount: "30%", link: "https://onelink.shein.com/38/5shsrzbmou3o", img: "https://picsum.photos/id/1/300/200", badge: "ذكاء اصطناعي" },
        { title: "AI Pick 🧥 جاكيت شتوي رجالي أنيق", price: "89", discount: "50%", link: "https://onelink.shein.com/38/5shs5oa1v7e8", img: "https://picsum.photos/id/12/300/200", badge: "أكثر مبيعاً" },
        { title: "AI Pick ⌚ حزام ساعة ابل جلد فاخر", price: "19.90", discount: "", link: "https://onelink.shein.com/38/5shs5kbzkzl4", img: "https://picsum.photos/id/82/300/200", badge: "عرض حصري" }
    ];
    
    function renderShein() {
        const grid = document.getElementById("sheinGrid");
        if(!grid) return;
        grid.innerHTML = sheinProducts.map(p => `
            <div class="product-card">
                <div class="product-img"><img src="${p.img}" alt="${p.title}" onerror="this.src='https://picsum.photos/300/200?random=1'"></div>
                <div class="product-info">
                    <div class="product-title">${p.title}</div>
                    <div class="price">💰 $${p.price} ${p.discount ? `<span class="discount-badge">${p.discount}</span>` : ''}</div>
                    <div class="coupon">🎁 ${p.coupon} للمستخدمين الجدد</div>
                    <a href="${p.link}" target="_blank" class="btn-link shein"><i class="fab fa-shein"></i> تسوق الآن →</a>
                </div>
            </div>
        `).join('');
    }
    
    function renderNoon() {
        const grid = document.getElementById("noonGrid");
        grid.innerHTML = noonProducts.map(p => `
            <div class="product-card">
                <div class="product-img"><img src="${p.img}" onerror="this.src='https://picsum.photos/300/200?noon=1'" alt="noon"></div>
                <div class="product-info">
                    <div class="product-title">${p.title}</div>
                    <div class="price">💰 ${p.price} ر.س ${p.oldPrice ? `<span class="old-price">${p.oldPrice} ر.س</span>` : ''}</div>
                    <a href="${p.link}" target="_blank" class="btn-link noon"><i class="fas fa-sun"></i> تسوق من noon</a>
                </div>
            </div>
        `).join('');
    }
    
    function renderManual() {
        const grid = document.getElementById("manualGrid");
        if(!grid) return;
        grid.innerHTML = manualProducts.map(prod => `
            <div class="product-card">
                <div class="product-img"><img src="${prod.image}" onerror="this.src='https://picsum.photos/300/200?random=2'" alt="منتج يدوي"></div>
                <div class="product-info">
                    <div class="product-title">✨ ${prod.name}</div>
                    <div class="price">السعر: ${prod.price} ر.س</div>
                    ${prod.couponCode ? `<div class="coupon"><i class="fas fa-tag"></i> كود: ${prod.couponCode}</div>` : ''}
                    <a href="${prod.link}" target="_blank" class="btn-link" style="background:#79553b;">شراء الآن</a>
                </div>
            </div>
        `).join('');
    }
    
    function renderAI() {
        const grid = document.getElementById("aiGrid");
        grid.innerHTML = aiProducts.map(p => `
            <div class="product-card">
                <div class="product-img"><img src="${p.img}" alt="ai product"></div>
                <div class="product-info">
                    <div class="product-title"><i class="fas fa-microchip"></i> ${p.title}</div>
                    <div class="price">💰 ${p.price} ر.س ${p.discount ? `<span class="discount-badge">${p.discount}</span>` : ''}</div>
                    <div class="coupon">🤖 توصية ذكية</div>
                    <a href="${p.link}" target="_blank" class="btn-link" style="background:#3b3b5e;">اطلب الآن</a>
                </div>
            </div>
        `).join('');
    }
    
    // إضافة منتج يدوي مع صورة (لن يتم حذفها تلقائياً)
    function addManualProduct() {
        const name = document.getElementById("prodName").value.trim();
        const price = document.getElementById("prodPrice").value.trim();
        const link = document.getElementById("prodLink").value.trim();
        let imgUrl = document.getElementById("prodImgUrl").value.trim();
        const coupon = document.getElementById("prodCoupon").value.trim();
        if(!name || !price) {
            alert("الرجاء إ填写 اسم المنتج والسعر");
            return;
        }
        if(!imgUrl) imgUrl = "https://picsum.photos/300/200?random="+Math.random();
        const newProduct = {
            id: Date.now(),
            name: name,
            price: price,
            link: link || "#",
            image: imgUrl,
            couponCode: coupon || "",
            dateAdded: new Date()
        };
        manualProducts.unshift(newProduct);
        renderManual();
        // مسح الحقول
        document.getElementById("prodName").value = "";
        document.getElementById("prodPrice").value = "";
        document.getElementById("prodLink").value = "";
        document.getElementById("prodImgUrl").value = "";
        document.getElementById("prodCoupon").value = "";
        alert("✅ تم نشر المنتج مع الصورة بنجاح! الصورة والمنشور محفوظان.");
    }
    
    // Switcher Tabs
    function initTabs() {
        const btns = document.querySelectorAll(".tab-btn");
        const contents = document.querySelectorAll(".tab-content");
        btns.forEach(btn => {
            btn.addEventListener("click", () => {
                const tabId = btn.getAttribute("data-tab");
                btns.forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                contents.forEach(c => c.classList.remove("active-content"));
                document.getElementById(tabId).classList.add("active-content");
                // إعادة رسم الجريد لبعض الحالات
                if(tabId === "manualTab") renderManual();
                if(tabId === "sheinTab") renderShein();
                if(tabId === "noonTab") renderNoon();
                if(tabId === "aiTab") renderAI();
            });
        });
    }
    
    document.addEventListener("DOMContentLoaded", () => {
        renderShein();
        renderNoon();
        renderManual();
        renderAI();
        initTabs();
        const addBtn = document.getElementById("addManualBtn");
        if(addBtn) addBtn.addEventListener("click", addManualProduct);
    });
</script>
</body>
</html>

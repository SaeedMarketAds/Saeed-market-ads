class SaeedMarket:
    def __init__(self):
        self.markets = {
            "aliexpress": "AliExpress - عروض حصرية",
            "noon": "Noon - توصيل سريع",
            "shein": "Shein - أزياء عصرية",
            "yemen": "السوق اليمني - قادم قريباً"
        }
    
    def get_products(self, market_name):
        """جلب منتجات من سوق معين"""
        products = {
            "aliexpress": "🔍 منتجات AliExpress: هواتف، ساعات، سماعات",
            "noon": "🛍️ منتجات Noon: لابتوبات، إلكترونيات، ألعاب",
            "shein": "👗 منتجات Shein: فساتين، حقائب، أحذية",
            "yemen": "🇾🇪 منتجات يمنية: عسل، فضة، بخور"
        }
        return products.get(market_name, "مرحباً بك في السوق")

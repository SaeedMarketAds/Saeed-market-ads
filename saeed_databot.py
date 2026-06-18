import json
import random

class SaeedDataBot:
    def __init__(self, config_path="saeed_databot_config.json"):
        # تحميل الإعدادات
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except:
            self.config = {
                "bot_name": "Saeed DataBot",
                "owner": "Saeed Almasoori"
            }
        
        # ردود افتراضية
        self.responses = {
            "مرحبا": ["وعليكم السلام ورحمة الله", "أهلاً بك!", "مرحباً! كيف أخدمك؟"],
            "السلام عليكم": ["وعليكم السلام ورحمة الله وبركاته", "وعليكم السلام"],
            "كيف الحال": ["بخير والحمد لله، وأنت؟", "تمام، شكراً لسؤالك!"],
            "سعر": ["دعني أبحث لك عن أفضل الأسعار...", "جاري جلب العروض..."],
            "شكرا": ["عفواً، في خدمتك!", "الشكر لله، تحت أمرك!"],
            "وداعا": ["مع السلامة، ننتظر عودتك!", "في أمان الله!"]
        }
    
    def get_response(self, user_input):
        """الحصول على رد مناسب من البوت"""
        user_input = user_input.strip()
        
        # البحث عن رد مطابق
        for key, replies in self.responses.items():
            if key in user_input:
                return random.choice(replies)
        
        # رد افتراضي
        defaults = [
            "أنا Saeed DataBot، كيف يمكنني مساعدتك في التسوق؟",
            "هل تبحث عن منتج معين؟ أخبرني وسأبحث لك!",
            "يمكنني مساعدتك في مقارنة الأسعار والعروض.",
            f"مرحباً! أنا {self.config.get('bot_name', 'Saeed DataBot')}، صنع بواسطة {self.config.get('owner', 'Saeed Almasoori')}."
        ]
        return random.choice(defaults)
    
    def get_greeting(self):
        """رسالة ترحيبية"""
        return "السلام عليكم ورحمة الله وبركاته، كيف أخدمك اليوم؟"

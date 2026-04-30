import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pages.models import ContentPage

def create_default_pages():
    pages = [
        {
            'title_en': 'Privacy Policy',
            'title_ar': 'سياسة الخصوصية',
            'slug': 'privacy',
            'body_en': """Privacy Policy

At Cosmos Commerce, we are committed to protecting your privacy and ensuring the security of your personal information. This Privacy Policy outlines how we collect, use, and protect the data you provide to us.

1. Information We Collect
We collect information that you provide directly to us when you create an account, make a purchase, or communicate with us. This includes your name, email address, shipping address, and payment information.

2. How We Use Your Information
We use the information we collect to process your orders, provide customer support, and send you updates about our products and services. We do not sell or share your personal information with third parties for marketing purposes.

3. Data Security
We implement a variety of security measures to maintain the safety of your personal information. Your sensitive data is encrypted and stored securely.

4. Your Rights
You have the right to access, correct, or delete your personal information at any time. Please contact us if you have any questions regarding your data.""",
            'body_ar': """سياسة الخصوصية

في كوزموس كوميرس، نحن ملتزمون بحماية خصوصيتك وضمان أمن معلوماتك الشخصية. توضح سياسة الخصوصية هذه كيفية جمع واستخدام وحماية البيانات التي تزودنا بها.

1. المعلومات التي نجمعها
نجمع المعلومات التي تقدمها لنا مباشرة عند إنشاء حساب أو إجراء عملية شراء أو التواصل معنا. يتضمن ذلك اسمك وعنوان بريدك الإلكتروني وعنوان الشحن ومعلومات الدفع.

2. كيف نستخدم معلوماتك
نستخدم المعلومات التي نجمعها لمعالجة طلباتك وتقديم دعم العملاء وإرسال تحديثات حول منتجاتنا وخدماتنا. نحن لا نبيع أو نشارك معلوماتك الشخصية مع أطراف ثالثة لأغراض التسويق.

3. أمن البيانات
نحن ننفذ مجموعة متنوعة من الإجراءات الأمنية للحفاظ على سلامة معلوماتك الشخصية. يتم تشفير بياناتك الحساسة وتخزينها بشكل آمن.

4. حقوقك
لك الحق في الوصول إلى معلوماتك الشخصية أو تصحيحها أو حذفها في أي وقت. يرجى الاتصال بنا إذا كان لديك أي أسئلة بخصوص بياناتك.""",
        },
        {
            'title_en': 'Terms of Service',
            'title_ar': 'شروط الخدمة',
            'slug': 'terms',
            'body_en': """Terms of Service

Welcome to Cosmos Commerce. By accessing or using our website, you agree to comply with and be bound by the following terms and conditions.

1. Use of the Site
You may use our site for lawful purposes only. You must not use our site in any way that violates any applicable local, national, or international law or regulation.

2. Intellectual Property
All content on this site, including text, graphics, logos, and images, is the property of Cosmos Commerce and is protected by intellectual property laws.

3. Limitation of Liability
Cosmos Commerce shall not be liable for any direct, indirect, incidental, or consequential damages arising from the use of our site or the purchase of our products.""",
            'body_ar': """شروط الخدمة

مرحبًا بك في كوزموس كوميرس. من خلال الوصول إلى موقعنا الإلكتروني أو استخدامه، فإنك توافق على الالتزام بالشروط والأحكام التالية.

1. استخدام الموقع
يمكنك استخدام موقعنا للأغراض القانونية فقط. يجب عدم استخدام موقعنا بأي شكل من الأشكال التي تنتهك أي قانون أو لائحة محلية أو وطنية أو دولية معمول بها.

2. الملكية الفكرية
جميع المحتويات الموجودة على هذا الموقع، بما في ذلك النصوص والرسومات والشعارات والصور، هي ملك لشركة كوزموس كوميرس ومحمية بقوانين الملكية الفكرية.

3. تحديد المسؤولية
لن تكون كوزموس كوميرس مسؤولة عن أي أضرار مباشرة أو غير مباشرة أو عرضية أو تبعية تنشأ عن استخدام موقعنا أو شراء منتجاتنا.""",
        }
    ]

    for p in pages:
        obj, created = ContentPage.objects.update_or_create(slug=p['slug'], defaults=p)
        if created:
            print(f"Created page: {p['title_en']}")
        else:
            print(f"Updated page: {p['title_en']}")

if __name__ == "__main__":
    create_default_pages()

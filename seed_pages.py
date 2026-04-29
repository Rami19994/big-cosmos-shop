import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from pages.models import ContentPage

terms_body_en = """Welcome to Nova Commerce. These Terms of Service govern your use of our website and services.

1. General
By accessing and placing an order with Nova Commerce, you confirm that you are in agreement with and bound by the terms of service contained herein. These terms apply to the entire website and any email or other type of communication between you and Nova Commerce.

2. Products and Services
Nova Commerce is an e-commerce platform that connects buyers with high-quality products. We reserve the right to modify or discontinue any product at any given time without notice. Prices for our products are subject to change without notice.

3. Accounts and Registration
Regular customers can purchase products as guests without the need to create an account. However, sellers who wish to offer products on our platform must contact us directly to apply for a seller account. You are responsible for maintaining the security of your account and password.

4. Payments and Billing
All payments are processed securely. You agree to provide current, complete, and accurate purchase and account information for all purchases made at our store. We reserve the right to refuse any order you place with us.

5. Returns and Refunds
Please review our separate Returns Policy for detailed information on returns and refunds. We aim to ensure complete satisfaction with every purchase.

6. Limitation of Liability
Nova Commerce shall not be liable for any direct, indirect, incidental, consequential, or exemplary damages resulting from the use or inability to use the service.

7. Changes to Terms
We reserve the right, at our sole discretion, to update, change or replace any part of these Terms of Service by posting updates and changes to our website. It is your responsibility to check our website periodically for changes."""

terms_body_ar = """مرحباً بكم في نوفا كوميرس. تحكم شروط الخدمة هذه استخدامكم لموقعنا وخدماتنا.

1. عام
من خلال الوصول وتقديم طلب مع نوفا كوميرس، فإنك تؤكد أنك توافق وتلتزم بشروط الخدمة الواردة هنا. تنطبق هذه الشروط على الموقع بأكمله وأي بريد إلكتروني أو نوع آخر من الاتصالات بينك وبين نوفا كوميرس.

2. المنتجات والخدمات
نوفا كوميرس هي منصة للتجارة الإلكترونية تربط المشترين بالمنتجات عالية الجودة. نحتفظ بالحق في تعديل أو إيقاف أي منتج في أي وقت دون إشعار مسبق. أسعار منتجاتنا عرضة للتغيير دون إشعار.

3. الحسابات والتسجيل
يمكن للعملاء العاديين شراء المنتجات كضيوف دون الحاجة إلى إنشاء حساب. ومع ذلك، يجب على البائعين الذين يرغبون في عرض المنتجات على منصتنا الاتصال بنا مباشرة لطلب حساب بائع. أنت مسؤول عن الحفاظ على أمان حسابك وكلمة المرور.

4. المدفوعات والفوترة
تتم معالجة جميع المدفوعات بشكل آمن. أنت توافق على تقديم معلومات شراء وحساب حالية وكاملة ودقيقة لجميع عمليات الشراء التي تتم في متجرنا. نحتفظ بالحق في رفض أي طلب تقدمه لنا.

5. المرتجعات والمبالغ المستردة
يرجى مراجعة سياسة الإرجاع المنفصلة للحصول على معلومات مفصلة حول المرتجعات والمبالغ المستردة. نحن نهدف إلى ضمان الرضا التام عن كل عملية شراء.

6. تحديد المسؤولية
لن تكون نوفا كوميرس مسؤولة عن أي أضرار مباشرة أو غير مباشرة أو عرضية أو تبعية أو نموذجية ناتجة عن استخدام أو عدم القدرة على استخدام الخدمة.

7. التغييرات على الشروط
نحتفظ بالحق، وفقًا لتقديرنا الخاص، في تحديث أو تغيير أو استبدال أي جزء من شروط الخدمة هذه عن طريق نشر التحديثات والتغييرات على موقعنا. تقع على عاتقك مسؤولية مراجعة موقعنا بشكل دوري لمعرفة التغييرات."""

privacy_body_en = """At Nova Commerce, accessible from our website, one of our main priorities is the privacy of our visitors. This Privacy Policy document contains types of information that is collected and recorded by Nova Commerce and how we use it.

1. Information We Collect
We collect personal information that you provide to us when placing an order, such as your name, email address, phone number, shipping address, and payment information. We also collect data automatically when you navigate our site, such as your IP address, browser type, and device information.

2. How We Use Your Information
We use the information we collect to:
- Provide, operate, and maintain our website and services
- Process your orders, payments, and shipping
- Communicate with you, including for customer service and support
- Send you emails regarding your order or promotional offers (if you opted in)
- Find and prevent fraud

3. Log Files
Nova Commerce follows a standard procedure of using log files. These files log visitors when they visit websites. The information collected by log files include internet protocol (IP) addresses, browser type, Internet Service Provider (ISP), date and time stamp, referring/exit pages, and possibly the number of clicks.

4. Cookies and Web Beacons
Like any other website, Nova Commerce uses 'cookies'. These cookies are used to store information including visitors' preferences, and the pages on the website that the visitor accessed or visited. The information is used to optimize the users' experience by customizing our web page content based on visitors' browser type and/or other information.

5. Third-Party Policies
We do not sell, trade, or otherwise transfer your Personally Identifiable Information to outside parties. This does not include trusted third parties who assist us in operating our website, conducting our business, or servicing you, so long as those parties agree to keep this information confidential.

6. Contact Us
If you have additional questions or require more information about our Privacy Policy, do not hesitate to contact us."""

privacy_body_ar = """في نوفا كوميرس، واحدة من أولوياتنا الرئيسية هي خصوصية زوارنا. تحتوي وثيقة سياسة الخصوصية هذه على أنواع المعلومات التي يتم جمعها وتسجيلها بواسطة نوفا كوميرس وكيف نستخدمها.

1. المعلومات التي نجمعها
نقوم بجمع المعلومات الشخصية التي تقدمها لنا عند تقديم طلب، مثل اسمك وعنوان بريدك الإلكتروني ورقم هاتفك وعنوان الشحن ومعلومات الدفع. نقوم أيضًا بجمع البيانات تلقائيًا عند تصفحك لموقعنا، مثل عنوان IP الخاص بك ونوع المتصفح ومعلومات الجهاز.

2. كيف نستخدم معلوماتك
نحن نستخدم المعلومات التي نجمعها من أجل:
- توفير وتشغيل وصيانة موقعنا وخدماتنا
- معالجة طلباتك ومدفوعاتك وعمليات الشحن الخاصة بك
- التواصل معك، بما في ذلك لخدمة العملاء والدعم
- إرسال رسائل بريد إلكتروني إليك بخصوص طلبك أو العروض الترويجية (إذا قمت بالاشتراك)
- العثور على الاحتيال ومنعه

3. ملفات السجل
تتبع نوفا كوميرس إجراءً قياسيًا لاستخدام ملفات السجل. تسجل هذه الملفات الزوار عندما يزورون مواقع الويب. تتضمن المعلومات التي تجمعها ملفات السجل عناوين بروتوكول الإنترنت (IP) ونوع المتصفح ومزود خدمة الإنترنت (ISP) وختم التاريخ والوقت وصفحات الإحالة/الخروج وربما عدد النقرات.

4. ملفات تعريف الارتباط (Cookies)
مثل أي موقع ويب آخر، تستخدم نوفا كوميرس ملفات تعريف الارتباط. تُستخدم ملفات تعريف الارتباط هذه لتخزين المعلومات بما في ذلك تفضيلات الزوار والصفحات الموجودة على الموقع والتي وصل إليها الزائر أو زارها. تُستخدم المعلومات لتحسين تجربة المستخدمين من خلال تخصيص محتوى صفحة الويب الخاصة بنا بناءً على نوع متصفح الزوار و/أو معلومات أخرى.

5. سياسات الطرف الثالث
نحن لا نبيع أو نتاجر أو ننقل معلوماتك الشخصية التي يمكن التعرف عليها إلى أطراف خارجية. هذا لا يشمل الأطراف الثالثة الموثوقة التي تساعدنا في تشغيل موقعنا الإلكتروني أو إدارة أعمالنا أو خدمتك، طالما وافقت هذه الأطراف على الحفاظ على سرية هذه المعلومات.

6. اتصل بنا
إذا كانت لديك أسئلة إضافية أو تحتاج إلى مزيد من المعلومات حول سياسة الخصوصية الخاصة بنا، فلا تتردد في الاتصال بنا."""

ContentPage.objects.update_or_create(
    slug='terms',
    defaults={
        'title_en': 'Terms of Service',
        'title_ar': 'شروط الخدمة',
        'body_en': terms_body_en,
        'body_ar': terms_body_ar,
        'meta_title': 'Terms of Service - Nova Commerce',
        'meta_description': 'Our terms of service and usage conditions.',
        'is_published': True
    }
)

ContentPage.objects.update_or_create(
    slug='privacy',
    defaults={
        'title_en': 'Privacy Policy',
        'title_ar': 'سياسة الخصوصية',
        'body_en': privacy_body_en,
        'body_ar': privacy_body_ar,
        'meta_title': 'Privacy Policy - Nova Commerce',
        'meta_description': 'How we handle and protect your data.',
        'is_published': True
    }
)

print("Terms and Privacy pages created successfully!")

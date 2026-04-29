import re

with open('locale/ar/LC_MESSAGES/django.po', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove fuzzy comments
content = re.sub(r'#, fuzzy\n(?:#\|[^\n]*\n)*', '', content)
content = content.replace('نوفا كوميرس', 'كوزموس كوميرس')

with open('locale/ar/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
    f.write(content)

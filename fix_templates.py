import os
import re
from pathlib import Path

template_dir = Path('templates')

for html_file in template_dir.glob('*.html'):
    print(f"Processing {html_file.name}...")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add {% load static %} at the top if not present
    if '{% load static %}' not in content:
        content = '{% load static %}\n' + content
    
    # Replace href="css/...css" with href="{% static 'css/.../css" %}"
    content = re.sub(
        r'href="(css/[^"]+)"',
        r'href="{% static \'\1\' %}"',
        content
    )
    
    # Replace href="images/...
" with href="{% static 'images/..." %}"
    content = re.sub(
        r'href="(images/[^"]+)"',
        r'href="{% static \'\1\' %}"',
        content
    )
    
    # Replace src="js/...js"  with src="{% static 'js/...js" %}"
    content = re.sub(
        r'src="(js/[^"]+)"',
        r'src="{% static \'\1\' %}"',
        content
    )
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated {html_file.name}")

print("\nAll HTML files updated!")

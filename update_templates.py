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
        # Find the doctype or first line
        if content.startswith('<!DOCTYPE') or content.startswith('<html'):
            content = '{% load static %}\n' + content
        else:
            content = '{% load static %}\n' + content
    
    # Replace href="css/ with href="{% static 'css/
    content = re.sub(r'href="css/', r'href="{% static \'css/', content)
    content = re.sub(r'href="images/', r'href="{% static \'images/', content)
    
    # Replace src="js/ with src="{% static 'js/
    content = re.sub(r'src="js/', r'src="{% static \'js/', content)
    
    # Close the static tags
    content = re.sub(r'(href|src)="({% static \'[^"]+)"', r'\1="\2 %}"', content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated {html_file.name}")

print("\nAll HTML files updated!")

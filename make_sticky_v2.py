import os
import re
from pathlib import Path

# Updated breadcrumb CSS with sticky positioning
sticky_breadcrumb_css = '''        /* Breadcrumb Navigation Styles - Universal */
        .breadcrumb {
            position: sticky;
            top: 0;
            z-index: 100;
            background: linear-gradient(135deg, rgba(0, 123, 255, 0.95) 0%, rgba(102, 126, 234, 0.95) 100%);
            backdrop-filter: blur(10px);
            padding: 12px 25px;
            border-radius: 0;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            border-bottom: 2px solid rgba(0, 123, 255, 0.6);
        }

        .breadcrumb-item {
            color: #ffffff !important;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            padding: 5px 10px;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.2);
        }

        .breadcrumb-item:hover {
            background: rgba(255, 255, 255, 0.3);
            color: #ffffff !important;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(255, 255, 255, 0.3);
        }

        .breadcrumb-separator {
            color: #ffffff !important;
            font-weight: 600;
            user-select: none;
        }

        .breadcrumb-current {
            color: #ffd700 !important;
            font-weight: 700;
            font-size: 0.95rem;
            background: rgba(255, 215, 0, 0.2);
            padding: 5px 12px;
            border-radius: 5px;
        }

        @media (max-width: 768px) {
            .breadcrumb {
                padding: 10px 15px;
            }

            .breadcrumb-item,
            .breadcrumb-current {
                font-size: 0.85rem;
            }
        }'''

def replace_breadcrumb_css(file_path):
    """Replace breadcrumb CSS with sticky version"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if breadcrumb CSS exists
        if '/* Breadcrumb Navigation Styles' not in content:
            return False
        
        # More flexible pattern - match from start to end including variations
        # Match: /* Breadcrumb ... */ through the closing media query }
        pattern = r'/\*\s*Breadcrumb Navigation Styles[^*]*\*/.*?@media\s*\(max-width:\s*768px\)[^}]*\{[^}]*\.breadcrumb[^}]*\}[^}]*\.breadcrumb-item[^}]*\}[^}]*\.breadcrumb-current[^}]*\}[^}]*\}'
        
        matches = re.findall(pattern, content, re.DOTALL)
        
        if matches:
            # Replace the first match
            content = re.sub(pattern, sticky_breadcrumb_css.strip(), content, count=1, flags=re.DOTALL)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error: {file_path.name} - {e}")
        return False

# Process ALL HTML files in the project
base_path = r"c:\Users\yadav\Desktop\learn\learning-platform"

sections = [
    "HTML-CSS INTRACT",
    "java-script", 
    "REACT-JS INTRACT",
    "node",
    "MONGO-DB",
    "SQL",
    "BOOTSTRAP",
    "TAILWIND"
]

print("🔧 Making breadcrumbs sticky with improved pattern matching...\n")
total_fixed = 0

for section in sections:
    section_path = os.path.join(base_path, section)
    if not os.path.exists(section_path):
        continue
    
    print(f"📁 {section}")
    fixed_count = 0
    
    for file_path in Path(section_path).glob('*.html'):
        if replace_breadcrumb_css(file_path):
            print(f"  ✓ {file_path.name}")
            fixed_count += 1
    
    if fixed_count > 0:
        total_fixed += fixed_count
        print(f"  → Fixed: {fixed_count} files\n")

# Also fix main index.html
main_index = os.path.join(base_path, "index.html")
if os.path.exists(main_index):
    if replace_breadcrumb_css(main_index):
        print(f"✓ Main index.html")
        total_fixed += 1

print(f"\n{'='*60}")
print(f"✅ TOTAL FILES UPDATED: {total_fixed}")
print(f"{'='*60}")
print("\n🎨 Sticky breadcrumb features:")
print("  • position: sticky - stays at top when scrolling")
print("  • z-index: 100 - appears above content")
print("  • White text on blue gradient")
print("  • Gold current page indicator")

import os
import re
from pathlib import Path

# Updated breadcrumb CSS with better contrast for light backgrounds
breadcrumb_css_light_bg = '''
        /* Breadcrumb Navigation Styles */
        .breadcrumb {
            background: rgba(0, 123, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 12px 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(0, 123, 255, 0.3);
        }

        .breadcrumb-item {
            color: #007bff;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            padding: 5px 10px;
            border-radius: 5px;
        }

        .breadcrumb-item:hover {
            background: rgba(0, 123, 255, 0.2);
            color: #0056b3;
            transform: translateY(-1px);
        }

        .breadcrumb-separator {
            color: #666;
            font-weight: 300;
            user-select: none;
        }

        .breadcrumb-current {
            color: #0056b3;
            font-weight: 600;
            font-size: 0.95rem;
        }

        @media (max-width: 768px) {
            .breadcrumb {
                padding: 10px 15px;
            }

            .breadcrumb-item,
            .breadcrumb-current {
                font-size: 0.85rem;
            }
        }
'''

def fix_breadcrumb_visibility(file_path):
    """Fix breadcrumb visibility by updating CSS"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if this file has light background (white or light gray body/container)
        has_light_bg = (
            'background: white' in content or
            'background-color: #f4f4f4' in content or
            'background-color: white' in content or
            'background: #fff' in content
        )
        
        if not has_light_bg:
            return False  # Skip files with dark backgrounds
        
        # Find and replace the breadcrumb CSS
        pattern = r'/\* Breadcrumb Navigation Styles \*/.*?(?=\s*</style>|$)'
        
        if re.search(pattern, content, re.DOTALL):
            # Replace existing breadcrumb CSS
            content = re.sub(pattern, breadcrumb_css_light_bg.strip(), content, flags=re.DOTALL)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

# Process all HTML files
base_path = r"c:\Users\yadav\Desktop\learn\learning-platform"

sections = [
    "HTML-CSS INTRACT",
    "java-script",
    "REACT-JS INTRACT"
]

total_fixed = 0

for section in sections:
    section_path = os.path.join(base_path, section)
    if not os.path.exists(section_path):
        continue
    
    print(f"\n📁 Processing {section}...")
    fixed_count = 0
    
    for file_path in Path(section_path).glob('*.html'):
        if fix_breadcrumb_visibility(file_path):
            print(f"  ✓ Fixed {file_path.name}")
            fixed_count += 1
    
    total_fixed += fixed_count
    print(f"  Fixed: {fixed_count} files")

print(f"\n{'='*50}")
print(f"✅ Total files fixed: {total_fixed}")
print(f"{'='*50}")

import os
import re
from pathlib import Path

# Define breadcrumb CSS
breadcrumb_css = '''
        /* Breadcrumb Navigation Styles */
        .breadcrumb {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 12px 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .breadcrumb-item {
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            padding: 5px 10px;
            border-radius: 5px;
        }

        .breadcrumb-item:hover {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            transform: translateY(-1px);
        }

        .breadcrumb-separator {
            color: rgba(255, 255, 255, 0.6);
            font-weight: 300;
            user-select: none;
        }

        .breadcrumb-current {
            color: white;
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

def get_page_title(content):
    """Extract page title from HTML content"""
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    if title_match:
        title = title_match.group(1)
        # Clean up title
        title = re.sub(r'\s*-\s*Interactive.*', '', title)
        title = re.sub(r'\s*Study Guide.*', '', title)
        title = re.sub(r'\s*Learning.*', '', title)
        return title.strip()
    return "Page"

def get_breadcrumb_html(section_name, page_title):
    return f'''        <!-- Breadcrumb Navigation -->
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="../index.html" class="breadcrumb-item">🏠 Home</a>
            <span class="breadcrumb-separator">/</span>
            <a href="index.html" class="breadcrumb-item">{section_name}</a>
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-current">{page_title}</span>
        </nav>

'''

def process_directory(directory, section_name, exclude_files=['index.html']):
    """Process all HTML files in a directory"""
    processed = 0
    skipped = 0
    
    for file_path in Path(directory).glob('*.html'):
        if file_path.name in exclude_files:
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if breadcrumb already exists
            if 'class="breadcrumb"' in content:
                skipped += 1
                continue
            
            # Add CSS before closing </style> tag if not present
            if breadcrumb_css not in content:
                content = content.replace('    </style>', breadcrumb_css + '    </style>')
            
            # Get page title
            page_title = get_page_title(content)
            
            # Add breadcrumb HTML
            breadcrumb_html = get_breadcrumb_html(section_name, page_title)
            
            # Try different patterns to find where to insert breadcrumb
            patterns = [
                (r'(<div class="container">)\s*\n', r'\1\n' + breadcrumb_html),
                (r'(<body>)\s*\n', r'\1\n' + breadcrumb_html),
                (r'(<header)', breadcrumb_html + r'\1'),
            ]
            
            inserted = False
            for pattern, replacement in patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content, count=1)
                    inserted = True
                    break
            
            if inserted:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                processed += 1
                print(f"✓ {file_path.name}")
            else:
                print(f"⚠ Could not find insertion point in {file_path.name}")
                skipped += 1
                
        except Exception as e:
            print(f"✗ Error processing {file_path.name}: {e}")
            skipped += 1
    
    return processed, skipped

# Main execution
base_path = r"c:\Users\yadav\Desktop\learn\learning-platform"

sections = [
    ("HTML-CSS INTRACT", "HTML & CSS"),
    ("java-script", "JavaScript"),
    ("REACT-JS INTRACT", "React JS"),
]

total_processed = 0
total_skipped = 0

for folder, section_name in sections:
    dir_path = os.path.join(base_path, folder)
    if not os.path.exists(dir_path):
        print(f"Directory not found: {dir_path}")
        continue
    
    print(f"\n📁 Processing {folder}...")
    processed, skipped = process_directory(dir_path, section_name)
    total_processed += processed
    total_skipped += skipped
    print(f"   Processed: {processed}, Skipped: {skipped}")

print(f"\n{'='*50}")
print(f"✅ Total files processed: {total_processed}")
print(f"⏭️  Total files skipped: {total_skipped}")
print(f"{'='*50}")

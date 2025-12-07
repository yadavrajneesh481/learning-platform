import os
from pathlib import Path

# Simple direct replacement approach
base_path = r"c:\Users\yadav\Desktop\learn\learning-platform"

# The old breadcrumb CSS pattern (non-sticky)
old_css_start = '''        /* Breadcrumb Navigation Styles - Universal */
        .breadcrumb {
            background: linear-gradient(135deg, rgba(0, 123, 255, 0.15) 0%, rgba(102, 126, 234, 0.15) 100%);'''

# The new sticky breadcrumb CSS
new_css = '''        /* Breadcrumb Navigation Styles - Universal */
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

# Find all HTML files
all_files = list(Path(base_path).rglob('*.html'))
updated = 0
already_sticky = 0
no_breadcrumb = 0

print("🔧 Applying sticky breadcrumb CSS...\n")

for file_path in all_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if no breadcrumb CSS
        if '/* Breadcrumb Navigation Styles' not in content:
            no_breadcrumb += 1
            continue
        
        # Skip if already sticky
        if 'position: sticky' in content and '.breadcrumb {' in content:
            already_sticky += 1
            continue
        
        # Find and replace the old breadcrumb CSS block
        if old_css_start in content:
            # Find the end of the media query
            start_idx = content.find(old_css_start)
            # Find the closing brace of the media query
            media_start = content.find('@media (max-width: 768px)', start_idx)
            if media_start > 0:
                # Find the end - look for the closing brace after breadcrumb-current
                search_from = content.find('.breadcrumb-current', media_start)
                if search_from > 0:
                    # Find the next two closing braces
                    brace_count = 0
                    end_idx = search_from
                    while brace_count < 2 and end_idx < len(content):
                        if content[end_idx] == '}':
                            brace_count += 1
                            if brace_count == 2:
                                end_idx += 1
                                break
                        end_idx += 1
                    
                    # Replace the entire block
                    old_block = content[start_idx:end_idx]
                    content = content.replace(old_block, new_css)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✓ {file_path.relative_to(base_path)}")
                    updated += 1
        
    except Exception as e:
        print(f"✗ Error in {file_path.name}: {e}")

print(f"\n{'='*60}")
print(f"✅ Updated: {updated} files")
print(f"⏭️  Already sticky: {already_sticky} files")
print(f"⚠️  No breadcrumb: {no_breadcrumb} files")
print(f"📊 Total files scanned: {len(all_files)}")
print(f"{'='*60}")

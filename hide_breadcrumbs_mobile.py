import os
import re

def hide_breadcrumbs_mobile(directory):
    """
    Remove previous breadcrumb override styles and inject new CSS that:
    - Keeps breadcrumbs sticky on desktop
    - Hides breadcrumbs on mobile (max-width: 768px)
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if "breadcrumb" not in content.lower():
                        continue
                        
                    print(f"Processing: {filepath}")
                    
                    original_content = content
                    
                    # Remove the previous "Universal Sticky Breadcrumb Override" block
                    # This removes the entire <style> block that contains this comment
                    pattern = r'<style>\s*\/\*\s*Universal Sticky Breadcrumb Override\s*\*\/.*?<\/style>\s*'
                    content = re.sub(pattern, '', content, flags=re.DOTALL)
                    
                    # New CSS to inject
                    new_style = """
    <style>
        /* Sticky Breadcrumb - Desktop Only */
        .breadcrumb {
            position: sticky !important;
            top: 0 !important;
            z-index: 1000 !important;
        }
        
        /* Hide on Mobile/Small Devices */
        @media (max-width: 768px) {
            .breadcrumb {
                display: none !important;
            }
        }
    </style>
"""
                    
                    # Check if we already added this new style to avoid duplication
                    if "/* Sticky Breadcrumb - Desktop Only */" not in content:
                        if "</head>" in content:
                            content = content.replace("</head>", new_style + "\n</head>")
                        elif "</body>" in content:
                            content = content.replace("</body>", new_style + "\n</body>")
                    
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"✅ Updated: {filepath}")
                    else:
                        print(f"⏭️  No changes needed: {filepath}")

                except Exception as e:
                    print(f"❌ Error processing {filepath}: {e}")

if __name__ == "__main__":
    target_dir = r"c:\Users\yadav\Desktop\learn\learning-platform"
    print("Starting breadcrumb update process...")
    print("=" * 60)
    hide_breadcrumbs_mobile(target_dir)
    print("=" * 60)
    print("✅ Process complete!")

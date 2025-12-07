import os
import re

def fix_breadcrumbs(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if "breadcrumb" not in content:
                        continue
                        
                    print(f"Processing: {filepath}")
                    
                    original_content = content
                    
                    # 1. Remove display: none !important for breadcrumbs in media queries
                    content = re.sub(r'(\.breadcrumb\s*\{[^}]*?)display:\s*none\s*!important\s*;', r'\1', content, flags=re.DOTALL)
                    
                    # 2. Ensure universal sticky styles
                    # Check if .breadcrumb style exists
                    if ".breadcrumb {" in content:
                        # Append or ensure sticky styles exist. 
                        # A bit complex to regex edit inside existing block safely without breaking things.
                        # Easier strategy: RE-WRITE the specific mobile media query part or inject a new style block at the end of head?
                        # Injecting at end of head is safer to override.
                        pass
                    
                    # 3. Inject strict overrides at the end of <head> or before </body> if no head
                    # This ensures our styles win without complex parsing of existing CSS
                    
                    style_override = """
    <style>
        /* Universal Sticky Breadcrumb Override */
        .breadcrumb {
            position: sticky !important;
            top: 0 !important;
            z-index: 1000 !important;
        }
        
        /* Mobile Horizontal Scroll Override */
        @media (max-width: 768px) {
            .breadcrumb {
                display: flex !important;
                flex-wrap: nowrap !important;
                overflow-x: auto !important;
                white-space: nowrap !important;
                padding: 10px 15px !important;
                scrollbar-width: none; /* Firefox */
                -ms-overflow-style: none; /* IE/Edge */
            }
            .breadcrumb::-webkit-scrollbar {
                display: none; /* Chrome/Safari */
            }
            .breadcrumb-item {
                flex: 0 0 auto !important;
            }
        }
    </style>
"""
                    # Check if we already added this to avoid duplication if run multiple times
                    if "/* Universal Sticky Breadcrumb Override */" not in content:
                        if "</head>" in content:
                            content = content.replace("</head>", style_override + "\n</head>")
                        elif "</body>" in content:
                            content = content.replace("</body>", style_override + "\n</body>")
                    
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Updated: {filepath}")
                    else:
                        print(f"No changes needed: {filepath}")

                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    target_dir = r"c:\Users\yadav\Desktop\learn\learning-platform"
    fix_breadcrumbs(target_dir)

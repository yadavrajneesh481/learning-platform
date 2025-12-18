
import os
from pathlib import Path

# The button HTML to insert
BUTTON_HTML = '''            <a href="https://shimmering-dango-5a863e.netlify.app/" class="breadcrumb-item breadcrumb-explainer" target="_blank" style="background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%); color: #005f6b !important; font-weight: 800; border: 1px solid rgba(255,255,255,0.4); box-shadow: 0 4px 6px rgba(0,0,0,0.1);">🤖 Code Explainer</a>'''

def add_button_to_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if button already exists
        if 'https://shimmering-dango-5a863e.netlify.app/' in content:
            return False, "Already exists"

        # Find the breadcrumb nav
        nav_start = '<nav class="breadcrumb" aria-label="Breadcrumb">'
        if nav_start not in content:
            return False, "No breadcrumb found"

        # Insert the button after the opening tag
        new_content = content.replace(nav_start, nav_start + '\n' + BUTTON_HTML)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Added"

    except Exception as e:
        return False, f"Error: {e}"

def main():
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
    
    # Also check root directory
    all_paths = [base_path] + [os.path.join(base_path, s) for s in sections]

    total_added = 0
    total_skipped = 0

    print("🚀 Starting global rollout of Code Explainer button...\n")

    for section_path in all_paths:
        if not os.path.exists(section_path):
            continue
            
        section_name = os.path.basename(section_path)
        print(f"📁 Checking {section_name}...")
        
        folder_added = 0
        
        for file_path in Path(section_path).glob('*.html'):
            success, msg = add_button_to_file(file_path)
            if success:
                print(f"  ✓ {file_path.name}")
                folder_added += 1
                total_added += 1
            else:
                total_skipped += 1
                # distinct failures could be printed if needed, mainly skipping quiet
        
        if folder_added > 0:
            print(f"  → Added to {folder_added} files")

    print(f"\n{'='*50}")
    print(f"✅ COMPLETE")
    print(f"Total files updated: {total_added}")
    print(f"Total files skipped/unchanged: {total_skipped}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()

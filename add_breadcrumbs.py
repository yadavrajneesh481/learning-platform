import os
import re

# Define breadcrumb HTML template
def get_breadcrumb_html(section_name):
    return f'''        <!-- Breadcrumb Navigation -->
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="../index.html" class="breadcrumb-item">🏠 Home</a>
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-current">{section_name}</span>
        </nav>

'''

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

# Sections to process
sections = [
    ("node", "Node JS"),
    ("MONGO-DB", "MongoDB"),
    ("SQL", "MySQL"),
    ("BOOTSTRAP", "Bootstrap"),
    ("TAILWIND", "Tailwind CSS")
]

base_path = r"c:\Users\yadav\Desktop\learn\learning-platform"

for folder, section_name in sections:
    file_path = os.path.join(base_path, folder, "index.html")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add CSS before closing </style> tag
    if breadcrumb_css not in content:
        content = content.replace('    </style>', breadcrumb_css + '    </style>')
    
    # Add breadcrumb HTML after <div class="container">
    breadcrumb_html = get_breadcrumb_html(section_name)
    
    # Find the container div and add breadcrumb after it
    # Look for patterns like <div class="container"> followed by content
    pattern = r'(<div class="container">)\s*\n'
    if re.search(pattern, content):
        replacement = r'\1\n' + breadcrumb_html
        content = re.sub(pattern, replacement, content, count=1)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Added breadcrumb to {folder}/index.html")

print("\nAll section index files updated!")

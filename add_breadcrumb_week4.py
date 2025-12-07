import os

# Add breadcrumb CSS and HTML to week4.html
week4_file = r"c:\Users\yadav\Desktop\learn\learning-platform\HTML-CSS INTRACT\week4.html"

with open(week4_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Add breadcrumb CSS before closing </style> tag
breadcrumb_css = '''
        /* Breadcrumb Navigation Styles - Universal */
        .breadcrumb {
            background: linear-gradient(135deg, rgba(0, 123, 255, 0.15) 0%, rgba(102, 126, 234, 0.15) 100%);
            backdrop-filter: blur(10px);
            padding: 12px 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            border: 2px solid rgba(0, 123, 255, 0.4);
        }

        .breadcrumb-item {
            color: #0056b3 !important;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            padding: 5px 10px;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.8);
        }

        .breadcrumb-item:hover {
            background: rgba(0, 123, 255, 0.2);
            color: #003d82 !important;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
        }

        .breadcrumb-separator {
            color: #495057 !important;
            font-weight: 600;
            user-select: none;
        }

        .breadcrumb-current {
            color: #dc3545 !important;
            font-weight: 700;
            font-size: 0.95rem;
            background: rgba(255, 255, 255, 0.9);
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
        }
    </style>'''

# Replace closing </style> tag
content = content.replace('    </style>', breadcrumb_css)

# Add breadcrumb HTML after main-content opening
breadcrumb_html = '''        <div class="main-content" id="mainContent">
            <!-- Breadcrumb Navigation -->
            <nav class="breadcrumb" aria-label="Breadcrumb">
                <a href="../index.html" class="breadcrumb-item">🏠 Home</a>
                <span class="breadcrumb-separator">/</span>
                <a href="index.html" class="breadcrumb-item">HTML & CSS</a>
                <span class="breadcrumb-separator">/</span>
                <span class="breadcrumb-current">Week 4</span>
            </nav>

            <div class="search-bar">'''

content = content.replace('        <div class="main-content" id="mainContent">\r\n            <div class="search-bar">', breadcrumb_html)

with open(week4_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added breadcrumb to week4.html")

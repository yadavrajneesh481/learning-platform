import os

# Fix week4.html breadcrumb placement
week4_file = r"c:\Users\yadav\Desktop\learn\learning-platform\HTML-CSS INTRACT\week4.html"

with open(week4_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove breadcrumb from outside container (before sidebar)
content = content.replace('''    <div class="container">
        <!-- Breadcrumb Navigation -->
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="../index.html" class="breadcrumb-item">🏠 Home</a>
            <span class="breadcrumb-separator">/</span>
            <a href="index.html" class="breadcrumb-item">HTML & CSS</a>
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-current">Week 4</span>
        </nav>

        <aside class="sidebar"''', '''    <div class="container">
        <aside class="sidebar"''')

# Add breadcrumb inside main-content (after opening main tag)
content = content.replace('''        <main class="main-content" id="mainContent">
            <div class="search-bar">''', '''        <main class="main-content" id="mainContent">
            <!-- Breadcrumb Navigation -->
            <nav class="breadcrumb" aria-label="Breadcrumb">
                <a href="../index.html" class="breadcrumb-item">🏠 Home</a>
                <span class="breadcrumb-separator">/</span>
                <a href="index.html" class="breadcrumb-item">HTML & CSS</a>
                <span class="breadcrumb-separator">/</span>
                <span class="breadcrumb-current">Week 4</span>
            </nav>

            <div class="search-bar">''')

with open(week4_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed week4.html breadcrumb placement - moved from outside container to inside main-content")

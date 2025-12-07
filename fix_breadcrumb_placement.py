import os
import re

# Fix MongoDB - move breadcrumb inside main-content
mongodb_file = r"c:\Users\yadav\Desktop\learn\learning-platform\MONGO-DB\index.html"

with open(mongodb_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove breadcrumb from outside container
content = content.replace('''    <div class="container">
        <!-- Breadcrumb Navigation -->
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="../index.html" class="breadcrumb-item">🏠 Home</a>
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-current">MongoDB</span>
        </nav>

        <!-- Sidebar Navigation -->''', '''    <div class="container">
        <!-- Sidebar Navigation -->''')

# Add breadcrumb inside main-content after opening tag
content = content.replace('''        <!-- Main Content Area -->
        <main class="main-content">
            <div class="header">''', '''        <!-- Main Content Area -->
        <main class="main-content">
            <!-- Breadcrumb Navigation -->
            <nav class="breadcrumb" aria-label="Breadcrumb">
                <a href="../index.html" class="breadcrumb-item">🏠 Home</a>
                <span class="breadcrumb-separator">/</span>
                <span class="breadcrumb-current">MongoDB</span>
            </nav>

            <div class="header">''')

with open(mongodb_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed MongoDB breadcrumb placement")

# Fix Bootstrap - add breadcrumb inside main-content
bootstrap_file = r"c:\Users\yadav\Desktop\learn\learning-platform\BOOTSTRAP\index.html"

with open(bootstrap_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Add breadcrumb at start of main-content
content = content.replace('''    <!-- Main Content -->
    <main class="main-content">
        <!-- Get Started -->''', '''    <!-- Main Content -->
    <main class="main-content">
        <!-- Breadcrumb Navigation -->
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="../index.html" class="breadcrumb-item">🏠 Home</a>
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-current">Bootstrap</span>
        </nav>

        <!-- Get Started -->''')

with open(bootstrap_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed Bootstrap breadcrumb placement")

# Fix Tailwind - add breadcrumb inside main container
tailwind_file = r"c:\Users\yadav\Desktop\learn\learning-platform\TAILWIND\index.html"

with open(tailwind_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Add breadcrumb after main container opening
content = content.replace('''    <!-- Main Container -->
    <div class="container mx-auto px-4 py-8">

        <!-- Navigation Tabs -->''', '''    <!-- Main Container -->
    <div class="container mx-auto px-4 py-8">
        <!-- Breadcrumb Navigation -->
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="../index.html" class="breadcrumb-item">🏠 Home</a>
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-current">Tailwind CSS</span>
        </nav>

        <!-- Navigation Tabs -->''')

with open(tailwind_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed Tailwind breadcrumb placement")

print("\n✅ All breadcrumb placements fixed!")

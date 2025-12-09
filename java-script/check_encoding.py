import re

html_file = r"c:\Users\yadav\Desktop\learn\learning-platform\java-script\async-js-learning.html"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Check for common problematic characters
issues = []

# Check for non-breaking spaces
if '\u00a0' in content:
    count = content.count('\u00a0')
    issues.append(f"Found {count} non-breaking spaces (\\u00a0)")

# Check for zero-width characters
zero_width_chars = ['\u200b', '\u200c', '\u200d', '\ufeff']
for char in zero_width_chars:
    if char in content:
        count = content.count(char)
        issues.append(f"Found {count} zero-width characters ({repr(char)})")

# Check for mixed quotes
smart_quotes = ['\u2018', '\u2019', '\u201c', '\u201d']
for char in smart_quotes:
    if char in content:
        count = content.count(char)
        issues.append(f"Found {count} smart quotes ({repr(char)})")

# Extract script and check its ending
match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if match:
    script = match.group(1)
    last_100 = script[-100:]
    print("Last 100 characters of script:")
    print(repr(last_100))
    print()

if issues:
    print("⚠ Potential issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✓ No encoding issues found")

# Check file encoding
print(f"\nFile size: {len(content)} characters")
print(f"File encoding: UTF-8 (as read)")

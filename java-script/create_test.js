// Create a minimal test HTML to see if browser can execute the script
const fs = require('fs');

const htmlFile = 'c:/Users/yadav/Desktop/learn/learning-platform/java-script/async-js-learning.html';
const testFile = 'c:/Users/yadav/Desktop/learn/learning-platform/java-script/test_minimal.html';

const content = fs.readFileSync(htmlFile, 'utf-8');

// Extract just the script part
const scriptMatch = content.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/);

if (scriptMatch) {
    const script = scriptMatch[1];

    // Create minimal HTML
    const minimalHtml = `<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
<h1>Testing Script</h1>
<script>
${script}
</script>
</body>
</html>`;

    fs.writeFileSync(testFile, minimalHtml, 'utf-8');
    console.log("Created test_minimal.html");
    console.log("Open this file in your browser to test if the script runs");
    console.log(`File: ${testFile}`);
} else {
    console.log("Could not extract script");
}

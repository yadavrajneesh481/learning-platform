// Script to remove old code formatting CSS and prepare for new version
const fs = require('fs');
const path = require('path');

function removeOldCSS(filePath) {
    try {
        let content = fs.readFileSync(filePath, 'utf8');

        // Check if the file has the old CSS
        if (!content.includes('/* Code Block Formatting - Universal Styles */')) {
            return false;
        }

        // Find and remove the old CSS block
        const startMarker = '/* Code Block Formatting - Universal Styles */';
        const startIndex = content.indexOf(startMarker);

        if (startIndex === -1) {
            return false;
        }

        // Find the end of this CSS block (look for the closing of scrollbar styles)
        const endMarker = 'pre::-webkit-scrollbar-thumb:hover {';
        const endIndex = content.indexOf(endMarker, startIndex);

        if (endIndex === -1) {
            return false;
        }

        // Find the end of the hover rule
        const finalEnd = content.indexOf('}', endIndex + endMarker.length);

        if (finalEnd === -1) {
            return false;
        }

        // Remove the entire block (including the newlines before it)
        const beforeCSS = content.substring(0, startIndex).trimEnd();
        const afterCSS = content.substring(finalEnd + 1);

        const updatedContent = beforeCSS + '\n    ' + afterCSS;

        fs.writeFileSync(filePath, updatedContent, 'utf8');
        console.log(`✓ Removed old CSS from ${path.basename(filePath)}`);
        return true;
    } catch (error) {
        console.error(`✗ Error processing ${filePath}:`, error.message);
        return false;
    }
}

function processDirectory(dirPath) {
    const files = fs.readdirSync(dirPath);
    let processedCount = 0;

    files.forEach(file => {
        const filePath = path.join(dirPath, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory() && !file.startsWith('.')) {
            processedCount += processDirectory(filePath);
        } else if (file.endsWith('.html')) {
            if (removeOldCSS(filePath)) {
                processedCount++;
            }
        }
    });

    return processedCount;
}

// Main execution
const rootDir = path.join(__dirname, '..');
console.log('Removing old CSS from HTML files...\n');
const count = processDirectory(rootDir);
console.log(`\n✓ Removed CSS from ${count} files`);

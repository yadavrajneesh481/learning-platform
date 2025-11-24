// Script to add proper code formatting CSS to all HTML files
const fs = require('fs');
const path = require('path');

const codeFormattingCSS = `
        /* Code Block Formatting - Universal Styles */
        pre {
            background: #282c34 !important;
            color: #abb2bf !important;
            padding: 20px !important;
            border-radius: 8px !important;
            overflow-x: auto !important;
            overflow-y: auto !important;
            margin: 15px 0 !important;
            font-family: 'Courier New', 'Consolas', 'Monaco', monospace !important;
            font-size: 14px !important;
            line-height: 1.6 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
            white-space: pre !important;
            word-wrap: normal !important;
            tab-size: 4 !important;
        }

        code {
            font-family: 'Courier New', 'Consolas', 'Monaco', monospace !important;
            font-size: 14px;
            color: #e06c75;
            background: rgba(0, 0, 0, 0.1);
            padding: 2px 6px;
            border-radius: 3px;
        }

        pre code {
            background: transparent !important;
            padding: 0 !important;
            color: #abb2bf !important;
            display: block !important;
            white-space: pre !important;
            word-wrap: normal !important;
            overflow-wrap: normal !important;
        }

        /* Syntax Highlighting Classes */
        .syntax-keyword { color: #c678dd; font-weight: bold; }
        .syntax-tag { color: #e06c75; }
        .syntax-attr { color: #d19a66; }
        .syntax-string { color: #98c379; }
        .syntax-comment { color: #5c6370; font-style: italic; }
        .syntax-number { color: #d19a66; }
        .syntax-function { color: #61afef; }
        .syntax-operator { color: #56b6c2; }
        .syntax-variable { color: #e5c07b; }

        /* Code Block Container */
        .code-block {
            background: #282c34;
            border-radius: 8px;
            margin: 20px 0;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .code-block pre {
            margin: 0;
            border-radius: 0;
            box-shadow: none;
        }

        /* Code Example Container */
        .code-example {
            background: #282c34;
            color: #abb2bf;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            overflow-x: auto;
            position: relative;
        }

        .code-example pre {
            margin: 0;
            background: transparent;
            padding: 0;
            box-shadow: none;
        }

        /* Demo Box Code */
        .demo-box pre {
            background: #1e2127;
            padding: 15px;
            border-radius: 6px;
        }

        /* Inline Code */
        p code, li code, td code, th code {
            background: rgba(0, 0, 0, 0.1);
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
            color: #e06c75;
        }

        /* Dark Mode Support */
        body.dark-mode pre {
            background: #1e1e1e;
            border-color: rgba(255, 255, 255, 0.2);
        }

        body.dark-mode code {
            background: rgba(255, 255, 255, 0.1);
        }

        /* Scrollbar Styling for Code Blocks */
        pre::-webkit-scrollbar {
            height: 8px;
        }

        pre::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
        }

        pre::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 4px;
        }

        pre::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
`;

function addCodeFormattingToHTML(filePath) {
    try {
        let content = fs.readFileSync(filePath, 'utf8');

        // Check if the file already has code formatting CSS
        if (content.includes('/* Code Block Formatting - Universal Styles */')) {
            console.log(`✓ Skipping ${filePath} - already has code formatting`);
            return false;
        }

        // Find the closing </style> tag
        const styleEndIndex = content.lastIndexOf('</style>');

        if (styleEndIndex === -1) {
            console.log(`✗ No <style> tag found in ${filePath}`);
            return false;
        }

        // Insert the CSS before </style>
        const updatedContent = content.slice(0, styleEndIndex) +
            codeFormattingCSS +
            '\n    ' + content.slice(styleEndIndex);

        fs.writeFileSync(filePath, updatedContent, 'utf8');
        console.log(`✓ Added code formatting to ${filePath}`);
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
            if (addCodeFormattingToHTML(filePath)) {
                processedCount++;
            }
        }
    });

    return processedCount;
}

// Main execution
const rootDir = path.join(__dirname, '..');
console.log('Starting to add code formatting to HTML files...\n');
const count = processDirectory(rootDir);
console.log(`\n✓ Successfully processed ${count} files`);

// Script to fix code block structure across all HTML files
// This ensures all code blocks use proper <pre><code> tags

const fs = require('fs');
const path = require('path');

let filesProcessed = 0;
let blocksFixed = 0;

function fixCodeBlocks(filePath) {
    try {
        let content = fs.readFileSync(filePath, 'utf8');
        let modified = false;
        let localBlocksFixed = 0;

        // Pattern 1: Fix <div class="code-example"> without <pre><code>
        // Match: <div class="code-example">CODE_HERE</div>
        // Where CODE_HERE doesn't start with <pre>
        const codeExamplePattern = /<div class="code-example">\s*(?!<pre>)([\s\S]*?)<\/div>/gi;

        content = content.replace(codeExamplePattern, (match, codeContent) => {
            // Skip if already has pre tag
            if (codeContent.trim().startsWith('<pre>')) {
                return match;
            }

            // Skip if it's empty or just whitespace
            if (!codeContent.trim()) {
                return match;
            }

            localBlocksFixed++;
            modified = true;

            // Wrap the code content in <pre><code>
            return `<div class="code-example"><pre><code>${codeContent}</code></pre></div>`;
        });

        // Pattern 2: Fix standalone code blocks that should be in <pre><code>
        // This is more conservative - only fix obvious code patterns

        if (modified) {
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`✓ Fixed ${localBlocksFixed} code blocks in ${path.basename(filePath)}`);
            blocksFixed += localBlocksFixed;
            filesProcessed++;
            return true;
        } else {
            console.log(`  Skipped ${path.basename(filePath)} - no issues found`);
            return false;
        }
    } catch (error) {
        console.error(`✗ Error processing ${filePath}:`, error.message);
        return false;
    }
}

function processDirectory(dirPath) {
    const files = fs.readdirSync(dirPath);

    files.forEach(file => {
        const filePath = path.join(dirPath, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory() && !file.startsWith('.')) {
            processDirectory(filePath);
        } else if (file.endsWith('.html')) {
            fixCodeBlocks(filePath);
        }
    });
}

// Main execution
console.log('🔧 Starting code block structure fix...\n');
console.log('This will wrap code in <div class="code-example"> with proper <pre><code> tags\n');

const rootDir = path.join(__dirname, '..');
processDirectory(rootDir);

console.log('\n' + '='.repeat(60));
console.log(`✅ COMPLETE!`);
console.log(`📊 Files processed: ${filesProcessed}`);
console.log(`🔧 Code blocks fixed: ${blocksFixed}`);
console.log('='.repeat(60));

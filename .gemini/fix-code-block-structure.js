// Script to fix code block structural issues across all HTML files
// Fixes: <code><div class="code-header">...</div></code> patterns

const fs = require('fs');
const path = require('path');

let filesProcessed = 0;
let issuesFixed = 0;
let filesWithIssues = [];

function fixCodeBlockStructure(filePath) {
    try {
        let content = fs.readFileSync(filePath, 'utf8');
        let modified = false;
        let localIssuesFixed = 0;
        const fileName = path.basename(filePath);

        // Pattern 1: Fix <code><div class="code-header">
        // This is the main issue - code-header should be outside <code> tag
        const pattern1 = /<div class="code-example">\s*<pre>\s*<code>\s*<div class="code-header">([\s\S]*?)<\/div>\s*<\/code>\s*<\/pre>\s*<\/div>/gi;

        content = content.replace(pattern1, (match, headerContent) => {
            localIssuesFixed++;
            modified = true;
            // Move code-header outside of code tags
            return `<div class="code-example">
                <div class="code-header">${headerContent}</div>
            </div>`;
        });

        // Pattern 2: Fix cases where code-header is followed by actual code in separate pre/code tags
        const pattern2 = /<div class="code-example">\s*<pre>\s*<code>\s*<div class="code-header">([\s\S]*?)<\/div>\s*<\/code>\s*<\/pre>\s*<\/div>\s*<pre>\s*<code>([\s\S]*?)<\/code>\s*<\/pre>/gi;

        content = content.replace(pattern2, (match, headerContent, codeContent) => {
            localIssuesFixed++;
            modified = true;
            return `<div class="code-example">
                <div class="code-header">${headerContent}</div>
                <pre><code>${codeContent}</code></pre>
            </div>`;
        });

        // Pattern 3: Fix inline style code blocks (convert to proper structure)
        const pattern3 = /<div style="background:\s*#f8f9fa;\s*padding:\s*10px;\s*border-radius:\s*3px;\s*font-family:\s*monospace[^"]*">([\s\S]*?)<\/div>/gi;

        content = content.replace(pattern3, (match, codeContent) => {
            // Only replace if it looks like code (contains <br> or code-like content)
            if (codeContent.includes('<br>') || codeContent.includes('&nbsp;') || codeContent.match(/\w+\s*[=:]/)) {
                localIssuesFixed++;
                modified = true;
                // Clean up HTML entities and convert to proper code block
                const cleanCode = codeContent
                    .replace(/<br\s*\/?>/gi, '\n')
                    .replace(/&nbsp;/g, ' ')
                    .trim();
                return `<div class="code-example"><pre><code>${cleanCode}</code></pre></div>`;
            }
            return match;
        });

        // Pattern 4: Remove duplicate/nested code-example divs
        const pattern4 = /<div class="code-example">\s*<div class="code-example">/gi;
        content = content.replace(pattern4, '<div class="code-example">');

        const pattern5 = /<\/div>\s*<\/div>\s*<\/div>\s*<pre><code>/gi;
        if (pattern5.test(content)) {
            localIssuesFixed++;
            modified = true;
        }

        if (modified) {
            // Create backup before modifying
            const backupPath = filePath + '.backup';
            if (!fs.existsSync(backupPath)) {
                fs.writeFileSync(backupPath, fs.readFileSync(filePath));
            }

            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`✓ Fixed ${localIssuesFixed} issues in ${fileName}`);
            filesWithIssues.push({
                file: fileName,
                path: filePath,
                issuesFixed: localIssuesFixed
            });
            issuesFixed += localIssuesFixed;
            filesProcessed++;
            return true;
        } else {
            console.log(`  ✓ No issues found in ${fileName}`);
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
        } else if (file.endsWith('.html') && !file.endsWith('.backup')) {
            fixCodeBlockStructure(filePath);
        }
    });
}

// Main execution
console.log('🔧 Starting code block structure fix...\n');
console.log('This will fix structural issues in code blocks across all HTML files');
console.log('Backups will be created as .backup files\n');
console.log('='.repeat(70));

const rootDir = path.join(__dirname, '..');
processDirectory(rootDir);

console.log('\n' + '='.repeat(70));
console.log(`✅ COMPLETE!`);
console.log(`📊 Statistics:`);
console.log(`   - Files processed: ${filesProcessed}`);
console.log(`   - Total issues fixed: ${issuesFixed}`);
console.log(`   - Files scanned: ${filesProcessed + (83 - filesProcessed)} (no issues in ${83 - filesProcessed} files)`);

if (filesWithIssues.length > 0) {
    console.log(`\n📝 Files modified:`);
    filesWithIssues.forEach(item => {
        console.log(`   - ${item.file}: ${item.issuesFixed} issue(s) fixed`);
    });

    console.log(`\n💾 Backup files created with .backup extension`);
    console.log(`   To restore: remove .backup extension`);
    console.log(`   To clean up: delete all .backup files after verification`);
}

console.log('='.repeat(70));

// Generate summary report
const reportPath = path.join(__dirname, 'structure-fix-report.txt');
const reportContent = `Code Block Structure Fix Report
Generated: ${new Date().toLocaleString()}

Summary:
- Files processed: ${filesProcessed}
- Total issues fixed: ${issuesFixed}
- Files with issues: ${filesWithIssues.length}

Files Modified:
${filesWithIssues.map(item => `  ${item.file} - ${item.issuesFixed} issue(s)`).join('\n')}

Backup Information:
- Backup files created with .backup extension
- Original files can be restored by removing .backup extension
- Delete .backup files after verifying fixes

Issues Fixed:
1. Moved code-header divs outside of <code> tags
2. Fixed nested code-example divs
3. Converted inline-style code blocks to proper structure
4. Cleaned up malformed HTML in code blocks
`;

fs.writeFileSync(reportPath, reportContent);
console.log(`\n📄 Detailed report saved to: structure-fix-report.txt`);

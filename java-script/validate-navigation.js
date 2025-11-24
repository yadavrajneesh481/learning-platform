#!/usr/bin/env node

/**
 * Navigation Validation Script
 * 
 * This script validates that all tutorial pages have consistent navigation buttons
 * and helps identify any pages that might be missing navigation or have inconsistent styling.
 */

const fs = require('fs');
const path = require('path');

// Configuration
const TUTORIAL_EXTENSIONS = ['.html'];
const NAVIGATION_PATTERNS = {
    homeLink: /<a[^>]*href="index\.html"[^>]*class="home-link"[^>]*>.*?Back to Course Home.*?<\/a>/i,
    homeLinkCSS: /\.home-link\s*{[^}]*}/i,
    ariaLabel: /aria-label="Return to JavaScript course homepage"/i
};

const EXCLUDED_FILES = ['index.html']; // Main homepage doesn't need navigation to itself

/**
 * Get all HTML tutorial files in the current directory
 */
function getTutorialFiles() {
    const files = fs.readdirSync('.')
        .filter(file => {
            const ext = path.extname(file);
            return TUTORIAL_EXTENSIONS.includes(ext) && !EXCLUDED_FILES.includes(file);
        })
        .sort();
    
    return files;
}

/**
 * Check if a file contains the navigation button
 */
function hasNavigationButton(filePath) {
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        return {
            hasHomeLink: NAVIGATION_PATTERNS.homeLink.test(content),
            hasCSS: NAVIGATION_PATTERNS.homeLinkCSS.test(content),
            hasAriaLabel: NAVIGATION_PATTERNS.ariaLabel.test(content),
            content: content
        };
    } catch (error) {
        console.error(`Error reading file ${filePath}:`, error.message);
        return {
            hasHomeLink: false,
            hasCSS: false,
            hasAriaLabel: false,
            content: '',
            error: error.message
        };
    }
}

/**
 * Validate navigation consistency across all tutorial pages
 */
function validateNavigation() {
    console.log('🔍 JavaScript Course Navigation Validator\n');
    console.log('=' .repeat(50));
    
    const tutorialFiles = getTutorialFiles();
    console.log(`📚 Found ${tutorialFiles.length} tutorial files to validate\n`);
    
    const results = {
        total: tutorialFiles.length,
        passed: 0,
        failed: 0,
        issues: []
    };
    
    tutorialFiles.forEach(file => {
        const validation = hasNavigationButton(file);
        const issues = [];
        
        if (!validation.hasHomeLink) {
            issues.push('Missing navigation button');
        }
        
        if (!validation.hasCSS) {
            issues.push('Missing navigation CSS styles');
        }
        
        if (!validation.hasAriaLabel) {
            issues.push('Missing accessibility ARIA label');
        }
        
        if (validation.error) {
            issues.push(`File read error: ${validation.error}`);
        }
        
        if (issues.length === 0) {
            console.log(`✅ ${file} - All navigation checks passed`);
            results.passed++;
        } else {
            console.log(`❌ ${file} - Issues found:`);
            issues.forEach(issue => console.log(`   • ${issue}`));
            results.failed++;
            results.issues.push({ file, issues });
        }
    });
    
    // Summary
    console.log('\n' + '=' .repeat(50));
    console.log('📊 VALIDATION SUMMARY');
    console.log('=' .repeat(50));
    console.log(`Total files checked: ${results.total}`);
    console.log(`✅ Passed: ${results.passed}`);
    console.log(`❌ Failed: ${results.failed}`);
    
    if (results.failed === 0) {
        console.log('\n🎉 All tutorial pages have consistent navigation! 🎉');
        return true;
    } else {
        console.log('\n⚠️  Issues found that need attention:');
        results.issues.forEach(({ file, issues }) => {
            console.log(`\n📄 ${file}:`);
            issues.forEach(issue => console.log(`   • ${issue}`));
        });
        
        console.log('\n💡 To fix these issues:');
        console.log('1. Add the navigation button HTML: <a href="index.html" class="home-link" aria-label="Return to JavaScript course homepage">🏠 Back to Course Home</a>');
        console.log('2. Add the navigation CSS styles for .home-link class');
        console.log('3. Ensure proper accessibility attributes are included');
        
        return false;
    }
}

/**
 * Generate a template for adding navigation to new pages
 */
function generateNavigationTemplate() {
    return `
<!-- Navigation Template for New Tutorial Pages -->

<!-- 1. Add this CSS to your <style> section: -->
<style>
.home-link {
    display: inline-block;
    margin-bottom: 20px;
    padding: 10px 15px;
    background: #28a745;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.home-link:hover {
    background: #218838;
    transform: translateY(-1px);
}

.home-link:focus {
    outline: 2px solid #ffc107;
    outline-offset: 2px;
}

@media (max-width: 768px) {
    .home-link {
        padding: 8px 12px;
        font-size: 14px;
    }
}
</style>

<!-- 2. Add this HTML at the top of your <body> content: -->
<a href="index.html" class="home-link" aria-label="Return to JavaScript course homepage">🏠 Back to Course Home</a>
`;
}

/**
 * Main execution
 */
function main() {
    const args = process.argv.slice(2);
    
    if (args.includes('--template')) {
        console.log('📋 Navigation Template for New Pages:');
        console.log(generateNavigationTemplate());
        return;
    }
    
    if (args.includes('--help')) {
        console.log('JavaScript Course Navigation Validator');
        console.log('');
        console.log('Usage:');
        console.log('  node validate-navigation.js          # Run validation');
        console.log('  node validate-navigation.js --template  # Show navigation template');
        console.log('  node validate-navigation.js --help      # Show this help');
        return;
    }
    
    const success = validateNavigation();
    process.exit(success ? 0 : 1);
}

// Run the script
if (require.main === module) {
    main();
}

module.exports = {
    validateNavigation,
    generateNavigationTemplate,
    getTutorialFiles,
    hasNavigationButton
};
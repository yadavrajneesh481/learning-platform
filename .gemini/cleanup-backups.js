// Script to clean up backup files after verification
// Run this ONLY after you've verified all fixes are working correctly

const fs = require('fs');
const path = require('path');

let backupsFound = 0;
let backupsDeleted = 0;

function findAndDeleteBackups(dirPath) {
    const files = fs.readdirSync(dirPath);

    files.forEach(file => {
        const filePath = path.join(dirPath, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory() && !file.startsWith('.')) {
            findAndDeleteBackups(filePath);
        } else if (file.endsWith('.backup')) {
            backupsFound++;
            console.log(`Found backup: ${filePath}`);

            try {
                fs.unlinkSync(filePath);
                backupsDeleted++;
                console.log(`  ✓ Deleted`);
            } catch (error) {
                console.error(`  ✗ Error deleting: ${error.message}`);
            }
        }
    });
}

// Main execution
console.log('🧹 Cleaning up backup files...\n');
console.log('⚠️  WARNING: This will permanently delete all .backup files!');
console.log('   Make sure you have verified all fixes are working correctly.\n');

const rootDir = path.join(__dirname, '..');
findAndDeleteBackups(rootDir);

console.log('\n' + '='.repeat(60));
console.log(`✅ Cleanup Complete!`);
console.log(`📊 Statistics:`);
console.log(`   - Backup files found: ${backupsFound}`);
console.log(`   - Backup files deleted: ${backupsDeleted}`);
console.log('='.repeat(60));

if (backupsDeleted > 0) {
    console.log('\n✓ All backup files have been removed.');
    console.log('  Your project is now clean!');
} else {
    console.log('\n  No backup files found to delete.');
}

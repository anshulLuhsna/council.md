const fs = require('fs');
let content = fs.readFileSync('public/summary.html', 'utf-8');
content = content.replace(/\\`/g, '`');
content = content.replace(/\\\$/g, '$');
fs.writeFileSync('public/summary.html', content);

const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function checkGemini() {
    console.log("Launching headless Chrome to check Gemini state...");
    const browser = await puppeteer.launch({
        executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        userDataDir: 'C:\\Users\\Curtis\\AppData\\Local\\Google\\Chrome\\User Data_Temp',
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    
    console.log("Navigating to Gemini...");
    await page.goto('https://gemini.google.com/app', { waitUntil: 'networkidle2' });
    
    console.log("Taking screenshot...");
    await page.screenshot({ path: 'gemini_debug.png' });
    
    const html = await page.content();
    fs.writeFileSync('gemini_debug.html', html);
    
    console.log("Done.");
    await browser.close();
}

checkGemini().catch(console.error);

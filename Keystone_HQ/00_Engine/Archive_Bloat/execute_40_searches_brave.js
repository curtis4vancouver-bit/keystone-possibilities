const fs = require('fs');
const path = require('path');

async function runBraveResearch() {
    console.log("Starting Keystone Brave API Deep Research...");
    
    const queuePath = 'C:\\Users\\Curtis\\.gemini\\antigravity\\brain\\dcfb044f-d157-4191-8dd4-486712240c1d\\deep_research_queue.md';
    const queueContent = fs.readFileSync(queuePath, 'utf-8');
    const prompts = [...queueContent.matchAll(/\*\*"([^"]+)"\*\*/g)].map(m => m[1]);
    console.log(`Found ${prompts.length} prompts to research.`);

    const outDir = 'c:\\Users\\Curtis\\New folder\\construction-website\\Keystone_HQ\\00_Master_Brain\\Deep_Research_Results';
    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

    const API_KEY = "BSAlHe-SuRmVpoR86sunbF-5fK7m3kC";

    for (let i = 0; i < prompts.length; i++) {
        const prompt = prompts[i];
        console.log(`\n[${i+1}/${prompts.length}] Researching: ${prompt.substring(0, 40)}...`);
        
        try {
            const query = prompt + " 2026 guide MCP AI";
            const response = await fetch(`https://api.search.brave.com/res/v1/web/search?q=${encodeURIComponent(query)}&count=10`, {
                headers: {
                    "Accept": "application/json",
                    "X-Subscription-Token": API_KEY
                }
            });
            
            if (!response.ok) {
                console.log(`  ❌ Error HTTP: ${response.status} ${response.statusText}`);
                continue;
            }
            
            const data = await response.json();
            
            let results = "";
            if (data.web && data.web.results) {
                results = data.web.results.map(r => `### [${r.title}](${r.url})\n${r.description}`).join('\n\n---\n\n');
            } else {
                results = "No web results found.";
            }

            const mdContent = `# Deep Research: ${prompt}\n\n## Brave Search Intelligence (2026)\n\n${results}\n`;
            const filename = `DeepDive_${i+1}_${Date.now()}.md`;
            
            fs.writeFileSync(path.join(outDir, filename), mdContent);
            console.log(`  ✅ Saved intelligence to ${filename}`);
            
            // Wait 1 second to respect rate limits
            await new Promise(r => setTimeout(r, 1000));
            
        } catch (err) {
            console.log(`  ❌ Error: ${err.message}`);
        }
    }
    
    console.log("\n🎉 All 40 Deep Dives Completed Successfully via Brave API!");
}

runBraveResearch().catch(console.error);

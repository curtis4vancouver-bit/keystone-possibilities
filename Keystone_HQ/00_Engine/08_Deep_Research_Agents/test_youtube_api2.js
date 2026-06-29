const https = require('https');

const API_KEY = 'AIzaSyD-a49LpvfBhcFar4jc4C99oN_uIMeOGgQ';

function searchChannel(query) {
  const url = `https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(query)}&type=channel&maxResults=1&key=${API_KEY}`;
  
  https.get(url, (resp) => {
    let data = '';
    resp.on('data', (chunk) => { data += chunk; });
    resp.on('end', () => {
      try {
        const result = JSON.parse(data);
        if (result.items && result.items.length > 0) {
            console.log(`=== ${query} ===`);
            console.log(`Channel ID: ${result.items[0].id.channelId}`);
            console.log(`Title: ${result.items[0].snippet.title}`);
            console.log(`Description: ${result.items[0].snippet.description}`);
            console.log(`Published At: ${result.items[0].snippet.publishedAt}`);
            console.log('-------------------------');
        } else {
            console.log(`No results for ${query}`);
        }
      } catch(e) {
          console.log("Error parsing: " + e);
      }
    });
  }).on("error", (err) => {
    console.log("Error: " + err.message);
  });
}

searchChannel("Keystone Recomposition");
searchChannel("Keystone Protocols");
searchChannel("Keystone Possibilities");

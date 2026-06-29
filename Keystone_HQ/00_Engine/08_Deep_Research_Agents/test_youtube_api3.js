const https = require('https');

const API_KEY = 'AIzaSyD-a49LpvfBhcFar4jc4C99oN_uIMeOGgQ';

const channelIds = [
  'UCxURlqMNhAtxUTpdXmlOYaw', // Protocols
  'UCMn1f9DTF_iybKmv5WlTm9Q', // Recomposition
  'UC8KMj_nq-9Woss8ezknzkGA'  // Possibilities
];

const url = `https://youtube.googleapis.com/youtube/v3/channels?part=statistics,snippet&id=${channelIds.join(',')}&key=${API_KEY}`;

https.get(url, (resp) => {
  let data = '';
  resp.on('data', (chunk) => { data += chunk; });
  resp.on('end', () => {
    try {
      const result = JSON.parse(data);
      result.items.forEach(item => {
        console.log(`=== ${item.snippet.title} ===`);
        console.log(`Subscribers: ${item.statistics.subscriberCount}`);
        console.log(`Total Views: ${item.statistics.viewCount}`);
        console.log(`Video Count: ${item.statistics.videoCount}`);
        console.log(`Description: ${item.snippet.description}`);
        console.log('-------------------------');
      });
    } catch(e) {
        console.log("Error parsing: " + e);
    }
  });
}).on("error", (err) => {
  console.log("Error: " + err.message);
});

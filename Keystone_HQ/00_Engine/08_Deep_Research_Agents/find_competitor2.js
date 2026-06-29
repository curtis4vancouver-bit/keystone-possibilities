const https = require('https');

const API_KEY = 'AIzaSyD-a49LpvfBhcFar4jc4C99oN_uIMeOGgQ';

// Search for videos about the wolverine stack
const query = encodeURIComponent("wolverine stack bpc-157 tb-500 doctor");
const url = `https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=${query}&type=video&maxResults=50&order=viewCount&key=${API_KEY}`;

https.get(url, (resp) => {
  let data = '';
  resp.on('data', (chunk) => { data += chunk; });
  resp.on('end', () => {
    try {
      const result = JSON.parse(data);
      const channelIds = [...new Set(result.items.map(item => item.snippet.channelId))];
      
      if (channelIds.length > 0) {
          // get stats in chunks of 50
          const statsUrl = `https://youtube.googleapis.com/youtube/v3/channels?part=statistics,snippet&id=${channelIds.slice(0, 50).join(',')}&key=${API_KEY}`;
          https.get(statsUrl, (res2) => {
              let data2 = '';
              res2.on('data', (c) => { data2 += c; });
              res2.on('end', () => {
                  const statsObj = JSON.parse(data2);
                  statsObj.items.forEach(ch => {
                      if (ch.statistics.videoCount < 100) {
                          console.log(`Channel: ${ch.snippet.title}`);
                          console.log(`Videos: ${ch.statistics.videoCount}`);
                          console.log(`Subs: ${ch.statistics.subscriberCount}`);
                          console.log(`Published: ${ch.snippet.publishedAt}`);
                          console.log(`Link: https://www.youtube.com/channel/${ch.id}`);
                          console.log('---');
                      }
                  });
              });
          });
      }
    } catch(e) {
        console.log("Error: " + e);
    }
  });
});

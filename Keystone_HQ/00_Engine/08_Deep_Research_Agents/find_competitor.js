const https = require('https');

const API_KEY = 'AIzaSyD-a49LpvfBhcFar4jc4C99oN_uIMeOGgQ';

// Search for channels matching the criteria
const query = encodeURIComponent("peptides doctor female");
const url = `https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=${query}&type=channel&maxResults=50&key=${API_KEY}`;

https.get(url, (resp) => {
  let data = '';
  resp.on('data', (chunk) => { data += chunk; });
  resp.on('end', () => {
    try {
      const result = JSON.parse(data);
      const channelIds = result.items.map(item => item.id.channelId);
      
      // Now get stats for these channels to find the one with ~26 videos
      if (channelIds.length > 0) {
          const statsUrl = `https://youtube.googleapis.com/youtube/v3/channels?part=statistics,snippet&id=${channelIds.join(',')}&key=${API_KEY}`;
          https.get(statsUrl, (res2) => {
              let data2 = '';
              res2.on('data', (c) => { data2 += c; });
              res2.on('end', () => {
                  const statsObj = JSON.parse(data2);
                  statsObj.items.forEach(ch => {
                      // Look for channels with less than 100 videos, ideally around 26
                      if (ch.statistics.videoCount > 5 && ch.statistics.videoCount < 60) {
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

const https = require('https');

const API_KEY = 'AIzaSyD-a49LpvfBhcFar4jc4C99oN_uIMeOGgQ';
const videoId = 'FsJYOdiDPno';

const url = `https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=${videoId}&key=${API_KEY}`;

https.get(url, (resp) => {
  let data = '';
  resp.on('data', (chunk) => { data += chunk; });
  resp.on('end', () => {
    try {
      const result = JSON.parse(data);
      if (result.items && result.items.length > 0) {
          const video = result.items[0];
          console.log(`Video Title: ${video.snippet.title}`);
          console.log(`Channel Title: ${video.snippet.channelTitle}`);
          console.log(`Views: ${video.statistics.viewCount}`);
          console.log(`Likes: ${video.statistics.likeCount}`);
          console.log(`Tags: ${video.snippet.tags ? video.snippet.tags.join(', ') : 'None'}`);
      }
    } catch(e) {
        console.log("Error parsing: " + e);
    }
  });
}).on("error", (err) => {
  console.log("Error: " + err.message);
});

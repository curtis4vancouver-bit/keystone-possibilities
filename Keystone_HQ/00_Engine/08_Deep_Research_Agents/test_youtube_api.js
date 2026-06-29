const https = require('https');

const API_KEY = 'AIzaSyD-a49LpvfBhcFar4jc4C99oN_uIMeOGgQ';
const url = `https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=Keystone&type=channel&key=${API_KEY}`;

https.get(url, (resp) => {
  let data = '';
  resp.on('data', (chunk) => {
    data += chunk;
  });
  resp.on('end', () => {
    console.log("RESPONSE FROM YOUTUBE:");
    console.log(data);
  });
}).on("error", (err) => {
  console.log("Error: " + err.message);
});

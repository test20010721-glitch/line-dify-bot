import express from 'express';
import bodyParser from 'body-parser';
import axios from 'axios';

const app = express();
app.use(bodyParser.json());

const LINE_CHANNEL_ACCESS_TOKEN = 'lTkej/6zspK9S66UptgB7URrQ9s+3ttH24rSNXWjhStLaoF0YwzfmT9EQWWpvPUXx9+0CimB+s7r1H/fszbG44ygtQFN5HDhFdh1nX1yyCHKpcQ+3HfhsGzxeHlIzD5gzHEBFzoUCHfFY/jFrSsoVwdB04t89/1O/w1cDnyilFU=';

app.post('/callback', async (req, res) => {
  const events = req.body.events;
  for (let event of events) {
    if (event.type === 'message' && event.message.type === 'text') {
      try {
        // 受け取ったメッセージをそのまま返信
        await axios.post('https://api.line.me/v2/bot/message/reply', {
          replyToken: event.replyToken,
          messages: [{ type: 'text', text: '受信しました！: ' + event.message.text }]
        }, {
          headers: {
            'Authorization': `Bearer ${LINE_CHANNEL_ACCESS_TOKEN}`,
            'Content-Type': 'application/json'
          }
        });
      } catch (err) {
        console.error('LINE返信エラー:', err.response?.data || err.message);
      }
    }
  }
  res.sendStatus(200);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

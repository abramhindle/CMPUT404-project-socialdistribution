import 'dotenv/config';
import express from 'express';
import path from 'path';

const app = express();

app.use(express.static(path.join(__dirname, '../build')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../build/index.html'));
});

app.listen(process.env.API_PORT, () => {
  console.log('Your app is listening on port ' + process.env.API_PORT);
});

import 'dotenv/config';
import express from 'express';
import path from 'path';

const app = express();

app.use(express.static(path.join(__dirname, '../build')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../build/index.html'));
});

app.listen(3001, () => {
  console.log('Your app is listening on port ' + 3001);
});

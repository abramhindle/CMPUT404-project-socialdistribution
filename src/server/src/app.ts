import 'dotenv/config';
import express from 'express';
import path from 'path';

const app = express();
const PORT = process.env.PORT || process.env.API_PORT || 3001;

if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, '../build')));

  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../build/index.html'));
  });
}

app.listen(PORT, () => {
  console.log('Your app is listening on port ' + PORT);
});

export default app;

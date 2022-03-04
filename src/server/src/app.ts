import 'dotenv/config';
import express, { Request, Response } from 'express';
import cors from 'cors';
import path from 'path';
import db from './db';

import { authenticate, requiredLoggedIn } from './middlewares/auth.middlewares';

import auth from './routes/auth.routes';
import author from './routes/author.routes';

if (!process.env.JWT_SECRET) {
  throw new Error('JWT_SECRET environment variable is not set');
}

const app = express();
const PORT = process.env.PORT || process.env.API_PORT || 3001;

app.use(cors());

app.use(express.json());
app.use(authenticate);

// app.get('/auth-optional', (req, res) => {
//   if (!req.authorId) {
//     res.send('You are not logged in');
//   } else {
//     res.send(`You are logged in as ${req.authorId}`);
//   }
// });

// app.get('/auth-required', requiredLoggedIn, (req, res) => {
//   res.send(`You are logged in as ${req.authorId}`);
// });

db.sync({ alter: true }).then(() => {
  app.use(auth);
  app.use('/authors', author);

  if (process.env.NODE_ENV === 'production') {
    app.use(express.static(path.join(__dirname, '../build')));
  }

  app.all('*', (req: Request, res: Response) => {
    res.status(401);
  });

  if (process.env.NODE_ENV !== 'test') {
    app.listen(PORT, () => {
      console.log('Your app is listening on port ' + PORT);
    });
  }
});

export default app;

import "dotenv/config";
import express from "express";
import path from "path";
import db from "./db";
import { authenticate, authRoutes, requiredLoggedIn } from "./auth";

const app = express();
const PORT = process.env.PORT || process.env.API_PORT || 3001;

app.use(express.json());
app.use(authenticate);

app.use(authRoutes);

app.get("/auth-optional", (req, res) => {
  if (!req.authorId) {
    res.send("You are not logged in");
  } else {
    res.send(`You are logged in as ${req.authorId}`);
  }
});

app.get(
  "/auth-required",
  requiredLoggedIn((req, res) => {
    res.send(`You are logged in as ${req.authorId}`);
  })
);

db.sync({ alter: true }).then(() => {
  if (process.env.NODE_ENV === 'production') {
    app.use(express.static(path.join(__dirname, '../build')));

    app.get('*', (req, res) => {
      res.sendFile(path.join(__dirname, '../build/index.html'));
    });
  }

  if (process.env.NODE_ENV !== 'test') {
    app.listen(PORT, () => {
      console.log('Your app is listening on port ' + PORT);
    });
  }
});

export default app;

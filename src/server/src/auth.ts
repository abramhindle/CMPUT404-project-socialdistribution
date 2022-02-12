import express, { RequestHandler, Response, Router } from "express";
import jwt from "jsonwebtoken";
import { JTDDataType } from "ajv/dist/jtd";
import Author from "./models/Author";
import Ajv from "ajv/dist/jtd";
import argon2 from "argon2";

if (!process.env.JWT_SECRET) {
  throw new Error("JWT_SECRET environment variable is not set");
}

const ajv = new Ajv();

/**
 * Adds `authorId` to the request based on the request Authorization header.
 */
export const authenticate: RequestHandler = (req, res, next) => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(" ")[1];
  if (token) {
    jwt.verify(token, process.env.JWT_SECRET, (err, payload: JwtPayload) => {
      if (!err && payload) {
        req.authorId = payload.authorId;
      }
    });
  }
  next();
};

/**
 * Requires an author to be logged in.
 *
 * If the author is logged in, the request is handled with `handler`.
 * Otherwise, an HTTP 400 response is sent.
 *
 * @param handler the handler to use if the request is authenticated
 */
export const requiredLoggedIn: (
  handler: AuthenticatedRequestHandler
) => RequestHandler = (handler) => (req, res, next) => {
  if (!req.authorId) {
    unauthorized(res);
    return;
  }
  handler(req as AuthenticatedRequest, res, next);
};

export const authRoutes = Router();

/**
 * Registers a new author.
 */
authRoutes.post("/register", async (req, res) => {
  const schema = {
    properties: {
      email: { type: "string" },
      password: { type: "string" },
      displayName: { type: "string" },
    },
  } as const;
  const validate = ajv.compile<JTDDataType<typeof schema>>(schema);
  if (!validate(req.body)) {
    res.status(400).json({ error: validate.errors });
    return;
  }

  const { email, password, displayName } = req.body;
  const passwordHash = await argon2.hash(password);

  let author: Author;
  try {
    author = await Author.create({
      email,
      passwordHash,
      displayName,
    });
  } catch (e) {
    console.error(e);
    res.sendStatus(400);
    return;
  }

  await login(author, password, res);
});

/**
 * Logs into an existing author's account.
 *
 * Responds with a JSON Web Token if successful, and an HTTP 400 otherwise.
 */
authRoutes.post("/login", async (req, res) => {
  const schema = {
    properties: {
      email: { type: "string" },
      password: { type: "string" },
    },
  } as const;
  const validate = ajv.compile<JTDDataType<typeof schema>>(schema);
  if (!validate(req.body)) {
    res.sendStatus(400);
    return;
  }

  const { email, password } = req.body;
  const author = await Author.findOne({
    where: {
      email: email,
    },
  });
  if (author === null) {
    unauthorized(res);
    return;
  }

  await login(author, password, res);
});

const login = async (
  author: Author,
  password: string,
  res: Response
): Promise<void> => {
  const passwordIsCorrect = await argon2.verify(author.passwordHash, password);
  if (!passwordIsCorrect) {
    unauthorized(res);
    return;
  }
  const payload: JwtPayload = { authorId: author.id };
  const token = jwt.sign(payload, process.env.JWT_SECRET);
  res.json(token);
};

const unauthorized = (res: Response): void => {
  res.setHeader("WWW-Authenticate", "Bearer");
  res.sendStatus(401);
};

type AuthenticatedRequest = express.Request & { author: Author };
type AuthenticatedRequestHandler = (
  req: AuthenticatedRequest,
  res: express.Response,
  next: express.NextFunction
) => void;

interface JwtPayload {
  authorId: Author["id"];
}

import { Request, Response } from 'express';
import argon2 from 'argon2';

import Author from '../models/Author';

import { loginUser } from '../handlers/auth.handlers';
import { unauthorized } from '../handlers/auth.handlers';

/**
 * Logs into an existing author's account.
 *
 * Responds with a JSON Web Token and author data if successful,
 * and an HTTP 400 otherwise.
 */
const login = async (req: Request, res: Response) => {
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

  await loginUser(author, password, res);
};

/**
 * Registers a new author.
 */
const register = async (req: Request, res: Response) => {
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
    const errorMessage = e.name === 'SequelizeUniqueConstraintError'
      ? 'A user with that email already exists.'
      : 'An unknown error occurred.';
    res.status(400).json({ error: errorMessage });
    return;
  }

  await loginUser(author, password, res);
};

export { login, register };

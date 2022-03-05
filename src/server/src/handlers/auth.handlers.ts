import { Response } from 'express';
import argon2 from 'argon2';
import jwt from 'jsonwebtoken';
import Author from '../models/Author';
import { JwtPayload } from '../types/auth';

const loginUser = async (
  author: Author,
  password: string,
  res: Response
): Promise<void> => {
  const passwordIsCorrect = await argon2.verify(author.passwordHash, password);
  if (!passwordIsCorrect) {
    unauthorized(res);
    return;
  }
  const payload: JwtPayload = { authorId: author.id.toString() };
  const token = jwt.sign(payload, process.env.JWT_SECRET);
  res.json({ token, author });
};

const unauthorized = (res: Response): void => {
  res.setHeader('WWW-Authenticate', 'Bearer');
  res.status(401).send();
};

export { loginUser, unauthorized };

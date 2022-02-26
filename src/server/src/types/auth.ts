import express from 'express';
import { v4 } from 'uuid';
import Author from '../models/Author';

type AuthenticatedRequest = express.Request & { author: Author } & {
  authorId?: typeof v4;
};
type AuthenticatedRequestHandler = (
  req: AuthenticatedRequest,
  res: express.Response,
  next: express.NextFunction
) => void;

interface JwtPayload {
  authorId: Author['id'];
}

export { AuthenticatedRequest, AuthenticatedRequestHandler, JwtPayload };

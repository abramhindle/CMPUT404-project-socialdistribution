import { RequestHandler } from 'express';
import jwt from 'jsonwebtoken';
import { unauthorized } from '../handlers/auth.handlers';
import { AuthenticatedRequest, JwtPayload } from '../types/auth';

/**
 * Adds `authorId` to the request based on the request Authorization header.
 */
const authenticate: RequestHandler = (req: AuthenticatedRequest, res, next) => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(' ')[1];
  if (token) {
    jwt.verify(token, process.env.JWT_SECRET, (err, payload: JwtPayload) => {
      if (!err && payload) {
        req.authorId = payload.authorId;
      } else {
        unauthorized(res);
        return;
      }
    });
  }
  next();
};

/**
 * Requires an author to be logged in.
 *
 * If the author is logged in, the request is passed on.
 * Otherwise, an HTTP 400 response is sent.
 *
 * @param handler the handler to use if the request is authenticated
 */

const requiredLoggedIn: RequestHandler = (
  req: AuthenticatedRequest,
  res,
  next
) => {
  if (!req.authorId) {
    unauthorized(res);
    return;
  }
  next();
};

export { authenticate, requiredLoggedIn };

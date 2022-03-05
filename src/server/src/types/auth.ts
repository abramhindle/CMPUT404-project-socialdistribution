import express from 'express';

type AuthenticatedRequest = express.Request & {
  authorId: string;
};

type AuthenticatedRequestHandler = (
  req: AuthenticatedRequest,
  res: express.Response,
  next: express.NextFunction
) => void;

interface JwtPayload {
  authorId: string;
}

export { AuthenticatedRequest, AuthenticatedRequestHandler, JwtPayload };

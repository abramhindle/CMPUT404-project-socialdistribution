import { Request } from 'express';

type PaginationRequest = Request & {
  offset: number;
  limit: number;
};

export { PaginationRequest };

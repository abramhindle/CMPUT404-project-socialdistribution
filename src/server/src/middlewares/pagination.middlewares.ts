import { NextFunction, Response } from 'express';
import { PaginationRequest } from '../types/pagination';

const paginate = (
  req: PaginationRequest,
  res: Response,
  next: NextFunction
) => {
  if (req.query.page && req.query.size) {
    if (
      isNaN(parseInt(req.query.page.toString())) ||
      isNaN(parseInt(req.query.size.toString()))
    ) {
      res
        .status(400)
        .send({ error: 'Parameter page and size must be an integer' });
      return;
    }
    req.limit = parseInt(req.query.size.toString());
    req.offset = (parseInt(req.query.page.toString()) - 1) * req.limit;
    next();
    return;
  }
  res.status(400).send({
    error: 'This request must be paginated using the parameter page and size',
  });
};

export { paginate };

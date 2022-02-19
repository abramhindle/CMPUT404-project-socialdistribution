import { body } from 'express-validator';
import express from 'express';
const router = express.Router({ mergeParams: true });

import { paginate } from '../middlewares/pagination.middlewares';
import { validate } from '../middlewares/validator.middlewares';
import { requiredLoggedIn } from '../middlewares/auth.middlewares';

import { createPost, getAuthorPosts } from '../controllers/post.controllers';

router.get('/', paginate, getAuthorPosts);
router.post(
  '/',
  [
    // requiredLoggedIn,
    validate([
      body('title').isString(),
      body('description').isString(),
      body('source').isURL(),
      body('origin').isURL(),
      body('contentType').isIn([
        'text/markdown',
        'text/plain',
        'application/base64',
        'image/png;base64',
        'image/jpeg;base64',
      ]),
      body('content').notEmpty(),
      body('categories.*').isString(),
      body('visibility').isIn(['PUBLIC', 'FRIENDS']),
    ]),
  ],
  createPost
);

export default router;

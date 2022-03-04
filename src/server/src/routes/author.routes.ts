import { body, param } from 'express-validator';
import express from 'express';
const router = express.Router();

import { requiredLoggedIn } from '../middlewares/auth.middlewares';
import { paginate } from '../middlewares/pagination.middlewares';
import { validate } from '../middlewares/validator.middlewares';

import posts from './post.routes';

import {
  getAllAuthors,
  getAuthor,
  getCurrentAuthor,
  updateProfile,
} from '../controllers/author.controllers';

router.use('/:id/posts', posts);

router.get('/', paginate, getAllAuthors);
router.get('/me', requiredLoggedIn, getCurrentAuthor);
router.get('/:id', validate([param('id').isUUID()]), getAuthor);
router.post(
  '/:id',
  validate([
    param('id').isUUID(),
    body('email').isEmail().optional(),
    body('displayName').isString().optional(),
    body('github').isURL().optional(),
    body('profileImage').isURL().optional(),
  ]),
  updateProfile
);

export default router;

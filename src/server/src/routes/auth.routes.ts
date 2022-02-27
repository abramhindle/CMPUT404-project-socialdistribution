import { body } from 'express-validator';
import express from 'express';
const router = express.Router();

import { validate } from '../middlewares/validator.middlewares';

import { login, register } from '../controllers/auth.controllers';

router.post(
  '/login',
  validate([body('email').isEmail(), body('password').isString()]),
  login
);
router.post(
  '/register',
  validate([
    body('email').isEmail(),
    body('password').isString(),
    body('displayName').isString(),
  ]),
  register
);

export default router;

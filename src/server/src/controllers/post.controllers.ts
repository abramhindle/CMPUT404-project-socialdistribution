import { Request, Response } from 'express';
import Author from '../models/Author';
import Post from '../models/Post';
import { PaginationRequest } from '../types/pagination';

const createPost = async (req: Request, res: Response) => {
  const {
    title,
    description,
    source,
    origin,
    contentType,
    content,
    categories,
    visibility,
  } = req.body;
  const author = await Author.findOne({
    where: {
      id: req.params.id,
    },
  });
  if (author === null) {
    res.sendStatus(404);
    return;
  }
  try {
    const post = await Post.create({
      title: title,
      description: description,
      source: source,
      origin: origin,
      contentType: contentType,
      content: content,
      categories: categories,
      visibility: visibility,
    });
    author.addPost(post);
  } catch (error) {
    res.status(500).send(error);
    return;
  }

  res.sendStatus(200);
};

const getAuthorPosts = async (req: PaginationRequest, res: Response) => {
  const posts = await Post.findAll({
    where: {
      author_id: req.params.id,
    },
    include: {
      model: Author,
      as: 'author',
    },
    offset: req.offset,
    limit: req.limit,
  });
  res.send(posts);
};

export { createPost, getAuthorPosts };

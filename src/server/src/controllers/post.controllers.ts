import { Request, Response } from 'express';
import Author from '../models/Author';
import Post from '../models/Post';
import { AuthenticatedRequest } from '../types/auth';
import { PaginationRequest } from '../types/pagination';

const createPost = async (req: AuthenticatedRequest, res: Response) => {
  const post_exists = await Post.findOne({ where: { id: req.params.post_id } });
  if (post_exists !== null) {
    res.status(400).send({ error: 'Post already exists' });
    return;
  }
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
    res.status(404).send();
    return;
  }
  try {
    const post = await Post.create({
      ...(req.params.id && { id: req.params.post_id }),
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
    res.status(500).send({ error: error });
    return;
  }

  res.status(200).send();
};

const deleteAuthorPost = async (req: AuthenticatedRequest, res: Response) => {
  const post = await Post.findOne({
    where: { id: req.params.post_id, author_id: req.params.id },
    include: { model: Author, as: 'author' },
  });
  if (post === null) {
    res.status(404).send();
    return;
  }
  try {
    await post.destroy();
  } catch (error) {
    console.error(error);
    res.status(500).send({ error: error });
    return;
  }
  res.status(200).send();
};

const getAuthorPost = async (req: Request, res: Response) => {
  const post = await Post.findOne({
    attributes: [
      'id',
      'title',
      'source',
      'origin',
      'description',
      'contentType',
      'content',
      'categories',
      'count',
      'published',
      'visibility',
      'unlisted',
    ],
    where: {
      id: req.params.post_id,
      author_id: req.params.id,
    },
    include: {
      model: Author,
      attributes: ['id', 'displayName', 'github', 'profileImage'],
      as: 'author',
    },
  });
  if (post === null) {
    res.status(404).send();
    return;
  }
  res.send({
    type: 'post',
    ...post.toJSON(),
    author: { type: 'author', ...post.toJSON().author },
  });
};

const getAuthorPosts = async (req: PaginationRequest, res: Response) => {
  const posts = await Post.findAll({
    attributes: [
      'id',
      'title',
      'source',
      'origin',
      'description',
      'contentType',
      'content',
      'categories',
      'count',
      'published',
      'visibility',
      'unlisted',
    ],
    where: {
      author_id: req.params.id,
    },
    include: {
      model: Author,
      attributes: ['id', 'displayName', 'github', 'profileImage'],
      as: 'author',
    },
    offset: req.offset,
    limit: req.limit,
  });
  res.send({
    type: 'posts',
    items: posts.map((post) => {
      return {
        type: 'post',
        ...post.toJSON(),
        author: { type: 'author', ...post.toJSON().author },
      };
    }),
  });
};

const updateAuthorPost = async (req: AuthenticatedRequest, res: Response) => {
  const post = await Post.findOne({
    where: { id: req.params.post_id, author_id: req.params.id },
  });
  if (post === null) {
    res.status(404).send();
    return;
  }
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

  try {
    await post.update({
      ...(title && { title: title }),
      ...(description && { description: description }),
      ...(source && { source: source }),
      ...(origin && { origin: origin }),
      ...(contentType && { contentType: contentType }),
      ...(content && { content: content }),
      ...(categories && { categories: categories }),
      ...(visibility && { visibility: visibility }),
    });
  } catch (error) {
    console.error(error);
    res.status(500).send({ error: error });
    return;
  }
  res.status(200).send();
};

export {
  createPost,
  deleteAuthorPost,
  getAuthorPost,
  getAuthorPosts,
  updateAuthorPost,
};

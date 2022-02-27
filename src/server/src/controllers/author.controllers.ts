import { Request, Response } from 'express';
import Author from '../models/Author';
import { PaginationRequest } from '../types/pagination';

const getAllAuthors = async (req: PaginationRequest, res: Response) => {
  const authors = await Author.findAll({
    attributes: ['id', 'displayName', 'github', 'profileImage'],
    offset: req.offset,
    limit: req.limit,
  });
  res.send({
    type: 'authors',
    items: authors.map((author) => {
      return { type: 'author', ...author.toJSON() };
    }),
  });
};

const getAuthor = async (req: Request, res: Response) => {
  const author = await Author.findOne({
    attributes: ['id', 'displayName', 'github', 'profileImage'],
    where: { id: req.params.id },
  });
  if (author === null) {
    res.sendStatus(404);
    return;
  }
  res.send({ type: 'author', ...author.toJSON() });
};

const updateProfile = async (req: Request, res: Response) => {
  const { email, displayName, github, profileImage } = req.body;
  const author = await Author.findOne({ where: { id: req.params.id } });
  if (author === null) {
    res.sendStatus(404);
    return;
  }

  try {
    await author.update({
      ...(email && { email: email }),
      ...(displayName && { displayName: displayName }),
      ...(github && { github: github }),
      ...(profileImage && { profileImage: profileImage }),
    });
  } catch (error) {
    console.error(error);
    res.status(500).send(error);
    return;
  }
  res.sendStatus(200);
};

export { getAllAuthors, getAuthor, updateProfile };

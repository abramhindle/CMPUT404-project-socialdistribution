import axios from "axios";
const baseUrl = "";

// gets all posts
const getAll = async () => {};
// gets one user's posts
const getUser = async (user) => {};
const create = async (newPost, token) => {};
const update = async (updatedPost, token) => {};
const remove = async (post, token) => {};

const postService = {
  getAll, getUser, create, update, remove
};

export default postService;
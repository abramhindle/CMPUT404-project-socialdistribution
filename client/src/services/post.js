import axios from "axios";
const baseUrl = "/service/author";

// gets one user's posts
const getPosts = async (authorId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/posts`);
  return response;
};

// creates post by author with
//    contentType: {text/markdown, text/plain, application/base64, image/png;base64, image/jpeg;base64}
//    content
//    title
//    categories
const createPost = async (csrfToken, authorId, {contentType, content, title, categories}) => {
  const response = await axios.post(`${baseUrl}/${authorId}/posts`, {
      contentType,
      content,
      title,
      categories,
    },
    { withCredentials: true, headers: {"X-CSRFToken": csrfToken }}
  );
  return response;
};

// update post with id postId with correctly formatted post passed as post argument
const updatePost = async (csrfToken, authorId, postId, post) => {
  const response = await axios.post(`${baseUrl}/${authorId}/posts/${postId}`, 
    { post }, 
    { withCredentials: true, headers: {"X-CSRFToken": csrfToken }});
  return response;
};

// remove post with id postId 
const removePost = async (csrfToken, authorId, postId) => {
  const response = await axios.delete(`${baseUrl}/${authorId}/posts/${postId}`, 
    {},
    { withCredentials: true, headers: {"X-CSRFToken": csrfToken }}
  );
  return response;
};

const getLikes = async (authorId, postId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/post/${postId}/likes`);
  return response;
};

const getCommentLikes = async (authorId, postId, commentId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/post/${postId}/comments/${commentId}/likes`);
  return response;
};

// create comment for post with postId where comment has fields
//    contentType: { text/markdown, text/plain }
//    comment
const createComment = async (csrfToken, authorId, postId, { contentType, comment } ) => {
  const response = await axios.post(`${baseUrl}/${authorId}/posts/${postId}`, { 
      contentType, 
      comment
    }, 
    { withCredentials: true, headers: {"X-CSRFToken": csrfToken }});
  return response;
}

const getAllComments = async (authorId, postId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/posts/${postId}`);
  return response;
};

const getComments = async (authorId, postId, page, size) => {
  const params = new URLSearchParams(page);
  params.append(size);

  const response = await axios.get(`${baseUrl}/${authorId}/posts/${postId}`, params);
  return response;
};

const postService = {
  getPosts, 
  createPost, 
  updatePost, 
  removePost, 
  getComments, 
  getAllComments,
  createComment,
  getLikes,
  getCommentLikes,
};

export default postService;
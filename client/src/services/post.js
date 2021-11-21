import axios from "axios";
const baseUrl = "/service/author";

// gets single post
const getPost = async (csrfToken, authorId, postId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/posts/${postId}`,
    { withCredentials: true, headers: { "X-CSRFToken": csrfToken } });
  return response;
}

const getRemotePost = async () => {

}

const getPosts = async (csrfToken, authorId, page=1, size=5) => {
  const response = await axios.get(`${baseUrl}/${authorId}/posts?page=${page}&size=${size}`,
    { withCredentials: true, headers: { "X-CSRFToken": csrfToken } });
  return response;
};

const getRemotePosts = async () => {

}

const likePost = async (csrfToken, authorId, {author, object}) => {
  const response = await axios.post(`${baseUrl}/${authorId}/inbox`,
    { summary: `${author.displayName} likes your post`,
      "@context": "https://cmput404-vgt-socialdist.herokuapp.com/",
      type: "Like",
      object,
      author
    },
    { withCredentials: true, headers: { "X-CSRFToken": csrfToken } });
  return response;
};

const likeRemotePost = async (url, authorId, {author, object}) => {
  const response = await axios.post(`${url}/${authorId}/inbox`,
    { summary: `${author.displayName} likes your post`,
      "@context": "https://cmput404-vgt-socialdist.herokuapp.com/",
      type: "Like",
      object,
      author
    },
    { withCredentials: true, auth: { username: "username", password: "password"}});
  return response;
};



// creates post by author with
//    contentType: {text/markdown, text/plain, application/base64, image/png;base64, image/jpeg;base64}
//    content
//    title
//    categories
const createPost = async (csrfToken, authorId, postData) => {
  console.log(postData)
  const response = await axios.post(`${baseUrl}/${authorId}/posts/`, postData,
    { withCredentials: true, headers: {"X-CSRFToken": csrfToken }}
  );
  return response;
};

// update post with id postId with correctly formatted post passed as post argument
const updatePost = async (csrfToken, authorId, postId, post) => {
  console.log(post)
  const response = await axios.post(`${baseUrl}/${authorId}/posts/${postId}`,
    { ...post },
    { withCredentials: true, headers: {"X-CSRFToken": csrfToken }});
  return response;
};

// remove post with id postId
const removePost = async (csrfToken, authorId, postId) => {
  const response = await axios.delete(`${baseUrl}/${authorId}/posts/${postId}`,
    { withCredentials: true, headers: {"X-CSRFToken": csrfToken }}
  );
  return response;
};

const getLikes = async (authorId, postId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/post/${postId}/likes`);
  return response;
};

const getRemoteLikes = async () => {

}

const getCommentLikes = async (authorId, postId, commentId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/post/${postId}/comments/${commentId}/likes`);
  return response;
};

const getRemoteCommentLikes = async () => {

}

const likeComment = async (csrfToken, authorId, { author, object }) => {
  const response = await axios.post(`${baseUrl}/${authorId}/inbox`,
    { summary: `${author.displayName} likes your comment`,
      "@context": "https://cmput404-vgt-socialdist.herokuapp.com/",
      type: "Like",
      object,
      author
    },
    { withCredentials: true, headers: { "X-CSRFToken": csrfToken } });
  return response;

};

// create comment for post with postId where comment has fields
//    contentType: { text/markdown, text/plain }
//    comment
const createComment = async (csrfToken, authorId, postId, { contentType, comment, author } ) => {
  const response = await axios.post(`${baseUrl}/${authorId}/posts/${postId}/comments`, {
      type: "comment",
      contentType,
      comment,
      id: null,
      published: null,
      author
    },
    { withCredentials: true, headers: {"X-CSRFToken": csrfToken }});
  return response;
}

const getRemoteComment = async () => {

}

const getComments = async (csrfToken, authorId, postId, page=1, size=5) => {
  const response = await axios.get(`${baseUrl}/${authorId}/posts/${postId}/comments?page=${page}&size=${size}`,
    { withCredentials: true, headers: { "X-CSRFToken": csrfToken } });
  return response;
};

const getRemoteComments = async () => {

}

const getPostFeed = async (csrfToken, page = 1, size = 5) => {
  const response = await axios.get(
    `service/internal/feed?page=${page}&size=${size}`,
    { withCredentials: true, headers: { "X-CSRFToken": csrfToken } });
  return response
}

const postService = {
  getPosts,
  getPost,
  createPost,
  updatePost,
  removePost,
  getComments,
  createComment,
  getLikes,
  getCommentLikes,
  likePost,
  likeComment,
  getPostFeed
};

export default postService;
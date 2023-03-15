import axios from "axios";

export const post_like = async (
  likedAuthorId,
  likeAuthor,
  postId,
  context,
  success
) => {
  console.log("Attempting to post likes for", { postId });
  const data = {
    type: "Like",
    context: context,
    author: likeAuthor,
    object: `http://localhost:8000/authors/${likedAuthorId
      .split("/")
      .pop()}/posts/${postId.split("/").pop()}`,
  };
  const res = await axios.post(
    `http://localhost:8000/authors/${likedAuthorId}/inbox/`,
    data,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    }
  );
  console.log(res);
  if (res.status === 202) {
    console.log("Success!");
    success(res.data);
  } else {
    console.log("Error Occured");
  }
};

export const comment_like = async (
  likedAuthorId,
  likeAuthor,
  postId,
  commentId,
  context,
  success
) => {
  console.log("Attempting to post likes for", { commentId });
  const data = {
    type: "Like",
    context: context,
    author: likeAuthor,
    object: `http://localhost:8000/authors/${likedAuthorId
      .split("/")
      .pop()}/posts/${postId.split("/").pop()}/comments/${commentId
      .split("/")
      .pop()}`,
  };
  const res = await axios.post(
    `http://localhost:8000/authors/${likedAuthorId}/inbox/`,
    data,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    }
  );
  console.log(res);
  if (res.status === 202) {
    console.log("Success!");
    success(res.data);
  } else {
    console.log("Error Occured");
  }
};

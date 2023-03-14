export const get_post_like = async (authorId, postId, success) => {
  console.log("Attempting to get likes for", { postId });

  const res = await axios.get(
    `http://localhost:8000/authors/${authorId}/posts/${postId}/likes/`,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    }
  );
  console.log(res);
  if (res.status === 200) {
    console.log("Success!");
    success(res.data);
  } else {
    console.log("Error Occured");
  }
};

export const get_comment_like = async (
  authorId,
  postId,
  commentId,
  success
) => {
  console.log("Attempting to get likes for", { commentId });

  const res = await axios.get(
    `http://localhost:8000/authors/${authorId}/posts/${postId}/comments/${commentId}/likes/`,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    }
  );
  console.log(res);
  if (res.status === 200) {
    console.log("Success!");
    success(res.data);
  } else {
    console.log("Error Occured");
  }
};

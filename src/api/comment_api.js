import axios from "axios";

import { post_inbox } from "../api/inbox_api";

export const post_comment = async (
  postAuthorId,
  postId,
  type,
  comment,
  commentAuthorId
) => {
  console.log("Attempting to post a comment for", { postId });
  const data = { contentType: type, comment: comment };

  const res = await axios.post(
    `authors/${commentAuthorId}/posts/${postId}/comments/`,
    data,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    }
  );
  console.log(res);
  if (res.status === 201) {
    post_inbox(postAuthorId, res.data);
    console.log("Success!");
  } else {
    console.log("Error Occured");
  }
};

export const get_post_comments = async (
  authorId,
  postId,
  success,
  page,
  size
) => {
  console.log("Attempting to get comments for", { postId });

  const res = await axios.get(
    `authors/${authorId}/posts/${postId}/comments/?page=${page}&size=${size}`,
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

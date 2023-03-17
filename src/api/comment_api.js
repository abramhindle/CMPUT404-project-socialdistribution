import axios from "axios";

import { post_inbox } from "../api/inbox_api";

export const post_comment = async (
  postAuthorId,
  postId,
  type,
  comment,
  commentAuthorId
) => {
  console.log("Attempting to post comment for", { postId });
  const data = { contentType: type, comment: comment };

  const res = await axios.post(
    `http://localhost:8000/authors/${commentAuthorId}/posts/${postId}/comments/`,
    data,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    }
  );
  console.log(res);
  if (res.status == 201) {
    post_inbox(postAuthorId, res.data);
    console.log("Success!");
  } else {
    console.log("Error Occured");
  }
};

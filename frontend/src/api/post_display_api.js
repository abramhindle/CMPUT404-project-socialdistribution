import axios from "axios";
import { get_followers_for_author } from "./follower_api";

let head = {
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
};

export const post_api = async (authorId, post, successPost, successFollow) => {
  await axios
    .post(`http://localhost:8000/authors/${authorId}/posts/`, post, head)
    .then(function (response) {
      console.log("Post res: ", response["data"]);
      successPost(response["data"]);
      get_followers_for_author(authorId, successFollow);
    })
    .catch(function (error) {
      console.log(error);
    });
};

export const send_api = async (followers, data) => {
  console.log("Sending to api . . .", followers.items);
  for (var user in followers.items) {
    console.log("sending ", data, " to ", followers.items[user]["id"]);
    await axios
      .post(
        `http://localhost:8000/authors/${followers.items[user]["id"]}/inbox/`,
        data,
        head
      )
      .catch(function (error) {
        console.log(error, "occured while sending a post");
      });
  }
};

export const get_author_posts = async (authorId, page, success) => {
  console.log("Attempting to retrieve author info for", { authorId });
  await axios
    .get(`http://localhost:8000/authors/${authorId}/posts/?page=${page}`, {
      headers: {
        Accept: "application/json",
      },
    })
    .then(function (response) {
      console.log("Author_api res: ", response);
      success(response.data);
    })
    .catch(function (error) {
      console.log(error);
    });
};

export const get_inbox_posts = async (authorInbox, page, success) => {
  console.log("Attempting to retrieve inbox info for", { authorInbox });
  await axios
    .get(`http://localhost:8000/authors/${authorInbox}?page=${page}`, {
      headers: {
        Accept: "application/json",
      },
    })
    .then(function (response) {
      console.log("get_inbox_posts res: ", response.data);
      success(response.data);
    })
    .catch(function (error) {
      console.log(error);
    });
};

export const get_post = async (authorId, postId, success) => {
  console.log("Attempting to get post", { postId });

  await axios
    .get(`http://localhost:8000/authors/${authorId}/posts/${postId}`, {
      headers: {
        Accept: "application/json",
      },
    })
    .then(function (response) {
      console.log("Success");
      success(response.data);
    })
    .catch(function (error) {
      console.log(error);
    });
};

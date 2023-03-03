import axios from "axios";

export const post_api = async (authorId, post, success, failure) => {
  await axios
    .post(`http://localhost:8000/authors/${authorId}/posts/`, post, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    })
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
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

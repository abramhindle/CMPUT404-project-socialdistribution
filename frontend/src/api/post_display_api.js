import axios from "axios";

let head = { headers: {
  Accept: "application/json",
  "Content-Type": "application/json",
},};

export const post_api = async (authorId, post, success, failure) => {
  await axios
    .post(`http://localhost:8000/authors/${authorId}/posts/`, post, head)
    .then(function (response) {
      console.log(response);
      return response;
    })
    .catch(function (error) {
      console.log(error);
    });

};

export const send_api = async (followers, data) => {
  for (var user in followers) {
    console.log("sending to ", user);
    await axios.post(`http://localhost:8000/authors/${user}/inbox`, data, head)
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
  console.log("Attempting to retrieve inbox info for", {authorInbox});
  await axios.get(`http://localhost:8000/authors/${authorInbox}?page=${page}`,
  {
    headers: {
      Accept: "application/json"
    }
  }).then(function (response) {
    console.log("Author_api res: ", response);
    success(response.data);
  })
  .catch(function (error) {
    console.log(error);
  });
};
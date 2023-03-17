import axios from "axios";

export const get_followers_for_author = async (authorId, success) => {
  console.log("Attempting to retrieve follower list for", { authorId });
  await axios
    .get(`http://localhost:8000/authors/${authorId}/followers/`, {
      headers: {
        Accept: "application/json",
      },
    })
    .then(function (response) {
      console.log("Followerlist res: ", response["data"]["items"]);
      success({ items: response["data"]["items"] });
    })
    .catch(function (error) {
      console.log(error);
    });
};

export const add_followers_for_author = async (authorId, followId, success) => {
  console.log("Adding follower", { followId });
  await axios
    .put(`http://localhost:8000/authors/${authorId}/followers/${followId}`, {
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

import axios from "axios";

export const get_followers_for_author = async (authorId, success) => {
    console.log("Attempting to retrieve follower list for", {authorId});
    await axios.get(`http://localhost:8000/authors/${authorId}/followers/`,
    {
      headers: {
        Accept: "application/json"
      }
    }).then(function (response) {
      console.log("Followerlist res: ", response["data"]["items"]);
      success(response["data"]["items"]);

    })
    .catch(function (error) {
      console.log(error);
    });
  };
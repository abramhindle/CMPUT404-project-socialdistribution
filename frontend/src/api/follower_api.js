import axios from "axios";

export const get_followers_for_author = async (authorId, success) => {
    console.log("Attempting to retrieve author info for", {authorId});
    await axios.get(`http://localhost:8000/authors/${authorId}/followers/`,
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
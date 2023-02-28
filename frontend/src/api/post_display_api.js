import axios from "axios";

export const post_api = async (authorId, post, success, failure) => {
    await axios.post(
      `http://localhost:8000/authors/${authorId}/posts/`, 
      post, 
      {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        }
      }
    ).then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });

    /*if (res.status === 200) {
      console.log("successfully posted");
      success(res);
    } else {
      console.log("failed to post");
      failure(res);
    }*/
  };

export const author_api = async (authorId, success) => {
  console.log("Attempting to retrieve author info for", {authorId});
  await axios.get(`http://localhost:8000/authors/${authorId}`,
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

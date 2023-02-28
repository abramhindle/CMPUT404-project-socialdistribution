import axios from "axios";

export const post_api = async (authorId, post, success, failure) => {
    const res = await axios.post(
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

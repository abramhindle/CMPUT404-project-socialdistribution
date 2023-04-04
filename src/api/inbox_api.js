import axios from "axios";

export const post_inbox = async (authorId, object, return_status) => {
  console.log("Attempting to post", { object }, "to", { authorId });

  try {
    const res = await axios.post(`authors/${authorId}/inbox/`, object, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      withCredentials: true,
    });
    console.log(res);
    console.log("Success!");
    return_status(res.status);
  } catch (err) {
    console.log("Error Occured");
    return_status(err.response.status);
  }
};

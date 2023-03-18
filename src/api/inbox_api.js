import axios from "axios";

export const post_inbox = async (authorId, object, success) => {
  console.log("Attempting to post", { object }, "to", { authorId });

  const res = await axios.post(
    `authors/${authorId}/inbox/`,
    object,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    }
  );
  console.log(res);
  if (res.status == 202) {
    console.log("Success!");
  } else {
    console.log("Error Occured");
  }
};

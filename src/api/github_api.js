import axios from "axios";

export const get_github_activity = async (gitURL) => {
  const res = await axios.get(
    `https://api.github.com/users/${gitURL.split("/").pop()}/events`,
    { withCredentials: false }
  );
  if (res.status == 200) {
    console.log("Git Activity Success", res.data);
  } else {
    console.log("Something Went Wrong");
  }
};

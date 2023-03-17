import axios from "axios";

export const signIn_api = async (username, password, success) => {
  const user = {
    username: username,
    password: password,
  };
  const res = await axios.post(
    "http://localhost:8000/api/signin/",
    user,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    },
    { withCredentials: true }
  );
  if (res.status === 200) {
    console.log("success");
    success(res);
  } else {
    console.log("failed");
  }
};

export const signOut_api = async (success) => {
  const res = await axios.post("http://localhost:8000/api/signout/", {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });
  if (res.status === 200) {
    console.log("success");
    success();
  } else {
    console.log("failed");
  }
};

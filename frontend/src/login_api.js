import axios from "axios";

const login_api = async (username, password, success) => {
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

export default login_api;

import axios from "axios";

const login_api = async (username, password, success, fail) => {
  const user = {
    username: username,
    password: password,
  };
  const response = await axios.post(
    "http://localhost:8000/api/token/",
    user,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    },
    { withCredentials: true }
  );
  console.log(response);
  // const text = await response.data;
  if (response.status === 200) {
    console.log("success");
    success();
  } else {
    console.log("failed");
  }
};

export default login_api;

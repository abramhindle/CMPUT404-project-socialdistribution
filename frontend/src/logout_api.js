import axios from "axios";

const logout_api = async (success) => {
  const res = await axios.post("http://localhost:8000/api/signout/", {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });
  if (res.status === 200) {
    console.log("success");
    sessionStorage.clear("persist:root");
    success();
  } else {
    console.log("failed");
  }
};

export default logout_api;

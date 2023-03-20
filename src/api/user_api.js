import axios from "axios";

//TODO: cite this
function getCookie(name) { //stolen from django docs
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

export const signIn_api = async (username, password, success) => {
  const user = {
    username: username,
    password: password,
  };
  const res = await axios.post(
    "api/signin/",
    user,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    },
  )
  .then(function (res) {
    const csrftoken = getCookie('csrftoken');
    axios.defaults.headers.post["X-CSRFToken"] = csrftoken;
    success(res);
  })
  .catch(function (error) {
    console.log(error);
  });
  // if (res.status === 200) {
  //   console.log("success");
  //   console.log(res.headers["set-cookie"]);
  //   axios.defaults.headers.post["X-CSRF-Token"] = res.data;
  //   success(res);
  // } else {
  //   console.log("failed");
  // }
};

export const signOut_api = async (success) => {
  const res = await axios.post("api/signout/", {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    withCredentials: true
  },
  );
  if (res.status === 200) {
    console.log("success");
    success();
  } else {
    console.log("failed");
  }
};

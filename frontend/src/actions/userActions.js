import axios from "axios";
import {
  USER_REGISTER_FAIL,
  USER_REGISTER_SUCCESS,
  USER_REGISTER_REQUEST,
  USER_LOGOUT,
  USER_LOGIN_REQUEST,
  USER_LOGIN_SUCCESS,
  USER_LOGIN_FAIL,
  USER_DETAIL_SUCCESS,
  USER_DETAIL_FAIL,
  USER_DETAIL_REQUEST,
} from "../constants/userConstants";

export const register =
  (name, display, github = "", password, cPassword, csrftoken) =>
  async (dispatch) => {
    try {
      const form = new FormData();
      form.append("username", name);
      form.append("display_name", display);
      form.append("github_url", github);
      form.append("password1", password);
      form.append("password2", cPassword);

      dispatch({
        type: USER_REGISTER_REQUEST,
      });

      const config = {
        headers: {
          "Content-type": "multipart/form-data",
          "X-CSRFToken": csrftoken,
        },
      };

      const { data } = await axios.post("/api/signup/", form, config);
      dispatch({
        type: USER_REGISTER_SUCCESS,
        payload: data,
      });
    } catch (error) {
      dispatch({
        type: USER_REGISTER_FAIL,
        payload:
          error.response.status == "400"
            ? "Signup Unsuccessful: Please check if information is filled in correctly."
            : error.response && error.response.data.detail
            ? error.response.data.detail
            : error.message,
      });
    }
  };

export const login = (username, password, csrftoken) => async (dispatch) => {
  try {
    const form = new FormData();
    form.append("username", username);
    form.append("password", password);

    dispatch({
      type: USER_LOGIN_REQUEST,
    });

    const config = {
      headers: {
        "Content-type": "application/json",
        "X-CSRFToken": csrftoken,
      },
    };

    const { data } = await axios.post(
      "/api/login/",
      { username: username, password: password },
      config
    );

    dispatch({
      type: USER_LOGIN_SUCCESS,
      payload: data,
    });

    localStorage.setItem("userInfo", JSON.stringify(data));
  } catch (error) {
    dispatch({
      type: USER_LOGIN_FAIL,
      payload:
        error.response.status == "400"
          ? "Login Unsuccessful: Please check if your username or password is correct."
          : error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const getAuthorDetail = (csrftoken) => async (dispatch, getState) => {
  try {
    dispatch({
      type: USER_DETAIL_REQUEST,
    });

    const {
      userLogin: { userInfo },
    } = getState();

    const config = {
      headers: {
        "Content-type": "application/json",
        "X-CSRFToken": csrftoken,
        Authorization: `Token ${userInfo.token}`,
      },
    };

    const { data } = await axios.get(
      `/api/author/${userInfo.author_id}/`,
      config
    );

    dispatch({
      type: USER_DETAIL_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: USER_DETAIL_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const logout = () => async (dispatch) => {
  localStorage.removeItem("userInfo");
  const { data } = await axios.get("/api/logout/");
  console.log(data);
  dispatch({ type: USER_LOGOUT });
};

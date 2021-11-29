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
  USER_DETAIL_EDIT_SUCCESS,
  USER_DETAIL_EDIT_FAIL,
  USER_DETAIL_EDIT_REQUEST,
  USER_DETAIL_EDIT_RESET,
  USER_FRIENDLIST_REQUEST,
  USER_FRIENDLIST_FAIL,
  USER_FRIENDLIST_SUCCESS,
  USER_LIST_FAIL,
  USER_LIST_REQUEST,
  USER_LIST_SUCCESS,
  GET_USER_FOLLOWER_REQUEST,
  GET_USER_FOLLOWER_SUCCESS,
  GET_USER_FOLLOWER_FAIL,
} from "../constants/userConstants";

export const register =
  (name, display, github = "", password, cPassword) =>
  async (dispatch, getState) => {
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

      const {
        userLogin: { userInfo },
      } = getState();

      const config = {
        headers: {
          "Content-type": "multipart/form-data",
          //Authorization: `Token ${userInfo.token}`,
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

export const login = (username, password) => async (dispatch) => {
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

export const getAuthorDetail = () => async (dispatch, getState) => {
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
        Authorization: `Token ${userInfo.token}`,
      },
    };

    console.log("gethere!");
    console.log(userInfo.author_id);
    console.log("start");

    const { data } = await axios.get(
      `/api/author/${userInfo.author_id}/`,
      config
    );
    console.log(data);
    console.log("jx");

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

export const editAuthorDetail =
  (displayname, github) => async (dispatch, getState) => {
    try {
      dispatch({
        type: USER_DETAIL_EDIT_REQUEST,
      });

      const {
        userLogin: { userInfo },
      } = getState();

      const config = {
        headers: {
          "Content-type": "application/json",
          Authorization: `Token ${userInfo.token}`,
        },
      };

      const { data } = await axios.post(
        `/api/author/${userInfo.author_id}/`,
        { displayName: displayname, github: github },
        config
      );

      dispatch({
        type: USER_DETAIL_EDIT_SUCCESS,
        payload: data,
      });
    } catch (error) {
      dispatch({
        type: USER_DETAIL_EDIT_FAIL,
        payload:
          error.response && error.response.data.detail
            ? error.response.data.detail
            : error.message,
      });
    }
  };

export const authorFriendlist = () => async (dispatch, getState) => {
  try {
    dispatch({
      type: USER_FRIENDLIST_REQUEST,
    });

    const {
      userLogin: { userInfo },
    } = getState();

    const config = {
      headers: {
        "Content-type": "application/json",
        Authorization: `Token ${userInfo.token}`,
      },
    };

    const { data } = await axios.get(
      `/api/author/${userInfo.author_id}/friends`,
      config
    );

    dispatch({
      type: USER_FRIENDLIST_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: USER_FRIENDLIST_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const logout = () => async (dispatch, getState) => {
  const {
    userLogin: { userInfo },
  } = getState();
  await axios.get("/api/logout/", {
    headers: { Authorization: `Token ${userInfo.token}` },
  });

  localStorage.removeItem("userInfo");
  dispatch({ type: USER_LOGOUT });
};

export const editReset = () => (dispatch) => {
  dispatch({ type: USER_DETAIL_EDIT_RESET });
};

// get user list
export const getUsers = () => async (dispatch, getState) => {
  try {
    dispatch({
      type: USER_LIST_REQUEST,
    });

    const config = {
      headers: {
        "Content-type": "application/json",
      },
    };

    const { data } = await axios.get(`/api/authors/`, config);

    dispatch({
      type: USER_LIST_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: USER_LIST_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const followingUserCheck =
  (foreign_user_id) => async (dispatch, getState) => {
    try {
      dispatch({
        type: GET_USER_FOLLOWER_REQUEST,
      });

      const {
        userLogin: { userInfo },
      } = getState();

      const config = {
        headers: {
          "Content-type": "application/json",
          Authorization: `Token ${userInfo.token}`,
        },
      };

      const { data } = await axios.get(
        `/api/author/${userInfo.author_id}/followers/${foreign_user_id}`,
        config
      );

      dispatch({
        type: GET_USER_FOLLOWER_SUCCESS,
        payload: data,
      });
    } catch (error) {
      dispatch({
        type: GET_USER_FOLLOWER_FAIL,
        payload:
          error.response && error.response.data.detail
            ? error.response.data.detail
            : error.message,
      });
    }
  };

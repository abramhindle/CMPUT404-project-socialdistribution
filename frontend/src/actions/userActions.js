import axios from "axios";
import {
  USER_REGISTER_FAIL,
  USER_REGISTER_SUCCESS,
  USER_REGISTER_REQUEST,
  USER_LOGOUT,
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

      const { data } = await axios.post("/signup/", form, config);
      dispatch({
        type: USER_REGISTER_SUCCESS,
        payload: data,
      });

      /*
    dispatch({
      type: USER_LOGIN_SUCCESS,
      payload: data,
    });
    */
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

import axios from "axios";
import {
  POST_CREATE_FAIL,
  POST_CREATE_SUCCESS,
  POST_CREATE_REQUEST,
  POST_RESET,
} from "../constants/postConstants";

export const createPost =
  (title, content, contentType, visibility, csrftoken) =>
  async (dispatch, getState) => {
    try {
      dispatch({
        type: POST_CREATE_REQUEST,
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

      const { data } = await axios.post(
        `/api/author/${userInfo.author_id}/posts/`,
        {
          author: userInfo.author_id,
          title: title,
          content: content,
          content_type: contentType,
          visibility: visibility,
        },
        config
      );

      dispatch({
        type: POST_CREATE_SUCCESS,
        payload: data,
      });
    } catch (error) {
      dispatch({
        type: POST_CREATE_FAIL,
        payload:
          error.response && error.response.data.detail
            ? error.response.data.detail
            : error.message,
      });
    }
  };

export const postReset = () => (dispatch) => {
  dispatch({ type: POST_RESET });
};

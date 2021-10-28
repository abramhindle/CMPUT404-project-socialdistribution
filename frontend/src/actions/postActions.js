import axios from "axios";
import {
  POST_CREATE_FAIL,
  POST_CREATE_SUCCESS,
  POST_CREATE_REQUEST,
  POST_RESET,
  POST_LIST_REQUEST,
  POST_LIST_SUCCESS,
  POST_LIST_FAIL,
} from "../constants/postConstants";

export const createPost =
  (title, content, contentType, visibility) => async (dispatch, getState) => {
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

export const getPosts = () => async (dispatch, getState) => {
  try {
    dispatch({
      type: POST_LIST_REQUEST,
    });

    const config = {
      headers: {
        "Content-type": "application/json",
      },
    };

    const { data } = await axios.get(`/api/posts/`, config);

    dispatch({
      type: POST_LIST_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: POST_LIST_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

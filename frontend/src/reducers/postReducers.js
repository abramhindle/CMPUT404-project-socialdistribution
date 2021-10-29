import {
  POST_CREATE_FAIL,
  POST_CREATE_SUCCESS,
  POST_CREATE_REQUEST,
  POST_LIST_REQUEST,
  POST_LIST_SUCCESS,
  POST_LIST_FAIL,
  POST_RESET,
  WRITE_COMMENT_FAIL,
  WRITE_COMMENT_REQUEST,
  WRITE_COMMENT_SUCCESS,
} from "../constants/postConstants";

export const postCreateReducer = (state = {}, action) => {
  switch (action.type) {
    case POST_CREATE_REQUEST:
      return { loading: true };

    case POST_CREATE_SUCCESS:
      return { loading: false, success: true, post: action.payload };

    case POST_CREATE_FAIL:
      return { loading: false, error: action.payload };

    case POST_RESET:
      return {};

    default:
      return state;
  }
};

export const postListReducer = (state = {}, action) => {
  switch (action.type) {
    case POST_LIST_REQUEST:
      return { loading: true };

    case POST_LIST_SUCCESS:
      return { loading: false, post: action.payload };

    case POST_LIST_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const writeCommentReducer = (state = {}, action) => {
  switch (action.type) {
    case WRITE_COMMENT_REQUEST:
      return { loading: true };

    case WRITE_COMMENT_SUCCESS:
      return { loading: false, response: action.payload };

    case WRITE_COMMENT_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

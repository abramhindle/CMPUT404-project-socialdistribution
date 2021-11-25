import {
  POST_CREATE_FAIL,
  POST_CREATE_SUCCESS,
  POST_CREATE_REQUEST,
  POST_LIST_REQUEST,
  POST_LIST_SUCCESS,
  POST_LIST_FAIL,
  POST_RESET,
  POST_DELETE_REQUEST,
  POST_DELETE_SUCCESS,
  POST_DELETE_FAIL,
  POST_LIKE_REQUEST,
  POST_LIKE_SUCCESS,
  POST_LIKE_FAIL,
  POST_COMMENT_REQUEST,
  POST_COMMENT_SUCCESS,
  POST_COMMENT_FAIL,
  GET_COMMENTS_REQUEST,
  GET_COMMENTS_SUCCESS,
  GET_COMMENTS_FAIL,
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

export const postCommentReducer = (state = {}, action) => {
  switch (action.type) {
    case POST_COMMENT_REQUEST:
      return { loading: true };

    case POST_COMMENT_SUCCESS:
      return { loading: false, response: action.payload };

    case POST_COMMENT_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const postLikeReducer = (state = {}, action) => {
  switch (action.type) {
    case POST_LIKE_REQUEST:
      return { loading: true };

    case POST_LIKE_SUCCESS:
      return { loading: false, response: action.payload };

    case POST_LIKE_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const postDeleteReducer = (state = {}, action) => {
  switch (action.type) {
    case POST_DELETE_REQUEST:
      return { loading: true };

    case POST_DELETE_SUCCESS:
      return { loading: false, response: action.payload };

    case POST_DELETE_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const getCommentsReducer = (state = {}, action) => {
  switch (action.type) {
    case GET_COMMENTS_REQUEST:
      return { loading: true };

    case GET_COMMENTS_SUCCESS:
      return { loading: false, response: action.payload };

    case GET_COMMENTS_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

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
} from "../constants/userConstants";

export const userRegisterReducer = (state = {}, action) => {
  switch (action.type) {
    case USER_REGISTER_REQUEST:
      return { loading: true };

    case USER_REGISTER_SUCCESS:
      return { loading: false, userInfo: action.payload };

    case USER_REGISTER_FAIL:
      return { loading: false, error: action.payload };

    case USER_LOGOUT:
      return {};

    default:
      return state;
  }
};

export const userLoginReducer = (state = {}, action) => {
  switch (action.type) {
    case USER_LOGIN_REQUEST:
      return { loading: true };

    case USER_LOGIN_SUCCESS:
      return { loading: false, userInfo: action.payload };

    case USER_LOGIN_FAIL:
      return { loading: false, error: action.payload };

    case USER_LOGOUT:
      return {};

    default:
      return state;
  }
};

export const userDetailReducer = (state = {}, action) => {
  switch (action.type) {
    case USER_DETAIL_REQUEST:
      return { loading: true };

    case USER_DETAIL_SUCCESS:
      return { loading: false, userInfo: action.payload };

    case USER_DETAIL_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const userDetailEditReducer = (state = {}, action) => {
  switch (action.type) {
    case USER_DETAIL_EDIT_REQUEST:
      return { loading: true };

    case USER_DETAIL_EDIT_SUCCESS:
      return { loading: false, userInfo: action.payload };

    case USER_DETAIL_EDIT_FAIL:
      return { loading: false, error: action.payload };

    case USER_DETAIL_EDIT_RESET:
      return {};

    default:
      return state;
  }
};

export const userFriendlistReducer = (state = {}, action) => {
  switch (action.type) {
    case USER_FRIENDLIST_REQUEST:
      return { loading: true };

    case USER_FRIENDLIST_SUCCESS:
      return { loading: false, userFriends: action.payload };

    case USER_FRIENDLIST_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

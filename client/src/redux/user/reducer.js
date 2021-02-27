import { UserActionTypes } from "./types";

const INIT_STATE = {
  authorID: null
}

const userReducer = (state = INIT_STATE, action) => {
  switch (action.type) {
    case UserActionTypes.SET_CURRENT_USER:
      return {
        ...state,
        authorID: action.payload
      };
    default:
      return {
        ...state
      };
  }
}

export default userReducer;
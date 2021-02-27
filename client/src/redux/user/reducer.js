import { UserActionTypes } from "./types";
import { persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";

const INIT_STATE = {
  authorID: null
}

const persistConfig = {
  key: "root",
  storage,
  whitelist: ["authorID"]
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

export default persistReducer(persistConfig, userReducer);
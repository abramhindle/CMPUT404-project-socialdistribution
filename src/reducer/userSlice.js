import { createSlice } from "@reduxjs/toolkit";

export const userSlice = createSlice({
  name: "user",
  initialState: {
    displayName: "",
    github: "",
    host: "",
    id: "",
    profileImage: "",
    url: "",
    isLogin: null,
  },
  reducers: {
    signInUser: (state, action) => {
      console.log(action);
      state.displayName = action.payload.displayName;
      state.github = action.payload.github;
      state.host = action.payload.host;
      state.id = action.payload.id;
      state.profileImage = action.payload.profileImage;
      state.url = action.payload.url;
      state.isLogin = true;
      return state;
    },
    clearUser: (state) => {
      state.displayName = "";
      state.github = "";
      state.host = "";
      state.id = "";
      state.profileImage = "";
      state.url = "";
      state.isLogin = false;
      return state;
    },
  },
});

export const { signInUser, clearUser } = userSlice.actions;
export default userSlice.reducer;

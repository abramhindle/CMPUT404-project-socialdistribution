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
      state.displayName = action.payload.data.author.displayName;
      state.github = action.payload.data.author.github;
      state.host = action.payload.data.author.host;
      state.id = action.payload.data.author.id;
      state.profileImage = action.payload.data.author.profileImage;
      state.url = action.payload.data.author.url;
      state.isLogin = true;
      // sessionStorage.setItem("state", JSON.stringify(state));
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
      // sessionStorage.clear("state");
      return state;
    },
  },
});

export const { signInUser, clearUser } = userSlice.actions;
export default userSlice.reducer;

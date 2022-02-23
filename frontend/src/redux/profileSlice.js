import { createSlice } from '@reduxjs/toolkit'

export const profileSlice = createSlice({
  name: 'profile',
  initialState: {
    id: "",
    displayName: "", 
    github: "", 
    host: "", 
    profileImage: "", 
    url: "", 
  },
  reducers: {
    logout: (state) => {
        state.id = "";
        state.displayName = "";
        state.github = "";
        state.host = "";
        state.profileImage = "";
        state.url = "";
    },
    login: (state, action) => {
        state.id = action.payload.id.split("/").slice(-2, -1)[0];
        state.displayName = action.payload.displayName;
        state.github = action.payload.github;
        state.host = action.payload.host;
        state.profileImage = action.payload.profileImage;
        state.url = action.payload.url;
    },
  },
})

export const { logout, login } = profileSlice.actions

export default profileSlice.reducer
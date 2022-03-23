import { createSlice } from '@reduxjs/toolkit'
import { concat } from 'lodash/fp'

export const followingSlice = createSlice({
  name: 'following',
  initialState: {
    items: [], 
  },
  reducers: {
    addFollowing: (state, action) => {
      const data = {id: action.payload.id, displayName: action.payload.displayName, profileImage: action.payload.profileImage}
      state.items = concat(state.items)(data).sort((a, b) => a.displayName - b.displayName);
    },
    setFollowing: (state, action) => {
      state.items = action.payload.map(x => { return {id: x.id, displayName: x.displayName, profileImage: x.profileImage} });
    },
    removeFollowing: (state, action) => {
      state.items = state.items.filter(x => x.id !== action.payload.id);
    },
  },
})

export const { addFollowing, setFollowing, removeFollowing } = followingSlice.actions

export default followingSlice.reducer

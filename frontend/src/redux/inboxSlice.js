import { createSlice } from '@reduxjs/toolkit'
import { concat } from 'lodash/fp'

export const inboxSlice = createSlice({
  name: 'inbox',
  initialState: {
    items: [], 
  },
  reducers: {
    pushToInbox: (state, action) => {
      state.items = concat(state.items)(action.payload).sort((a, b) => Date.parse(b.published) - Date.parse(a.published));
    },
    setInbox: (state, action) => {
      state.items = action.payload;
    },
  },
})

export const { pushToInbox, setInbox } = inboxSlice.actions

export default inboxSlice.reducer

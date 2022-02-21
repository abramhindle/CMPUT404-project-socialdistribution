import { configureStore } from "@reduxjs/toolkit";
import storage from 'redux-persist/lib/storage';
import { combineReducers } from 'redux';
import { persistReducer } from 'redux-persist';
import thunk from 'redux-thunk';
import profileReducer from "./profileSlice"
import inboxReducer from "./inboxSlice"

const reducers = combineReducers({
    profile: profileReducer,
    inbox: inboxReducer, 
});

  const persistConfig = {
    key: 'root',
    storage,
};

  const persistedReducer = persistReducer(persistConfig, reducers);

const store = configureStore({
    reducer: persistedReducer,
    devTools: process.env.NODE_ENV !== 'production',
    middleware: [thunk],
})

export default store
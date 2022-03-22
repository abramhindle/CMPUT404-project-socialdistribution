import { configureStore } from "@reduxjs/toolkit";
import storage from 'redux-persist/lib/storage';
import { combineReducers, createStore } from 'redux';
import { persistReducer, persistStore } from 'redux-persist';
import profileReducer from "./profileSlice"
import inboxReducer from "./inboxSlice"
import followerReducer from "./followersSlice";
import followingReducer from "./followingsSlice"

const reducers = combineReducers({
    profile: profileReducer,
    inbox: inboxReducer, 
    followers: followerReducer, 
    following: followingReducer, 
});

const persistConfig = {
    key: 'root',
    storage,
    whitelist: ['profile', 'inbox', "followers", "following"]
};

const persistedReducer = persistReducer(persistConfig, reducers);
export let store = createStore(persistedReducer)
export let persistor = persistStore(store)

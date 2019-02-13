import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import socialDistApp from "../reducers/index";

const store = createStore(socialDistApp, applyMiddleware(thunk));

export default store;
import { createStore, applyMiddleware } from "redux"
import rootReducer from "./root-reducer";
import logger from "redux-logger";
// import StateLoader from "./state-loader";


const middlewares = [logger];

// const stateLoader = new StateLoader();

const store = createStore(
  rootReducer,
  // stateLoader.loadState(),
  applyMiddleware(...middlewares),
);

// store.subscribe(() => { stateLoader.saveState(store.getState()) });

export default store;
import { createStore, applyMiddleware } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension';
import thunk from 'redux-thunk';
import combineReducers from './reducers';

const initialState = {};

const middleware = [thunk];

const store = createStore(
    combineReducers,
    initialState,
    composeWithDevTools(applyMiddleware(...middleware))
);

export default store;
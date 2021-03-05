import { combineReducers } from 'redux';
import users from './users';
import errors from './errors';
import posts from './posts';

export default combineReducers({
    users,
    errors,
    posts
});
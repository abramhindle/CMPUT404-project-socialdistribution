import { combineReducers } from 'redux';
import users from './users';
import errors from './errors';

export default combineReducers({
    users,
    errors
});
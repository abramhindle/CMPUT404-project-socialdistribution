import { combineReducers } from 'redux';
import loginReducers from "./LoginReducers";
import friendsReducers from "./FriendsReducers";

const socialDistApp = combineReducers({
	loginReducers,
	friendsReducers,

})

export default socialDistApp;
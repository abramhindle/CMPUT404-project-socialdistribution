import { combineReducers } from 'redux';
import loginReducers from "./LoginReducers";
import registerReducers from "./RegisterReducers";
import friendsReducers from "./FriendsReducers";

const socialDistApp = combineReducers({
	loginReducers,
	registerReducers,
	friendsReducers,

})

export default socialDistApp;
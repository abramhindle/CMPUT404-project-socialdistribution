import { combineReducers } from 'redux';
import loginReducers from "./LoginReducers";
import registerReducers from "./RegisterReducers";

const socialDistApp = combineReducers({
	loginReducers,
	registerReducers

})

export default socialDistApp;
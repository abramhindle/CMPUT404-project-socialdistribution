import { combineReducers } from 'redux';
import loginReducers from "./LoginReducers";


const socialDistApp = combineReducers({
	loginReducers,
})

export default socialDistApp;
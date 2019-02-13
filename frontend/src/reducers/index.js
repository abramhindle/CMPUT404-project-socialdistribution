import { combineReducers } from 'redux';
import notes from "./notes";
import loginReducers from "./LoginReducers";


const socialDistApp = combineReducers({
  	notes,
	loginReducers,
})

export default socialDistApp;
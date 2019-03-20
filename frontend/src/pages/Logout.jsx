import React, { Component } from 'react';
import {Redirect} from "react-router-dom";
import Cookies from 'js-cookie';
import * as LoginActions from "../actions/LoginActions";
import {connect} from "react-redux";

class Logout extends Component {

    constructor(props) {
		super(props);
		Cookies.remove("username");
        Cookies.remove("userID");
        Cookies.remove("displayName");
        Cookies.remove("userPass");
        this.props.sendLogout();
    }

	render() {
        return(
            <Redirect push to="/" />
        )
    }
}

const mapDispatchToProps = dispatch => {
    return {
        sendLogout: () => {
            return dispatch(LoginActions.sendLogout());
        }
    }
};

export default connect(null, mapDispatchToProps)(Logout);
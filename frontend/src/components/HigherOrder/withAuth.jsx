import React from "react";
import SideBar from "../SideBar";
import {Redirect} from "react-router-dom";
import Cookies from 'js-cookie';
import store from '../../store/index.js';

export default function withAuth(Component, navId) {
    return class extends Component {
        render() {
            let isLoggedIn = store.getState().loginReducers.isLoggedIn || Cookies.get("userPass");
            if (isLoggedIn) {
                return (
                    <div>
                        <SideBar/>
                        <Component {...this.props} />
                    </div>
                );
            } else {
                return (
                    <Redirect to={"/"}/>
                );
            }
        }
    };
}

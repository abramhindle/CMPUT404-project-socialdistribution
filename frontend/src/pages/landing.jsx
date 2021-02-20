import React from 'react';
import CustomLayout from '../containers/layout';
import EntryCard from '../components/EntryCard';


import {UserSvc} from '../svc/UserSvc';

import {Typography} from 'antd';
const {Title} = Typography;


/*
 * Show this page when the user is not authorized.
 * It will provide the user with the ability to login or sign up
 */
class LandingPage extends React.Component {
    constructor(props) {
        super(props);
    }
    
    LoginHandler = (values) => {
        UserSvc.Login(values);
    }

    RegisterHandler = (values) => {
        UserSvc.Register(values);
    }

    render() {
        return (
            <CustomLayout>
               <Title>Wecolme to Social Distribution</Title>
                <div className="container" style={{display:"flex", justifyContent:"center"}}>
                    <EntryCard
                    style={{backgroundColor:"red"}}
                    LoginHandler={this.LoginHandler} 
                    RegisterHandler={this.RegisterHandler}
                /> 
                </div>
               
            </CustomLayout>
        );
    }
}

export default LandingPage;


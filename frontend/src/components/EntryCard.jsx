import React from 'react';
import {Card} from 'antd';

import LoginForm  from './LoginForm';
import RegisterForm from './RegisterForm';

const tabList = [
    {
        key: "Register",
        tab: "Register",
    },
    {
        key: "Login",
        tab: "Login",
    }
];


class EntryCard extends React.Component {
    constructor(props) {
        super(props);
        this.state = { key: 'Register' }
    }


    onTabChange = (key, type) => {
        this.setState({[type]: key});
    }

    render() {
       return (
           <Card
            style={{width:"20%"}}
            size="small"
            tabList={tabList}
            activeTabKey={this.state.key}
            tabProps={{centered: true}}
            onTabChange={key => {
                this.onTabChange(key, 'key');
            }}
           >
           {this.state.key === "Login"
               ? <LoginForm LoginHandler={this.props.LoginHandler}/>
               : <RegisterForm RegisterHandler={this.props.RegisterHandler}/>
           }
           </Card>
       );
    }
}

export default EntryCard;


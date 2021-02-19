import React from 'react';
import CustomLayout from '../containers/layout';
import EntryCard from '../components/EntryCard';


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
        console.log('Login values of form: ', values);
    }

    RegisterHandler = (values) => {
        console.log('Register values of form: ', values);
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
/*
<Row>
                <Col flex={3} style={{backgroundColor: '#14213d'}}>
                    <h1> Welcome to Social Distribution! </h1>
                </Col>
                <Col flex={2} style={{backgroundColor: '#fca311'}}>
                    Right
                </Col>
            </Row>
*/

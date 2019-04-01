import React from 'react';
import { Message } from 'semantic-ui-react';
import './styles/NotFound.css';
const NotFound = () => {
    return (
        <div className="container">
			<img className="image404" alt="Not Found" src={require('../assets/images/404Image.png')}/>
        	<h1 className="text404"> 404 </h1>
        
        	<Message as="h2"
            className="notFoundMessage"
            color="blue"
            >
            <Message.Header> Not Found </Message.Header>
            <p>The page you're looking for does not exist.</p>
            </Message>
        </div>
    )
}

export default NotFound
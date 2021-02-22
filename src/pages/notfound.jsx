import React from 'react';

import Response from '../components/Response';
/*
 * Show this page when a path in the router cannot be found
 */

const NotFound = () => {
    return (
        <Response status="404" title="404" subTitle="Sorry, the page you visited does not exist"/>
    )
}

export default NotFound;

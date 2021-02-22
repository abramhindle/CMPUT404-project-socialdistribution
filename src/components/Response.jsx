import React from 'react';

import {Result} from 'antd';

const Response = (props) => {
    return (
        <Result
            status={props.status}
            title={props.title}
            subTitle={props.subTitle}
        />
    );
}

export default Response; 

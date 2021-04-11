import React from 'react';

import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';


const useStyles = makeStyles(() => ({
    root: {
        // height: '300px',
        backgroundColor: 'white',
        borderRadius: "8px",
        padding: '1em 2em',
        display: 'flex'
    },
    summary: {
        marginTop: 'auto',
        marginBottom: 'auto'
    },
    like: {
        marginLeft: 'auto',
        padding: '0.25em 0.5em',
        borderRadius: '50%',
        '&:hover': {
            backgroundColor: '#D3D3D3',
        }
    }
}));  


export default function Comment(props) {
    const classes = useStyles();

    const clickHandler = () => {
        props.likeClicked(props.comment);
    }
    return (
        <div className={classes.root}>
            <p className={classes.summary}>{ props.comment.comment }</p>
            <div className={classes.like} onClick={clickHandler}>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.66665 14.6666H2.66665C2.31302 14.6666 1.97389 14.5261 1.72384 14.2761C1.47379 14.026 1.33331 13.6869 1.33331 13.3333V8.66659C1.33331 8.31296 1.47379 7.97383 1.72384 7.72378C1.97389 7.47373 2.31302 7.33325 2.66665 7.33325H4.66665M9.33331 5.99992V3.33325C9.33331 2.80282 9.1226 2.29411 8.74753 1.91904C8.37245 1.54397 7.86375 1.33325 7.33331 1.33325L4.66665 7.33325V14.6666H12.1866C12.5082 14.6702 12.8202 14.5575 13.0653 14.3493C13.3103 14.141 13.4718 13.8512 13.52 13.5333L14.44 7.53325C14.469 7.34216 14.4561 7.14704 14.4022 6.96142C14.3483 6.7758 14.2547 6.60412 14.1279 6.45826C14.0011 6.31241 13.844 6.19587 13.6677 6.11673C13.4914 6.03759 13.2999 5.99773 13.1066 5.99992H9.33331Z" stroke="#D1305E" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
            </div>
        </div>
    );
}

import React from 'react';
import { useHistory } from "react-router-dom";

import { makeStyles } from '@material-ui/core/styles';
// import Link from '@material-ui/core/Link';

// import { Link, Redirect } from 'react-router-dom'

const useStyles = makeStyles(() => ({
    root: {
        // height: '300px',
        backgroundColor: 'white',
        marginBottom: '40px',
        borderRadius: "8px",
    },
    postCard: {
        padding: "1em",
        overflow: "hidden",
    },
    postHead: {
        height: "50px",
        margin: "1em",
        alignItems: "center"
    },
    displayName: {
        fontWeight: 'bold',
        fontSize: '1.15em',
        margin: '0em 1em'
    },
    postBody: {
        height: "10.5em",
        margin: "1em",
        overflow: "hidden",
    },
    divider: {
        margin: '0em 1em',
        opacity: '0.2'
    },
    postFooter: {
        display: "flex",
        alignItems: "center",
        fontWeight: '500'
    },
    title: {
        margin: "0",
    },
    textField: {
        overflow: "hidden",
        lineHeight: "1.5em"
    },
    info: {
        color: '#H3H3H3',
        fontSize: '0.75em'
    },
    likeButton: {
        marginLeft: '1em',
        width: '4em',
        height: '2em',
        borderRight: '1px solid lightgray',
        display: 'flex',
        alignItems: 'center',
        '&:hover': {
            backgroundColor: '#D3D3D3',
        }
    },
    like: {
        margin: '0 auto',
        display: 'block'
    },
    commentButton: {
        height: '2em',
        borderRight: '1px solid lightgray',
        display: 'flex',
        alignItems: 'center',
        '&:hover': {
            backgroundColor: '#D3D3D3',
        }
    },
    comment: {
        margin: '0em 1em',
        display: 'block'
    },
    commentCount: {
        display: 'inline-block',
        transform: 'translate(2px, 2px)'
    },
    shareButton: {
        height: '2em',
        borderLeft: '1px solid lightgray',
        display: 'flex',
        alignItems: 'center',
        marginLeft: 'auto',
        marginRight: '1em',
        '&:hover': {
            backgroundColor: '#D3D3D3',
        }
    },
    share: {
        margin: '0em 1em',
        display: 'block'
    },
  }));  


export default function Post(props) {
    const classes = useStyles();
    const history = useHistory();
    
    const { postData } = props;

    // click on the Comments count to see the full post, with its paginated comments
    const handleSeeFullPost = (url) => {
        history.push(url)
    }

    // console.log(postData.id)

    return (
        <div className={classes.root}>
            <div 
                className={classes.postCard}
            >
                <div
                    className={classes.postHead}
                >
                    <h4>{ postData.title }</h4>
                    <p className={classes.info}>
                        Posted by {postData.author.displayName} on {postData.published.split('T')[0]}
                    </p> 
                </div>
                <div 
                    className={classes.postBody}
                >
                    <p
                        className={classes.textField}
                    >
                        {postData.content}
                    </p>
                </div>
                <hr className={classes.divider}></hr>
                    
                <div className={classes.postFooter}>
                    <div className={classes.likeButton}>
                        <svg className={classes.like} width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M4.66665 14.6666H2.66665C2.31302 14.6666 1.97389 14.5261 1.72384 14.2761C1.47379 14.026 1.33331 13.6869 1.33331 13.3333V8.66659C1.33331 8.31296 1.47379 7.97383 1.72384 7.72378C1.97389 7.47373 2.31302 7.33325 2.66665 7.33325H4.66665M9.33331 5.99992V3.33325C9.33331 2.80282 9.1226 2.29411 8.74753 1.91904C8.37245 1.54397 7.86375 1.33325 7.33331 1.33325L4.66665 7.33325V14.6666H12.1866C12.5082 14.6702 12.8202 14.5575 13.0653 14.3493C13.3103 14.141 13.4718 13.8512 13.52 13.5333L14.44 7.53325C14.469 7.34216 14.4561 7.14704 14.4022 6.96142C14.3483 6.7758 14.2547 6.60412 14.1279 6.45826C14.0011 6.31241 13.844 6.19587 13.6677 6.11673C13.4914 6.03759 13.2999 5.99773 13.1066 5.99992H9.33331Z" stroke="#D1305E" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                    </div>
                    <div className={classes.commentButton} onClick={() => handleSeeFullPost(postData.id)}>
                        <div className={classes.comment}>
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M14 7.66669C14.0023 8.5466 13.7967 9.41461 13.4 10.2C12.9296 11.1412 12.2065 11.9328 11.3116 12.4862C10.4168 13.0396 9.3855 13.3329 8.33333 13.3334C7.45342 13.3356 6.58541 13.1301 5.8 12.7334L2 14L3.26667 10.2C2.86995 9.41461 2.66437 8.5466 2.66667 7.66669C2.66707 6.61452 2.96041 5.58325 3.51381 4.68839C4.06722 3.79352 4.85884 3.0704 5.8 2.60002C6.58541 2.20331 7.45342 1.99772 8.33333 2.00002H8.66667C10.0562 2.07668 11.3687 2.66319 12.3528 3.64726C13.3368 4.63132 13.9233 5.94379 14 7.33335V7.66669Z" stroke="#D1305E" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                            </svg>
                            <span className={classes.commentCount}>{postData.count}</span>
                        </div>
                    </div>
                    <div className={classes.shareButton}>
                        <div className={classes.share}>
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 5.33325C13.1046 5.33325 14 4.43782 14 3.33325C14 2.22868 13.1046 1.33325 12 1.33325C10.8954 1.33325 10 2.22868 10 3.33325C10 4.43782 10.8954 5.33325 12 5.33325Z" fill="#D1305E" stroke="#D1305E" strokeLinecap="round" strokeLinejoin="round"/>
                                <path d="M4 10C5.10457 10 6 9.10457 6 8C6 6.89543 5.10457 6 4 6C2.89543 6 2 6.89543 2 8C2 9.10457 2.89543 10 4 10Z" fill="#D1305E" stroke="#D1305E" strokeLinecap="round" strokeLinejoin="round"/>
                                <path d="M12 14.6667C13.1046 14.6667 14 13.7713 14 12.6667C14 11.5622 13.1046 10.6667 12 10.6667C10.8954 10.6667 10 11.5622 10 12.6667C10 13.7713 10.8954 14.6667 12 14.6667Z" fill="#D1305E" stroke="#D1305E" strokeLinecap="round" strokeLinejoin="round"/>
                                <path d="M5.72672 9.00684L10.28 11.6602" stroke="#D1305E" strokeLinecap="round" strokeLinejoin="round"/>
                                <path d="M10.2734 4.34009L5.72672 6.99342" stroke="#D1305E" strokeLinecap="round" strokeLinejoin="round"/>
                            </svg>
                            <span className={classes.commentCount}>SHARE</span>
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
    )
}

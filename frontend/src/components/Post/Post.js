import React, { useState } from 'react';
import { useHistory } from "react-router-dom";
import InputBase from '@material-ui/core/InputBase';

import { makeStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import Comment from './Comment';
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
        alignItems: "center",
        position: "relative"
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
    commentsTitle: {
        color: '#H3H3H3',
        fontSize: '0.75em',
        padding: '0em 2em',
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
    sendButton: {
        margin: '0em 0.5em',
        marginTop: '0.2em',
        '&:hover': {
            backgroundColor: '#FFCCCB',
            fill: 'white'
        },
        height: 'fit-content'
    },
    flexContainer: {
        display: 'flex',
        padding: '1em 1em'
    },
    editWrapper: {
        position: "absolute",
        right: "0",
        display: "flex"
    },
    editButton: {
        width: "fit-content",
        padding: "10px 10px",
        borderRadius: "50%",
        '&:hover': {
            backgroundColor: 'lightgray',
        }
    },
    editButtonSelected: {
        backgroundColor: "lightgray"
    },
    editTitleWrapper: {
        width: "80%"
    }
}));  


export default function Post(props) {
    const classes = useStyles();
    const history = useHistory();

    var CommonMark = require('commonmark');
    var ReactRenderer = require('commonmark-react-renderer');

    var parser = new CommonMark.Parser();
    var renderer = new ReactRenderer();    
        
    const { postData } = props;

    if (postData) {
        if (postData.visibility === 'FRIENDS') {
            const url = postData.id.split('/');
            url[5] = 'post';
            url.push('likes');
            props.getLikes(url.join('/'));
        }
    }

    const [expanded, setExpanded] = useState(false);
    const [expandedContent, setExpandedContent] = useState(null);
    const [edit, setEdit] = useState(false);
    const [title, setTitle] = useState(postData.title);

    let comment = '';

    const content = () => {
        if (postData.contentType === 'text/plain') {
            return <p className={classes.postBody}>{postData.content}</p>;
        } else if (postData.contentType === 'text/markdown') {
            var ast = parser.parse(postData.content);
            var result = renderer.render(ast);
            return result;
        } else if (postData.contentType === 'image/jpeg' || postData.contentType === 'image/png' || postData.contentType === 'image/jpeg;base64' || postData.contentType === 'image/png;base64') {
            return <img src={postData.content} alt='postimage'/>;
        } else {
            console.log(postData);
        }

        return null;
    }

    const onLikeClicked = () => {
        return props.onLikeClicked(postData);
    }

    const onTextChange = (e) => {
        switch (e.target.id) {
            case postData.id:
                comment = e.target.value;
                break;
            case 'editTitle':
                setTitle(e.target.value);
                break;    
            default:
                break;
        }
    }

    const sendButtonHandler = (e) => {
        props.createComment({
            type: 'comment',
            author: props.author,
            comment,
            contentType: 'text/markdown'
        }, postData);
    }

    const onShareClicked = (e) => {
        props.sharePost(postData);
    }

    const onEditButtonClick = (e) => {
        setEdit(!edit);
    }

    const onDeleteClicked = (e) => {
        props.deleteClicked(postData);
    }

    const onCommentClicked = (e) => {
        if (!expanded) {
            const comments = (postData.visibility !== 'FRIENDS') && (postData.comments.length !== 0)
                ?   <div>
                        <div className={classes.commentsTitle}>
                            Comments:
                        </div>
                        <div>
                            { postData.comments.map( (d) => <Comment key={d.id} comment={d}/>) }
                        </div>
                    </div>
                : null;

            setExpandedContent(
                <div>
                    <div className={classes.flexContainer}>
                        <InputBase
                            className={classes.textField}
                            onChange={onTextChange}
                            placeholder='Add a comment'
                            fullWidth
                            id={postData.id}
                        />
                        <div
                            className={classes.sendButton}
                            onClick={sendButtonHandler}
                        >
                            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect width="32" height="32" rx="4" fill="#D1305E"/>
                                <path d="M21.6667 10.3333L14.3333 17.6666" stroke="white" strokeLinecap="round" strokeLinejoin="round"/>
                                <path d="M21.6667 10.3333L17 23.6666L14.3333 17.6666L8.33333 14.9999L21.6667 10.3333Z" stroke="white" strokeLinecap="round" strokeLinejoin="round"/>
                            </svg>
                        </div>
                    </div>
                    { comments }
                </div>
                );
            setExpanded(true);
        } else {
            setExpandedContent(null);
            setExpanded(false);
        }

    }

    return (
        <div className={classes.root}>
            <div 
                className={classes.postCard}
            >
                <div
                    className={classes.postHead}
                >
                    <div>
                        {
                            props.editMode
                            ? <div className={classes.editWrapper}>
                                { edit ? <IconButton aria-label="delete" className={classes.margin} onClick={onDeleteClicked}>
                                    <DeleteIcon fontSize="small"/>
                                </IconButton> : null}
                                <div className={edit ? [classes.editButton, classes.editButtonSelected].join(' ') : classes.editButton} onClick={onEditButtonClick}>
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path fillRule="evenodd" clipRule="evenodd" d="M5.92688 18.0732L7.61133 22.5953L12 20.5887L16.3887 22.5953L18.0732 18.0732L22.5953 16.3887L20.5887 12L22.5953 7.61133L18.0732 5.92688L16.3887 1.40479L12 3.4113L7.61133 1.40479L5.92688 5.92688L1.40479 7.61133L3.4113 12L1.40479 16.3887L5.92688 18.0732ZM15.265 19.8824L12 18.3896L8.73504 19.8824L7.48189 16.5182L4.11767 15.265L5.61042 12L4.11767 8.73504L7.48189 7.48189L8.73504 4.11767L12 5.61042L15.265 4.11767L16.5182 7.48189L19.8824 8.73504L18.3896 12L19.8824 15.265L16.5182 16.5182L15.265 19.8824ZM12 17C9.2386 17 7.00002 14.7614 7.00002 12C7.00002 9.2386 9.2386 7.00002 12 7.00002C14.7614 7.00002 17 9.2386 17 12C17 14.7614 14.7614 17 12 17ZM15 12C15 13.6569 13.6569 15 12 15C10.3432 15 9.00002 13.6569 9.00002 12C9.00002 10.3432 10.3432 9.00002 12 9.00002C13.6569 9.00002 15 10.3432 15 12Z" fill="black"/>
                                    </svg>
                                </div>
                            </div>
                            : null
                        }
                    </div>
                    {
                        edit ?
                            <div className={classes.editTitleWrapper}>
                                <InputBase
                                    className={classes.editTitle}
                                    onChange={onTextChange}
                                    placeholder={postData.title}
                                    fullWidth
                                    id='editTitle'
                                />
                            </div>
                            : <h4>{ postData.title }</h4>
                    }
                    <p className={classes.info}>
                        Posted by {postData.author.displayName} on {postData.published.split('T')[0]}
                    </p>
                </div>
                <div 
                    className={classes.postBody}
                >
                    {content()}
                </div>
                <hr className={classes.divider}></hr>
                    
                <div className={classes.postFooter}>
                    <div className={classes.likeButton} onClick={onLikeClicked}>
                        <svg className={classes.like} width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M4.66665 14.6666H2.66665C2.31302 14.6666 1.97389 14.5261 1.72384 14.2761C1.47379 14.026 1.33331 13.6869 1.33331 13.3333V8.66659C1.33331 8.31296 1.47379 7.97383 1.72384 7.72378C1.97389 7.47373 2.31302 7.33325 2.66665 7.33325H4.66665M9.33331 5.99992V3.33325C9.33331 2.80282 9.1226 2.29411 8.74753 1.91904C8.37245 1.54397 7.86375 1.33325 7.33331 1.33325L4.66665 7.33325V14.6666H12.1866C12.5082 14.6702 12.8202 14.5575 13.0653 14.3493C13.3103 14.141 13.4718 13.8512 13.52 13.5333L14.44 7.53325C14.469 7.34216 14.4561 7.14704 14.4022 6.96142C14.3483 6.7758 14.2547 6.60412 14.1279 6.45826C14.0011 6.31241 13.844 6.19587 13.6677 6.11673C13.4914 6.03759 13.2999 5.99773 13.1066 5.99992H9.33331Z" stroke="#D1305E" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                    </div>
                    <div className={classes.commentButton} onClick={onCommentClicked}>
                        <div className={classes.comment}>
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M14 7.66669C14.0023 8.5466 13.7967 9.41461 13.4 10.2C12.9296 11.1412 12.2065 11.9328 11.3116 12.4862C10.4168 13.0396 9.3855 13.3329 8.33333 13.3334C7.45342 13.3356 6.58541 13.1301 5.8 12.7334L2 14L3.26667 10.2C2.86995 9.41461 2.66437 8.5466 2.66667 7.66669C2.66707 6.61452 2.96041 5.58325 3.51381 4.68839C4.06722 3.79352 4.85884 3.0704 5.8 2.60002C6.58541 2.20331 7.45342 1.99772 8.33333 2.00002H8.66667C10.0562 2.07668 11.3687 2.66319 12.3528 3.64726C13.3368 4.63132 13.9233 5.94379 14 7.33335V7.66669Z" stroke="#D1305E" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                            </svg>
                            <span className={classes.commentCount}>{postData.visibility !== 'FRIENDS' ? postData.count : ''}</span>
                        </div>
                    </div>
                    <div className={classes.shareButton} onClick={onShareClicked}>
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
            { expandedContent }
        </div>
    )
}

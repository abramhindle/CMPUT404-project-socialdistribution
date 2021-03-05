import React from 'react';

import { makeStyles } from '@material-ui/core/styles';
// import Link from '@material-ui/core/Link';

// import { Link, Redirect } from 'react-router-dom'

const useStyles = makeStyles(() => ({
    root: {
        height: '300px',
        backgroundColor: 'white',
        marginBottom: '40px',
        borderRadius: "8px",
    },
    postCard: {
        // height: '300px',
        // marginBottom: '40px',
        padding: "1em",
        // backgroundColor: 'white',
        overflow: "hidden",
    },
    postHead: {
        height: "50px",
        margin: "1em",
    },
    displayName: {
        fontWeight: 'bold',
        fontSize: '1.15em',
        margin: '0em 1em'
    },
    postBody: {
        height: "11.5em",
        margin: "1em",
        overflow: "hidden",
    },
    divider: {
        margin: '1em 1em',
        opacity: '0.2'
    },
    title: {
        // fontSize: '1.25em',
        // margin: '0em 1em'
    },
    textField: {
        // fontSize: '1.15em',
        // margin: '0em 1em',
        overflow: "hidden",
        lineHeight: "1.5em"
    },
  }));  


export default function Post(props) {
    const classes = useStyles();
    
    const { history } = props;
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
                <p 
                    className={classes.title}
                >
                    Post by: {postData.author.displayName}
                </p>
                <div 
                    className={classes.postBody}
                >
                    <p
                        className={classes.title}
                    >
                        Title: {postData.title}
                    </p>
                    <p
                        className={classes.textField}
                    >
                        Content: {postData.content}
                    </p>

                    <hr className={classes.divider}></hr>
                    
                    <a 
                        className={classes.title}
                        onClick={() => handleSeeFullPost(postData.id)}
                    >
                        {`Comments (${postData.count})`}
                    </a>
                </div>
                
            </div>
            
        </div>
    )
}

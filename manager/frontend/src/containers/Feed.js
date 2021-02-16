import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import Navbar from '../components/Navbar/Navbar';
import PostCreator from '../components/PostCreator/PostCreator';
import PostSorter from '../components/PostSorter/PostSorter';
import Post from '../components/Post/Post';

const useStyles = makeStyles(() => ({
    posts: {
        padding: '0px 10%'
    },
  }));  


export default function Feed() {
    const classes = useStyles();
    const postClasses = [classes.posts, 'col-9']

    const temp_posts = ['post1', 'post2', 'post3'];

    return (
        <div 
            className="feed"
            style={{ width: "100%", height: "100%" }}
        >
            <Navbar />
            <div className='container-fluid'>
                <div className='row align-items-start'>
                    <div className={postClasses.join(' ')}>
                        <PostCreator />
                        <PostSorter />

                    </div>
                    <div className='col-3'>

                    </div>
                </div>
            </div>            
        </div>
        
    )
}
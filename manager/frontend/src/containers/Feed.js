import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import _ from 'lodash';

import Navbar from '../components/Navbar/Navbar';
import PostCreator from '../components/PostCreator/PostCreator';
import PostSorter from '../components/PostSorter/PostSorter';
import Post from '../components/Post/Post';

const useStyles = makeStyles(() => ({
    posts: {
        padding: '0px 10%'
    },
    feed: {
        
    }
  }));


export default function Feed() {
    const classes = useStyles();
    const postClasses = [classes.posts, 'col-9']

    const temp_posts = [
        {title: 'post1'},
        {title: 'post2'},
        {title: 'post3'},
        {title: 'post4'},
    ];

    let posts = temp_posts.map((d, i) => <Post key={i} postContent={d.title}/>);

    return (
        <div 
            className={classes.feed}
        >
            <Navbar />
            <div className='container-fluid'>
                <div className='row align-items-start'>
                    <div className={postClasses.join(' ')}>
                        <PostCreator />
                        <PostSorter />
                        { posts }
                    </div>
                    <div className='col-3'>

                    </div>
                </div>
            </div>            
        </div>
        
    )
}
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import _ from 'lodash';

import Navbar from '../components/Navbar/Navbar';
import PostCreator from '../components/PostCreator/PostCreator';
import PostSorter from '../components/PostSorter/PostSorter';
import Post from '../components/Posts/Post/Post';
import Friends from '../components/Friends/Friends';
import Followers from '../components/Followers/Followers';

import simplifiedPosts from '../dummyData/Dummy.FeedPosts.js';

const useStyles = makeStyles(() => ({
    posts: {
    },
    feed: {
        backgroundColor: "#EFEFEF"
    },
    container: {
        padding: '0px 10%'
    }
  }));

// pretend this is my author id to tell between my posts and others' posts
// const stuffFromAuthContext = {
//     "userId": "http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e"
// }

export default function Feed(props) {
    const classes = useStyles();
    const postClasses = [classes.posts, 'col-9', 'pe-5']
    const container = ['container-fluid', classes.container];

    const { history } = props;

    const temp_friends = [
        {name: 'Friend1'},
        {name: 'Friend2'},
        {name: 'Friend3'},
        {name: 'Friend4'},
        {name: 'Friend5'},
    ];

    const temp_follower_count = 10;
    // console.log(simplifiedPosts)

    return (
        <div 
            className={classes.feed}
        >
            <Navbar />
            <div className={container.join(' ')}>
                <div className='row align-items-start'>
                    <div className={postClasses.join(' ')}>
                        <PostCreator />
                        <PostSorter />

                        {/* I think getting multiple posts should have less data. The full structure is available in ExpandPost */}
                        {simplifiedPosts.map( postData =>
                            <Post 
                                key={postData["id"]}
                                postData={postData}
                                history={history}
                            />
                        )}
                    </div>
                    <div className='col-3 ps-5'>
                        <Friends friends={temp_friends}/>
                        <Followers followerCount={temp_follower_count} />
                    </div>
                </div>
            </div>            
        </div>
        
    )
}
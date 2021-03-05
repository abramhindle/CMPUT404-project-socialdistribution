import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import _ from 'lodash';
import { connect } from "react-redux";

import Navbar from '../components/Navbar/Navbar';
import PostCreator from '../components/PostCreator/PostCreator';
import PostSorter from '../components/PostSorter/PostSorter';
import Post from '../components/Posts/Post/Post';
import Friends from '../components/Friends/Friends';
import Followers from '../components/Followers/Followers';

import { postNewPost } from "../actions/posts";

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

<<<<<<< HEAD
export default function Feed(props) {
=======
function Feed(props) {
>>>>>>> master
    const classes = useStyles();
    const postClasses = [classes.posts, 'col-9', 'pe-5']
    const container = ['container-fluid', classes.container];

<<<<<<< HEAD
    const { history } = props;

=======
>>>>>>> master
    const temp_friends = [
        {name: 'Friend1'},
        {name: 'Friend2'},
        {name: 'Friend3'},
        {name: 'Friend4'},
        {name: 'Friend5'},
    ];

    const temp_follower_count = 10;

    const createNewPost = (post) => {
        // TEMPORARY DATA UNTIL API CHANGES
        const author_id = "e7345869425e449ba97ad93fce793dd5";
        const source = "http://lastplaceigotthisfrom.com/posts/yyyyy";
        const origin = "http://whereitcamefrom.com/posts/zzzzz";
        const count = 1023;
        const unlisted = false;

        const finalPost = {
            ...post,
            author_id,
            source,
            origin,
            count,
            unlisted
        }
        console.log(finalPost);
        props.postNewPost(finalPost);
    }

    React.useEffect(() => {
        if (!_.isEmpty(props.post)) {
            console.log(props.post);
        }
    });

    return (
        <div 
            className={classes.feed}
        >
            <Navbar />
            <div className={container.join(' ')}>
                <div className='row align-items-start'>
                    <div className={postClasses.join(' ')}>
                        <PostCreator createNewPost={createNewPost}/>
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

const mapStateToProps = (state) => ({
    post: state.posts.post
});
  
export default connect(mapStateToProps, { postNewPost })(Feed);
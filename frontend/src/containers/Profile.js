import React, {useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import _ from 'lodash';
import { useHistory } from "react-router-dom";
import { connect } from "react-redux";

import ProfileInfo from '../components/ProfileInfo/ProfileInfo';
import Navbar from '../components/Navbar/Navbar';

import { getPersonalPosts, deletePost, putUpdatePost, getComments, getLikes, postLike, postComment, postSharePost } from "../actions/posts";
import Stream from '../components/Stream/Stream';

const useStyles = makeStyles(() => ({
    posts: {
    },
    feed: {
        backgroundColor: "#EFEFEF"
    },
    container: {
        padding: '0px 10%'
    },
    friends: {
        marginBottom: '2em'
    }
  }));

function Profile(props) {
    const classes = useStyles();
    const history = useHistory();
    const postClasses = [classes.posts, 'col-9', 'pe-5'];
    const container = ['container-fluid', classes.container];

    const [loaded, setLoaded] = useState(false);
    const [likesLoaded, setLikesLoaded] = useState(false);

    const initialLoad = () => {
        if (!loaded) {
            props.getPersonalPosts(props.author, props.token);
            setLoaded(true);
        }
    }

    const deletePost = (post) => {
        props.deletePost(post, props.token);
    }

    const editPost = (post) => {
        props.putUpdatePost(post, props.token);
    }

    const postLiked = (post) => {
        const body = {
            '@context': "https://www.w3.org/ns/activitystreams",
            summary: `${props.author.displayName} Likes your post`,
            type: 'Like',
            author: props.author,
            object: post.id
        }
        props.postLike(body, post.author, props.token);
    }

    const commentLiked = (comment) => {
        const body = {
            '@context': "https://www.w3.org/ns/activitystreams",
            summary: `${props.author.displayName} Likes your comment`,
            type: 'Like',
            author: props.author,
            object: comment.id
        }
        props.postLike(body, comment.author, props.token);
    }

    const createComment = (body, post) => {
        props.postComment(body, post, props.token, !body.comments.includes('team6-project-socialdistrib'));
    }

    const sharePost = (post) => {
        props.postSharePost(post, props.token, props.author_id);
    }

    React.useEffect(() => {
        if (_.isEmpty(props.author)) {
            history.push("/login");
        } else {
            initialLoad();
        }

        if (!_.isEmpty(props.personal_posts)) {
            if (props.personal_posts && props.personal_posts.length !== 0 && !likesLoaded) {
                setLikesLoaded(true);
                _.forEach(props.personal_posts, d => {
                    if (d.type === 'post' && d.visibility === 'FRIENDS') {
                        const post = d.id.split('/');
                        post[5] = 'post';
                        props.getLikes(
                        {
                            ...d,
                            id: post.join('/')
                        }, props.token);
                    }

                    // get comments of each post
                    if (d.type === 'post') {
                        props.getComments(d, props.token);
                    }
                });
            }
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
                        <h2>My Posts</h2>
                        <hr></hr>
                        <Stream
                            data={props.personal_posts}
                            author={props.author}
                            deleteClicked={deletePost}
                            editPost={editPost}
                            comments={props.comments}
                            postLiked={postLiked}
                            commentLiked={commentLiked}
                            createComment={createComment}
                            sharePost={sharePost}
                            likes={props.likes}
                        />
                    </div>
                    <div className='col-3 ps-5'>
                        <ProfileInfo profile={props.author}/>
                    </div>
                </div>
            </div>
        </div>
        
    )
}

const mapStateToProps = (state) => ({
    author: state.users.user,
    token: state.users.basic_token,
    personal_posts: state.posts.personal_posts,
    comments: state.posts.comments
});
  
export default connect(mapStateToProps, {getPersonalPosts, deletePost, putUpdatePost, getComments, getLikes, postLike, postComment, postSharePost})(Profile);
import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import _ from 'lodash';
import { connect } from "react-redux";
import { useHistory } from "react-router-dom";

import Navbar from '../components/Navbar/Navbar';
import PostCreator from '../components/PostCreator/PostCreator';
import PostSorter from '../components/PostSorter/PostSorter';
import Inbox from '../components/Inbox/Inbox';
import Friends from '../components/Friends/Friends';
import Followers from '../components/Followers/Followers';
import GithubStream from '../components/GithubStream/GithubStream';

import { postNewPost, getInbox, postLike, postComment, getLikes } from "../actions/posts";
import { postSearchDisplayName, postFriendRequest, getGithub, getFriends, getFollowers, getRemoteAuthors, postRemoteFriendRequest, postSearchDisplayNameRemote } from '../actions/users';

import reference from '../dummyData/Dummy.FeedPosts.js';
import { object } from 'prop-types';

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

function Feed(props) {
    const classes = useStyles();
    const history = useHistory();
    const postClasses = [classes.posts, 'col-9', 'pe-5']
    const container = ['container-fluid', classes.container];

    const searchPeople = (displayName) => {
        props.postSearchDisplayName({displayName});
        props.postSearchDisplayNameRemote({displayName});
    }

    // const searchRemoteAuthors = () => {
    //     props.getRemoteAuthors();
    // }

    const postFriendRequest = (post, object_id) => {
        console.log(object_id);
        console.log(props.remote_authors);
        if (_.includes(props.remote_authors, object_id)) {
            props.postRemoteFriendRequest(post, object_id, props.author_id, btoa('team6user:thisisforteam6'));
        } else {
            props.postFriendRequest(post, object_id.url, props.token);
        }
    }
    

    const temp_follower_count = 10;
    const [loaded, setLoaded] = useState(false);
    const initialLoad = () => {
        if (!loaded) {
            props.getInbox(props.author_id, props.token);
            props.getFriends(props.author_id);
            props.getFollowers(props.author_id);
            props.getRemoteAuthors(btoa('team6user:thisisforteam6'));
            const github = props.author.github.split('/');
            props.getGithub(github[github.length - 1]);
            setLoaded(true);
        }
    }

    const createNewPost = (post) => {
        // TEMPORARY DATA UNTIL API CHANGES
        const source = "http://lastplaceigotthisfrom.com/posts/yyyyy";
        const origin = "http://whereitcamefrom.com/posts/zzzzz";
        const unlisted = false;
        const description = 'this is a text post';

        const finalPost = {
            ...post,
            author_id: props.author_id,
            source,
            origin,
            unlisted,
            description
        }

        // const uploadData = new FormData();
        // uploadData.append('author_id', author_id);
        // uploadData.append('categories', post.categories);
        // uploadData.append('contentType', post.contentType);
        // uploadData.append('description', post.description);
        // uploadData.append('content', post.content);
        // uploadData.append('origin', origin);
        // uploadData.append('source', source);
        // uploadData.append('title', post.title);
        // uploadData.append('unlisted', unlisted);
        // uploadData.append('visibility', post.visibility);

        props.postNewPost(finalPost, props.token);
    }

    const postLiked = (post) => {
        const body = {
            '@context': "https://www.w3.org/ns/activitystreams",
            summary: `${props.author.displayName} Likes your post`,
            type: 'Like',
            author: props.author,
            object: post.id
        }
        const author = post.author.id.split('/');
        props.postLike(body, author[author.length - 1], props.token);
    }

    const createComment = (body, post) => {
        props.postComment(body, post.id, props.token);
    }

    const getLikes = (url) => {
        // props.getLikes(url, props.token);
    }

    React.useEffect(() => {
        if (_.isEmpty(props.author)) {
            history.push("/login");
        } else {
            initialLoad();
        }
        if (!_.isEmpty(props.post)) {
            // console.log(props.post);
        }
        if (!_.isEmpty(props.friendRequest)) {
            // console.log(props.friendRequest);
        }
        if (!_.isEmpty(props.inbox)) {
            // console.log(props.inbox);
        }
        if (!_.isEmpty(props.like)) {
            // console.log(props.like);
        }
        if (!_.isEmpty(props.comment)) {
            // console.log(props.comment);
        }
        if (!_.isEmpty(props.remote_authors)) {
            // console.log(props.remote_authors);
        }
        if (!_.isEmpty(props.konnect_remote_authors)) {
            // console.log(props.konnect_remote_authors);
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
                        <GithubStream activities={props.github_activity}/>
                        <Inbox
                            postData={reference}
                            data={props.inbox}
                            author={props.author}
                            postFriendRequest={postFriendRequest}
                            postLiked={postLiked}
                            createComment={createComment}
                            getLikes={getLikes}
                        />
                    </div>
                    <div className='col-3 ps-5'>
                        <Friends
                            friends={_.uniqBy(props.friends.items, 'id')}
                            followers={_.uniqBy(props.followers.items, 'id')}
                            searchPeople={searchPeople}
                            searchPeopleResult={props.displayNameSearchResult.concat(props.remote_authors).concat(props.konnect_remote_authors)}
                            author={props.author}
                            postFriendRequest={postFriendRequest}
                            // searchRemoteAuthors={searchRemoteAuthors}
                            // remoteAuthors={props.remote_authors}
                        />
                        {/* <Followers followerCount={temp_follower_count} /> */}
                    </div>
                </div>
            </div>
        </div>
        
    )
}

const mapStateToProps = (state) => ({
    post: state.posts.post,
    author: state.users.user,
    author_id: state.users.user_id,
    displayNameSearchResult: state.users.displayNameSearchResult,
    inbox: state.posts.inbox,
    friendRequest: state.users.friendRequest,
    github_activity: state.users.github_activity,
    friends: state.users.friends,
    followers: state.users.followers,
    token: state.users.basic_token,
    like: state.posts.like,
    comment: state.posts.comment,
    remote_authors: state.users.remote_authors,
    konnect_remote_authors: state.users.konnect_remote_authors
});
  
export default connect(mapStateToProps, { postNewPost, postSearchDisplayName, getInbox, postFriendRequest, getGithub, getFriends, getFollowers, postLike, postComment, getLikes, getRemoteAuthors, postRemoteFriendRequest, postSearchDisplayNameRemote })(Feed);

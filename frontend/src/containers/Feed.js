import React from 'react';
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

import { postNewPost, getInbox } from "../actions/posts";
import { postSearchDisplayName, postFriendRequest } from '../actions/users';

import reference from '../dummyData/Dummy.FeedPosts.js';

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

    const temp_friends = {
        type: "friends",      
        items:[
            {
                "type":"author",
                "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Greg Johnson",
                "github": "http://github.com/gjohnson"
            },
            {
                "type":"author",
                "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Lara Croft",
                "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "github": "http://github.com/laracroft"
            }
        ]
    }

    const temp_people = {
        type: "friends",      
        items:[
            {
                "type":"author",
                "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Greg Johnson",
                "github": "http://github.com/gjohnson"
            },
            {
                "type":"author",
                "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Lara Croft",
                "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "github": "http://github.com/laracroft"
            }
        ]
    }

    const searchPeople = (displayName) => {
        props.postSearchDisplayName({displayName});
    }

    const postFriendRequest = (post, object_id) => {
        props.postFriendRequest(post, object_id);
    }
    

    const temp_follower_count = 10;

    const createNewPost = (post) => {
        // TEMPORARY DATA UNTIL API CHANGES
        const author_id = props.author.id.split('/')[4];
        const source = "http://lastplaceigotthisfrom.com/posts/yyyyy";
        const origin = "http://whereitcamefrom.com/posts/zzzzz";
        const unlisted = false;
        const description = 'this is a text post';

        const finalPost = {
            ...post,
            author_id,
            source,
            origin,
            unlisted,
            description
        }
        props.postNewPost(finalPost);
    }

    React.useEffect(() => {
        if (_.isEmpty(props.author)) {
            history.push("/login");
        } else {
            if (_.isEmpty(props.inbox)) {
                props.getInbox(props.author.id.split('/')[4]);
            }
            // console.log(props.inbox);
        }
        if (!_.isEmpty(props.post)) {
            // console.log(props.post);
        }
        if (!_.isEmpty(props.friendRequest)) {
            // console.log(props.friendRequest);
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
                        <Inbox postData={reference} data={props.inbox}/>
                    </div>
                    <div className='col-3 ps-5'>
                        <Friends friends={temp_friends.items} searchPeople={searchPeople} searchPeopleResult={props.displayNameSearchResult} author={props.author} postFriendRequest={postFriendRequest}/>
                        <Followers followerCount={temp_follower_count} />
                    </div>
                </div>
            </div>            
        </div>
        
    )
}

const mapStateToProps = (state) => ({
    post: state.posts.post,
    author: state.users.user,
    displayNameSearchResult: state.users.displayNameSearchResult,
    inbox: state.posts.inbox,
    friendRequest: state.users.friendRequest,
    
});
  
export default connect(mapStateToProps, { postNewPost, postSearchDisplayName, getInbox, postFriendRequest })(Feed);

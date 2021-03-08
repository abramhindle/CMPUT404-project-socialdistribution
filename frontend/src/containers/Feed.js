import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import _ from 'lodash';
import { connect } from "react-redux";
import { useHistory } from "react-router-dom";

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
        return _.filter(temp_people.items, person => person.displayName.includes(displayName));
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
        // if (_.isEmpty(props.author)) {
        //     history.push("/login");
        // }
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
                                history={props.history}
                            />
                        )}
                    </div>
                    <div className='col-3 ps-5'>
                        <Friends friends={temp_friends.items} searchPeople={searchPeople}/>
                        <Followers followerCount={temp_follower_count} />
                    </div>
                </div>
            </div>            
        </div>
        
    )
}

const mapStateToProps = (state) => ({
    post: state.posts.post,
    author: state.users.user
});
  
export default connect(mapStateToProps, { postNewPost })(Feed);
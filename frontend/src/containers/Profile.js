import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import _ from 'lodash';
import { connect } from "react-redux";

import ProfileInfo from '../components/ProfileInfo/ProfileInfo';
import Navbar from '../components/Navbar/Navbar';
import Inbox from '../components/Inbox/Inbox';
import Friends from '../components/Friends/Friends';
import Followers from '../components/Followers/Followers';

import reference from '../dummyData/Dummy.FeedPosts.js';

import { getPersonalPosts } from "../actions/posts";

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
    const postClasses = [classes.posts, 'col-9', 'pe-5']
    const container = ['container-fluid', classes.container];

    props.getPersonalPosts(props.author, props.token);

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
});
  
export default connect(mapStateToProps, {getPersonalPosts})(Profile);
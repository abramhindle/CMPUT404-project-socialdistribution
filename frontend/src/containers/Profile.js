import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import _ from 'lodash';
import { connect } from "react-redux";

import ProfileInfo from '../components/ProfileInfo/ProfileInfo';
import Navbar from '../components/Navbar/Navbar';
import Posts from '../components/Posts/Posts';
import Friends from '../components/Friends/Friends';
import Followers from '../components/Followers/Followers';

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


function Profile(props) {
    const classes = useStyles();
    const postClasses = [classes.posts, 'col-9', 'pe-5']
    const container = ['container-fluid', classes.container];

    const temp_posts = [
        {title: 'MyPost1'},
        {title: 'MyPost2'},
        {title: 'MyPost3'},
        {title: 'MyPost4'},
    ];

    const temp_friends = [
        {name: 'Friend1'},
        {name: 'Friend2'},
        {name: 'Friend3'},
        {name: 'Friend4'},
        {name: 'Friend5'},
    ];

    const temp_followers = [
        {name: 'Friend1'},
        {name: 'Friend2'},
        {name: 'Friend3'},
        {name: 'Friend4'},
        {name: 'Friend5'},
    ];

    const temp_follower_count = 10;

    const temp_profile = {
        type: 'author',
        id: 'http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e',
        host: 'http://127.0.0.1:5454/',
        displayName: 'Lara Croft',
        url:'http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e',
        github: 'http://github.com/laracroft'
    };


    return (
        <div 
            className={classes.feed}
        >
            <Navbar />
            <div className={container.join(' ')}>
                <div className='row align-items-start'>
                    <div className={postClasses.join(' ')}>
                        <hr></hr>
                        {/* <Posts posts={temp_posts} /> */}
                    </div>
                    <div className='col-3 ps-5'>
                        <ProfileInfo profile={props.author} numFollowers={temp_followers.length} numFriends={temp_friends.length}/>
                        <Friends friends={temp_friends}/>
                        <Followers followerCount={temp_follower_count} />
                    </div>
                </div>
            </div>
        </div>
        
    )
}

const mapStateToProps = (state) => ({
    author: state.users.user
});
  
export default connect(mapStateToProps, null)(Profile);
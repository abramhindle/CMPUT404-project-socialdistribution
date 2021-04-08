import React, {useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import _ from 'lodash';
import { useHistory } from "react-router-dom";
import { connect } from "react-redux";

import ProfileInfo from '../components/ProfileInfo/ProfileInfo';
import Navbar from '../components/Navbar/Navbar';

import { getPersonalPosts } from "../actions/posts";
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

    const initialLoad = () => {
        if (!loaded) {
            props.getPersonalPosts(props.author, props.token);
            setLoaded(true);
        }
    }

    React.useEffect(() => {
        if (_.isEmpty(props.author)) {
            history.push("/login");
        } else {
            initialLoad();
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
    personal_posts: state.posts.personal_posts
});
  
export default connect(mapStateToProps, {getPersonalPosts})(Profile);
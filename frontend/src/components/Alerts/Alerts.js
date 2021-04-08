import React, { Component, Fragment } from 'react';
import {
    POST_REGISTER,
    POST_LOGIN,
    POST_SEARCH_DISPLAYNAME,
    POST_FRIEND_REQUEST,
    GET_GITHUB,
    POST_UPDATE_PROFILE,
    GET_FRIENDS,
    GET_FOLLOWERS,
    GET_REMOTE_AUTHORS,
    GET_KONNECT_REMOTE_AUTHORS,
    GET_POST,
    POST_NEWPOST,
    GET_INBOX,
    POST_LIKE,
    POST_COMMENT,
    GET_LIKES,
    POST_SHARE_POST
} from '../../actions/types';

import { withAlert } from 'react-alert';
import { connect } from 'react-redux';

export class Alerts extends Component {
    componentDidUpdate(prevProps) {
        const { error, alert } = this.props;
        if (error !== prevProps.error) {
            if (error.status >= 400) {
                switch(error.origin) {
                    case POST_LOGIN:
                        return alert.error(`${error.status} Error: Login Failed`);
                    case GET_GITHUB:
                        return alert.error(`${error.status} Error: Github Not Found`);
                    case POST_REGISTER:
                        return alert.error(`${error.status} Error: Register Failed`);
                    case POST_SEARCH_DISPLAYNAME:
                        return alert.error(`${error.status} Error: Search Failed`);
                    case GET_KONNECT_REMOTE_AUTHORS:
                        return alert.error(`${error.status} Error: Searching Konnect Remote Failed`);
                    case POST_FRIEND_REQUEST:
                        return alert.error(`${error.status} Error: Friend Request Failed`);
                    case POST_UPDATE_PROFILE:
                        return alert.error(`${error.status} Error: Update Profile Failed`);        
                    case GET_FRIENDS:
                        return alert.error(`${error.status} Error: Getting Friends List Failed`);
                    case GET_FOLLOWERS:
                        return alert.error(`${error.status} Error: Getting Followers List Failed`);
                    case GET_POST:
                        return alert.error(`${error.status} Error: Getting Post Failed`);
                    case POST_NEWPOST:
                        return alert.error(`${error.status} Error: Creating New Post Failed`);
                    case GET_INBOX:
                        return alert.error(`${error.status} Error: Getting Inbox Failed`);
                    case POST_LIKE:
                        return alert.error(`${error.status} Error: Liking Post Failed`);
                    case POST_COMMENT:
                        return alert.error(`${error.status} Error: Commenting Failed`);
                    case GET_LIKES:
                        return alert.error(`${error.status} Error: Getting Post Likes Failed`);
                    case POST_SHARE_POST:
                        return alert.error(`${error.status} Error: Sharing Post Failed`);
                    default:
                        return alert.error(`${error.status} Error`);
                }
            } else if (error.status >= 200 && error.status < 300) {
                switch(error.origin) {
                    case POST_NEWPOST:
                        return alert.success(`Post Created`);
                    case POST_LIKE:
                        return alert.success(`Post Liked`);    
                    case POST_COMMENT:
                        return alert.success(`Comment Created`);
                    case POST_FRIEND_REQUEST:
                        return alert.success(`Friend Request Sent`);
                    case POST_SHARE_POST:
                        return alert.success(`Post Shared`);
                    default:
                        return alert.success(`Success`);
                }
            }
        }
    }

    render() {
        return <Fragment />;
    }
}

const mapStateToProps = state => ({
    error: state.errors
})

export default connect(mapStateToProps)(withAlert()(Alerts));
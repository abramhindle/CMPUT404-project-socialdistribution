import React from 'react';
import '../../styles/userHeader.css';
import Avatar from '@material-ui/core/Avatar';

const UserHeader = props => {
  console.log("user profile in header:", props.userProfile);
  return (
    <div id="user-header">
      <h1>Welcome!</h1>
      <hr />
      <div>
        <Avatar id="user-avatar">{props.userProfile.displayName.slice(0, 2)}</Avatar>
        <h1 id="name-info">Username: {props.userProfile.displayName} </h1>
      </div>
    </div>
  )
}

export default UserHeader

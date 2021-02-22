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
        <Avatar id="user-avatar">User</Avatar>
      </div>
    </div>
  )
}

export default UserHeader

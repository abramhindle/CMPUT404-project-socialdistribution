import React, { useContext, useEffect, useState } from "react";
import { UserContext } from "../UserContext";
import followService from "../services/follow";

const Friends = () => {
  const { user } = useContext(UserContext);
  const [ friends, setFriends ] = useState([])

  useEffect(() => async () => {
    const res = followService.followers(user);
    console.log(res)
  }, [user]);

  return (
    <div>
      friends
    </div>
  );
}

export default Friends;
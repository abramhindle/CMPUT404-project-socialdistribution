import { useSelector } from "react-redux";
import { get_friends_for_author } from "../api/follower_api";
import { useEffect, useState } from "react";
import { Box, Modal, Table } from "@mui/material";
import { post_inbox } from "../api/inbox_api";

const ShareModal = (props) => {
  const user = useSelector((state) => state.user);
  const [friends, setFriends] = useState(null);

  const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 400,
    bgcolor: "background.paper",
    boxShadow: 24,
    p: 4,
  };

  useEffect(() => {
    get_friends_for_author(user.id, setFriends);
  }, []);

  const shareToInbox = (authorId, post) => {
    post_inbox(authorId, post);
  };

  console.log("Friends", friends);

  return (
    friends && (
      <Modal {...props}>
        <Box sx={style}>
          {friends.items.map((friend) => (
            <div>
              {friend.displayName}
              <button onClick={() => shareToInbox(friend.id, props.post)}>
                Send
              </button>
            </div>
          ))}
        </Box>
      </Modal>
    )
  );
};

export default ShareModal;

import { useSelector } from "react-redux";
import { get_friends_for_author } from "../api/follower_api";
import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Input,
  Modal,
  Snackbar,
  Typography,
} from "@mui/material";
import { post_inbox } from "../api/inbox_api";
import "./share-modal.css";

const ShareModal = (props) => {
  const user = useSelector((state) => state.user);
  const [friends, setFriends] = useState(null);
  const [filter, setFilter] = useState("");

  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarServerity, setSnackbarServerity] = useState("");

  const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 400,
    bgcolor: "background.paper",
    boxShadow: 20,
    p: 4,
  };

  useEffect(() => {
    get_friends_for_author(user.id, setFriends);
  }, []);

  const filterFriend = (friend) => {
    return friend.displayName.toLowerCase().includes(filter.toLowerCase());
  };

  const handleClose = () => {
    setSnackbarOpen(false);
  };

  const inbox_result = (status) => {
    if (status === 202) {
      setSnackbarServerity("success");
    }
    if (status === 409) {
      setSnackbarServerity("error");
    }
    setSnackbarOpen(true);
  };

  return (
    <div>
      {friends && (
        <Modal {...props}>
          <Box sx={style}>
            <Input
              sx={{ width: "100%", mb: 5 }}
              name="filter"
              type="text"
              placeholder="Search friend"
              onChange={(e) => setFilter(e.target.value)}
              value={filter}
            />
            {friends.items
              .filter((friend) => filterFriend(friend))
              .map((friend) => (
                <div className="friend-row">
                  <img id="profile-image" src={friend.profileImage} />
                  <Typography id="display-name">
                    {friend.displayName}
                  </Typography>
                  <Button
                    id="send-button"
                    onClick={() =>
                      post_inbox(friend.id, props.post, inbox_result)
                    }
                  >
                    Send
                  </Button>
                </div>
              ))}
          </Box>
        </Modal>
      )}
      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        open={snackbarOpen}
        autoHideDuration={4000}
        onClose={handleClose}
      >
        <Alert
          onClose={handleClose}
          severity={snackbarServerity}
          sx={{ width: "100%" }}
        >
          {snackbarServerity === "success"
            ? "Successfully sent to the inbox!"
            : "Failed! The author already have the post in the inbox!"}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default ShareModal;

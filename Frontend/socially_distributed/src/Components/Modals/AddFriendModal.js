import React, { useState } from "react";
import { Avatar, Button, Modal, Input, InputGroup } from "rsuite";
import { ToastContainer, toast } from "react-toastify";
import SearchIcon from "@rsuite/icons/Search";
import axios from "axios";
import { getAuthorId } from "../utils/auth";

function ADD_FRIEND_MODAL({ open, handleClose }) {
	const [displayName, setName] = useState("");
	const [foreign_author_id, setId] = useState("");
	const [isFriends, setIsFriends] = useState("");

	const handleAddFriendClick = () => {
		// url = `authors/authors/${AUTHOR_ID}/followers/${foreign_author_id}/`;
		// axios({ method: "put", url: url });
		const url = `authors/${displayName}`;
		const AUTHOR_ID = getAuthorId();
		axios({ method: "get", url: url }).then((res) => {
			if (res.status === 200) {
				console.log(res.data);
				setId(res.data);
			}
		});
		if (checkFriends(foreign_author_id, AUTHOR_ID)) {
			notifyAlreadyFriends();
		}

		handleClose();
	};

	const notifyAlreadyFriends = () =>
		toast.success("success", {
			position: "top-right",
			autoClose: 5000,
			hideProgressBar: false,
			closeOnClick: true,
			pauseOnHover: true,
			draggable: true,
			progress: undefined,
			theme: "light",
		});

	const checkFriends = (AUTHOR_ID, foreign_author_id) => {
		const data = "";
		console.log(AUTHOR_ID);
		const url = `authors/authors/${AUTHOR_ID}/followers/${foreign_author_id}/`;
		axios({ method: "get", url: url }).then((res) => {
			if (Object.keys(res.data).length === 0) {
				return false;
			} else {
				return true;
			}
		});
	};

	return (
		<Modal open={open} onClose={handleClose}>
			<Modal.Header>
				<h3>Add Friend</h3>
			</Modal.Header>
			<Modal.Body>
				<InputGroup>
					<Input
						placeholder={"display name"}
						value={displayName}
						onChange={(e) => setName(e)}
					/>
					<InputGroup.Addon>
						<SearchIcon />
					</InputGroup.Addon>
				</InputGroup>
			</Modal.Body>
			<Modal.Footer>
				<Button onClick={handleAddFriendClick} appearance="primary">
					Add Friend
				</Button>
				<ToastContainer
					position="top-right"
					autoClose={5000}
					hideProgressBar={false}
					newestOnTop={false}
					closeOnClick
					rtl={false}
					pauseOnFocusLoss
					draggable
					pauseOnHover
					theme="light"
				/>
				{/* Same as */}
				<ToastContainer />
			</Modal.Footer>
		</Modal>
	);
}

export default ADD_FRIEND_MODAL;

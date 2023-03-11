import React, { useState } from "react";
import { Avatar, Button, Modal, Input, InputGroup } from "rsuite";
import SearchIcon from "@rsuite/icons/Search";

function ADD_FRIEND_MODAL({ open, handleClose }) {
	const handleAddFriendClick = () => {
		handleClose();
	};

	return (
		<Modal open={open} onClose={handleClose}>
			<Modal.Header>
				<h3>Add Friend</h3>
			</Modal.Header>
			<Modal.Body>
				<InputGroup>
					<Input placeholder={"display name"} />
					<InputGroup.Addon>
						<SearchIcon />
					</InputGroup.Addon>
				</InputGroup>
			</Modal.Body>
			<Modal.Footer>
				<Button onClick={handleAddFriendClick} appearance="primary">
					Add Friend
				</Button>
			</Modal.Footer>
		</Modal>
	);
}

export default ADD_FRIEND_MODAL;

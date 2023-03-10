import React, { useState } from "react";
import { Avatar } from "rsuite";

function ADD_FRIEND_MODAL() {
	// make a get request to get author and every post the author made and comments on the posts
	// make a get request to get all the friends of an author
	cosnt[(open, setOpen)] = useState(false);

	const handleAddFriendClick = () => {};

	const handleClose = () => {
		setOpen(false);
	};

	return (
		<Modal open={open} onClose={handleClose}>
			<Modal.Header>
				<h3>Add Friend</h3>
			</Modal.Header>
			<Modal.Body>
				<InputGroup>
					<Input placeholder={"JhonDoe"} />
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

import React, { useState } from "react";
import {
	Avatar,
	Button,
	Modal,
	Input,
	InputGroup,
	useToaster,
	Message,
} from "rsuite";
import { ToastContainer, toast } from "react-toastify";
import SearchIcon from "@rsuite/icons/Search";
import axios from "axios";
import { getAuthorId } from "../utils/auth";

function ADD_FRIEND_MODAL({ open, handleClose }) {
	const [displayName, setName] = useState("");
	const [foreign_author, setForeign] = useState({});
	const toaster = useToaster();

	async function sendreq(id) {
		console.log(id);
		const AUTHOR_ID = getAuthorId(null);
		const url2 = `authors/${id}/inbox`;
		const params = {
			type: "Follow",
			actor: {
				id: AUTHOR_ID,
			},
			object: {
				id: foreign_author,
			},
		};
		return axios({ method: "post", url: url2, data: params })
			.then((res) => {
				console.log(res.data);
				toaster.push(
					<Message type="success">Friend Request Sent</Message>,
					{
						placement: "topEnd",
						duration: 5000,
					}
				);
			})
			.catch((err) => console.log(err.data));
	}

	// This function gets the author info and sends the friend req to the author
	async function handleAddFriendClick() {
		// url = `authors/authors/${AUTHOR_ID}/followers/${foreign_author_id}/`;
		// axios({ method: "put", url: url });
		const url = `authors/displayName/${displayName}`;
		await axios({ method: "get", url: url }).then(async (res) => {
			if (res.status === 200) {
				await sendreq(res.data.id);
			}
		});
		handleClose();
	}

	// async function checkFriends(AUTHOR_ID, foreign_author_id) {
	// 	const data = "";
	// 	console.log(AUTHOR_ID);
	// 	const url = `authors/authors/${AUTHOR_ID}/followers/${foreign_author_id}`;
	// 	await axios({ method: "get", url: url }).then((res) => {
	// 		if (Object.keys(res.data).length === 0) {
	// 			return false;
	// 		} else {
	// 			return true;
	// 		}
	// 	});
	// }

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
			</Modal.Footer>
		</Modal>
	);
}

export default ADD_FRIEND_MODAL;

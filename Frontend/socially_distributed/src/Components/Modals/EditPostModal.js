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
import CREATEPOST from "../Post/CreatePost";
import EDITPOST from "../Post/EditPost";

function EDITPOSTMODAL({ open, obj, handleClose }) {
	const [displayName, setName] = useState("");
	const [foreign_author, setForeign] = useState({});
	const toaster = useToaster();

	return (
		<Modal open={open} onClose={handleClose}>
			<Modal.Header>
				<h3>Edit Post</h3>
			</Modal.Header>
			<Modal.Body>
				<EDITPOST obj={obj}> </EDITPOST>
			</Modal.Body>
			<Modal.Footer>
				<Button appearance="primary">Confirm Edit</Button>
			</Modal.Footer>
		</Modal>
	);
}

export default EDITPOSTMODAL;

import React, { useState } from "react";
import {
	Avatar,
	ButtonGroup,
	Panel,
	Button,
	Navbar,
	Nav,
	InputGroup,
	Input,
	Modal,
} from "rsuite";
import FRIENDS from "./Friends";
import AUTHORPOSTS from "./AuthorPosts";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import SearchIcon from "@rsuite/icons/Search";
import ADD_FRIEND_MODAL from "../Modals/AddFriendModal";

function PROFILE() {
	const [posts, setPosts] = React.useState(true);
	const [appearance, setAppearance] = React.useState({
		posts: "primary",
		friends: "ghost",
	});
	const [open, setOpen] = useState(false);

	const handlePostsBtnClick = () => {
		setPosts(true);
		setAppearance({ posts: "primary", friends: "ghost" });
	};

	const handleFriendsBtnClick = () => {
		setPosts(false);
		setAppearance({ posts: "ghost", friends: "primary" });
	};

	const [curPage, setCurPage] = useState("profile");
	let navigate = useNavigate();

	const handleInboxClick = () => {
		navigate("/");
	};

	const handleLogoutClick = () => {
		const token = localStorage.getItem("token");

		let reqInstance = axios.create({
			headers: { "X-CSRFToken": token },
		});
		reqInstance.post("accounts/logout/").then((res) => {
			if (res.status === 200) {
				navigate("/login");
			}
		});
	};

	// make a get request to get author and every post the author made and comments on the posts
	// make a get request to get all the friends of an author
	const handleAddFriendClick = () => {};

	const handleOpen = () => {
		setOpen(true);
	};

	const handleClose = () => {
		setOpen(false);
	};

	return (
		<div style={{ padding: "10px", width: "60%", margin: "auto" }}>
			<Navbar>
				<Navbar.Brand>Socially Distrubted</Navbar.Brand>
				<Nav pullRight>
					<Nav.Item onClick={handleLogoutClick}>Logout</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleInboxClick}>Inbox</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item>Profile</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleOpen}>Add Friend</Nav.Item>
				</Nav>
			</Navbar>
			<Panel shaded>
				<Avatar
					style={{ float: "left" }}
					circle
					src="https://avatars.githubusercontent.com/u/12592949"
					size="lg"
				></Avatar>
				<h2 style={{ marginLeft: "10px", float: "left" }}>Author</h2>

				<ButtonGroup
					justified
					style={{ paddingTop: "10px", marginBottom: "5px" }}
				>
					<Button
						style={{ textAlign: "center" }}
						appearance={appearance["posts"]}
						onClick={handlePostsBtnClick}
					>
						Posts
					</Button>
					<Button
						style={{ textAlign: "center" }}
						appearance={appearance["friends"]}
						onClick={handleFriendsBtnClick}
					>
						Friends
					</Button>
				</ButtonGroup>
				{posts ? <AUTHORPOSTS /> : <FRIENDS />}
			</Panel>
		</div>
	);
}

export default PROFILE;

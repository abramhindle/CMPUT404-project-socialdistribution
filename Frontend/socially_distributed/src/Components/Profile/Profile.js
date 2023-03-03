import React, { useState } from "react";
import { Avatar, ButtonGroup, Panel, Button, Navbar, Nav } from "rsuite";
import FRIENDS from "./Friends";
import AUTHORPOSTS from "./AuthorPosts";
import { useNavigate } from "react-router-dom";

function PROFILE() {
	const [posts, setPosts] = React.useState(true);
	const [appearance, setAppearance] = React.useState({
		posts: "primary",
		friends: "ghost",
	});

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

	// make a get request to get author and every post the author made and comments on the posts
	// make a get request to get all the friends of an author

	return (
		<div style={{ width: "50%", margin: "auto" }}>
			<Navbar>
				<Navbar.Brand>Socially Distrubted</Navbar.Brand>
				<Nav pullRight>
					<Nav.Item onClick={handleInboxClick}>Inbox</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item>Profile</Nav.Item>
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

import React, { useEffect, useState, useLayoutEffect } from "react";
// Component Imports
import { Navbar, Nav, Panel, useToaster, Message } from "rsuite";
import { useNavigate } from "react-router-dom";
import { reqInstance } from "../utils/axios";
import FOLLOWREQ from "../Post/FollowReq";
import LIKEINBOX from "../Post/LikeInbox";
import ADD_FRIEND_MODAL from "../Modals/AddFriendModal";
import POST from "../Post/Post";
import COMMENTINBOX from "../Post/CommentInbox";
import { unsetCurrentUser } from "../utils/auth";

function EXPLORE() {
	const [inbox, setInbox] = useState([]);
	const [curPage, setCurPage] = useState("inbox");
	const [open, setOpen] = useState(false);
	let navigate = useNavigate();

	// Get the inbox
	useEffect(() => {
		if (!localStorage.getItem("loggedIn")) {
			navigate("/login");
		} else {
			const url = `posts/public/`;
			reqInstance({ method: "get", url: url }).then((res) => {
				console.log(res);
				setInbox(res.data);
			});
		}
	}, []);

	const item = (obj) => {
		if (obj.type === "post") {
			return <POST key={obj.id} postobj={obj} />;
		}
		if (obj.type === "Like") {
			return <LIKEINBOX key={obj.id} likeobj={obj} />;
		}
		if (obj.type === "Follow") {
			return <FOLLOWREQ key={obj.id} obj={obj} />;
		}
		if (obj.type === "comment") {
			return <COMMENTINBOX key={obj.id} obj={obj} />;
		}
	};

	const handleProfileClick = () => {
		if (curPage !== "profile") {
			setCurPage("profile");
			navigate("/profile");
		}
	};

	const handleExploreClick = () => {
		if (curPage !== "explore") {
			setCurPage("explore");
			navigate("/explore");
		}
	};

	async function handleLogoutClick() {
		reqInstance.post("dlogout/").then((res) => {
			if (res.status === 200) {
				unsetCurrentUser();
				navigate("/login");
			}
		});
	}

	const handleOpen = () => {
		setOpen(true);
	};

	const handleModalClose = () => {
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
					<Nav.Menu title="Inbox"></Nav.Menu>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleProfileClick}>Profile</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleExploreClick}>Explore</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleOpen}>Add Friend</Nav.Item>
				</Nav>
			</Navbar>
			{inbox.map((obj) => item(obj))}
			<ADD_FRIEND_MODAL open={open} handleClose={handleModalClose} />
		</div>
	);
}

export default EXPLORE;

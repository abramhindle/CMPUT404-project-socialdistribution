import React, { useEffect, useState } from "react";
import {
	ButtonGroup,
	Panel,
	Button,
	Navbar,
	Nav,
	Input,
	InputGroup,
	Message,
	useToaster,
} from "rsuite";
import FRIENDS from "./Friends";
import AUTHORPOSTS from "./AuthorPosts";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import ADD_FRIEND_MODAL from "../Modals/AddFriendModal";
import { getAuthorId, getCsrfToken, getProfileImageUrl } from "../utils/auth";
import PROFILEIMAGE from "./ProfileImage";

function PROFILE() {
	const [posts, setPosts] = React.useState(true);
	const [appearance, setAppearance] = React.useState({
		posts: "primary",
		friends: "ghost",
	});
	const [author, setAuthor] = useState({});
	let navigate = useNavigate();
	const [open, setOpen] = useState(false);
	const [imageurl, setImage] = useState("");
	const [giturl, setGiturl] = useState("");
	let toaster = useToaster();

	useEffect(() => {
		if (!localStorage.getItem("loggedIn")) {
			navigate("/login");
		} else {
			setImage(getProfileImageUrl);
			setAuthor(localStorage.getItem("user"));
		}
	}, []);

	const handlePostsBtnClick = () => {
		setPosts(true);
		setAppearance({ posts: "primary", friends: "ghost" });
	};

	const handleFriendsBtnClick = () => {
		setPosts(false);
		setAppearance({ posts: "ghost", friends: "primary" });
	};

	const [curPage, setCurPage] = useState("profile");

	const handleInboxClick = () => {
		navigate("/");
	};

	async function handleLogoutClick() {
		await getCsrfToken();
		const token = localStorage.getItem("token");

		let reqInstance = axios.create({
			headers: { "X-CSRFToken": token },
		});
		reqInstance.post("accounts/logout/").then((res) => {
			if (res.status === 200) {
				navigate("/login");
			}
		});
	}

	// make a get request to get author and every post the author made and comments on the posts
	// make a get request to get all the friends of an author

	const handleOpen = () => {
		setOpen(true);
	};

	const handleModalClose = () => {
		setOpen(false);
	};

	const notifySuccessPost = (message) => {
		toaster.push(<Message type="success">{message}</Message>, {
			placement: "topEnd",
			duration: 5000,
		});
	};

	const notifyFailedPost = (error) => {
		toaster.push(<Message type="error">{error}</Message>, {
			placement: "topEnd",
			duration: 5000,
		});
	};

	async function handleGitClick() {
		const author_id = getAuthorId(null);
		const url = `authors/${author_id}/`;
		axios({ method: "post", url: url, data: { github: giturl } })
			.then((res) => {
				notifySuccessPost("successfully upadated the giturl");
			})
			.error((err) => notifyFailedPost(err));
	}

	async function handleImageClick() {
		const author_id = getAuthorId(null);
		const url = `authors/${author_id}/`;
		axios({
			method: "post",
			url: url,
			data: { profileImage: imageurl },
		})
			.then((res) => {
				notifySuccessPost("successfully upadated the profile url");
			})
			.error((err) => notifyFailedPost(err));
	}

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
				<PROFILEIMAGE size="lg" />
				<h2 style={{ marginLeft: "10px", float: "left" }}>
					{author["displayName"]}
				</h2>

				<InputGroup inside style={{ marginTop: "5px" }}>
					<Input
						placeholder="Profile Image Url"
						value={imageurl}
						onChange={(e) => setImage(e)}
					/>
					<InputGroup.Button onClick={handleImageClick}>
						Save
					</InputGroup.Button>
				</InputGroup>

				<InputGroup inside style={{ marginTop: "5px" }}>
					<Input
						placeholder="Github Url"
						value={giturl}
						onChange={(e) => setGiturl(e)}
					/>
					<InputGroup.Button onClick={handleGitClick}>
						Save
					</InputGroup.Button>
				</InputGroup>

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
			<ADD_FRIEND_MODAL open={open} handleClose={handleModalClose} />
		</div>
	);
}

export default PROFILE;

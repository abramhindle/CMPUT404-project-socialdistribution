import React, { useEffect, useState } from "react";
// Component Imports
import POST from "./Post";
import CREATEPOST from "./CreatePost";
import LIKEINBOX from "./LikeInbox";
import { Navbar, Nav, Panel, Modal, Button, InputGroup, Input } from "rsuite";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import FOLLOWREQ from "./FollowReq";
import ADD_FRIEND_MODAL from "../Modals/AddFriendModal";

function INBOX() {
	const inbox = {
		type: "inbox",
		author: "http://127.0.0.1:5454/authors/c1e3db8ccea4541a0f3d7e5c75feb3fb",
		items: [
			{
				type: "post",
				title: "A Friendly post title about a post about web dev",
				id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
				source: "http://lastplaceigotthisfrom.com/posts/yyyyy",
				origin: "http://whereitcamefrom.com/posts/zzzzz",
				description: "This post discusses stuff -- brief",
				contentType: "text/plain",
				content:
					"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
				author: {
					type: "author",
					id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					host: "http://127.0.0.1:5454/",
					displayName: "Lara Croft",
					url: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					github: "http://github.com/laracroft",
					profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
				},
				categories: ["web", "tutorial"],
				comments:
					"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
				published: "2015-03-09T13:07:04+00:00",
				visibility: "FRIENDS",
				unlisted: false,
			},
			{
				type: "Follow",
				summary: "Greg wants to follow Lara",
				actor: {
					type: "author",
					id: "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
					url: "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
					host: "http://127.0.0.1:5454/",
					displayName: "Greg Johnson",
					github: "http://github.com/gjohnson",
					profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
				},
				object: {
					type: "author",
					// # ID of the Author
					id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					// # the home host of the author
					host: "http://127.0.0.1:5454/",
					// # the display name of the author
					displayName: "Lara Croft",
					// # url to the authors profile
					url: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					// # HATEOS url for Github API
					github: "http://github.com/laracroft",
					// # Image from a public domain
					profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
				},
			},
			{
				"@context": "https://www.w3.org/ns/activitystreams",
				summary: "Lara Croft Likes your post",
				type: "Like",
				author: {
					type: "author",
					id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					host: "http://127.0.0.1:5454/",
					displayName: "Lara Croft",
					url: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					github: "http://github.com/laracroft",
					profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
				},
				object: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
			},
			{
				type: "post",
				title: "DID YOU READ MY POST YET?",
				id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/999999983dda1e11db47671c4a3bbd9e",
				source: "http://lastplaceigotthisfrom.com/posts/yyyyy",
				origin: "http://whereitcamefrom.com/posts/zzzzz",
				description: "Whatever",
				contentType: "text/plain",
				content: "Are you even reading my posts Arjun?",
				author: {
					type: "author",
					id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					host: "http://127.0.0.1:5454/",
					displayName: "Lara Croft",
					url: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					github: "http://github.com/laracroft",
					profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
				},
				categories: ["web", "tutorial"],
				comments:
					"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
				published: "2015-03-09T13:07:04+00:00",
				visibility: "FRIENDS",
				unlisted: false,
			},
			{
				"@context": "https://www.w3.org/ns/activitystreams",
				summary: "Lara Croft Likes your post",
				type: "Like",
				author: {
					type: "author",
					id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					host: "http://127.0.0.1:5454/",
					displayName: "Lara Croft",
					url: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					github: "http://github.com/laracroft",
					profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
				},
				object: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
			},
		],
	};

	const item = (obj) => {
		if (obj.type === "post") {
			return <POST postobj={obj} />;
		}
		if (obj.type === "Like") {
			return <LIKEINBOX likeobj={obj} />;
		}
		if (obj.type === "Follow") {
			return <FOLLOWREQ obj={obj} />;
		}
	};

	// we need make a query to get all the postid that need to be in the author's stream
	// useEffect();

	const [curPage, setCurPage] = useState("inbox");
	const [open, setOpen] = useState(false);
	let navigate = useNavigate();

	useEffect(() => {
		// console.log(localStorage.getItem("token"));
		// console.log(localStorage.getItem("user"));
		// console.log(localStorage.getItem("loggedIn"));
	});

	const handleProfileClick = () => {
		if (curPage !== "profile") {
			console.log(curPage);
			setCurPage("profile");
			navigate("profile");
		}
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
					<Nav.Menu title="Inbox">
						<Nav.Item style={{ color: "red" }}>
							Clear Inbox
						</Nav.Item>
					</Nav.Menu>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleProfileClick}>Profile</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleOpen}>Add Friend</Nav.Item>
				</Nav>
			</Navbar>
			<Panel bordered header="New Post" collapsible>
				<CREATEPOST></CREATEPOST>
			</Panel>
			{inbox.items.map((obj) => item(obj))}
			{/* <Modal open={open} onClose={handleClose}>
				<Modal.Header>
					<div>Add Friend</div>
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
			</Modal> */}
			<ADD_FRIEND_MODAL open={open} handleClose={handleModalClose} />
		</div>
	);
}

export default INBOX;

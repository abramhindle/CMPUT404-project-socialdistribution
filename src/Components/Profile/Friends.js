import React, { useLayoutEffect, useState, IconButton, Message, useToaster } from "react";
import { Avatar } from "rsuite";
import axios from "axios";
import { getAuthorId } from "../utils/auth";
import { useNavigate } from "react-router-dom";
import TrashIcon from "@rsuite/icons/Trash";
import PROFILEIMAGE from "./ProfileImage";

function FRIENDS() {
	const [friends, setFriends] = useState({ items: [] });
	let navigate = useNavigate();
	// const toaster = useToaster();

	useLayoutEffect(() => {
		if (!localStorage.getItem("loggedIn")) {
			navigate("/login");
		} else {
			const AUTHOR_ID = getAuthorId(null);
			const url = `authors/${AUTHOR_ID}/followers/`;
			axios({
				method: "get",
				url: url,
			}).then((res) => {
				setFriends(res.data);
			});
		}
	}, []);

	async function handleDeleteFollower(obj) {
		const author_id = getAuthorId(null);
		const follower_id = getAuthorId(obj.id);
		const url = `posts/authors/${author_id}/followers/${follower_id}/`;
		axios({ method: "delete", url: url })
			.then((res) => {
				if (res.status === 204) {
					notifySuccessPost();
				} else {
					notifyFailedPost(res.data);
				}
			})
			.catch((err) => console.log(err));
	}
	const notifySuccessPost = () => {
		// toaster.push(
		// 	<Message type="success">Successfully removed this follower</Message>,
		// 	{
		// 		placement: "topEnd",
		// 		duration: 5000,
		// 	}
		// );
	};
	const notifyFailedPost = (error) => {
		// toaster.push(<Message type="error">{error}</Message>, {
		// 	placement: "topEnd",
		// 	duration: 5000,
		// });
	};

	const item = (obj) => {
		return (
			<div
				key={obj.id}
				style={{
					height: "50px",
					border: "0.5px solid lightgrey",
					borderRadius: "10px",
					marginTop: "5px",
				}}
			>
				<div style={{ padding: "5px" }}>
					<Avatar
						style={{ float: "left", marginBotton: "5px" }}
						circle
						src={obj["profileImage"]} //{follow[actor][profileImage]} replace this with the actors profile image url
					/>
					<h5
						style={{
							marginLeft: "10px",
							float: "left",
						}}
					>
						{obj["displayName"]}
					</h5>
				</div>

			</div>
		);
	};

	return <div>{friends.items.map((obj) => item(obj))}</div>;
}

export default FRIENDS;

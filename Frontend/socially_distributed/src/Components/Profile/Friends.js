import React, { useLayoutEffect, useState } from "react";
import { Avatar } from "rsuite";
import axios from "axios";

function FRIENDS() {
	// make a get request to get author and every post the author made and comments on the posts
	// make a get request to get all the friends of an author
	const [friends, setFriends] = useState({ items: [] });

	useLayoutEffect(() => {
		const author = JSON.parse(localStorage.getItem("user"));
		const len = 36;
		const AUTHOR_ID = author.id.slice(
			author.id.length - len,
			author.id.length
		);
		const url = `authors/authors/${AUTHOR_ID}/followers/`;
		axios({
			method: "get",
			url: url,
		}).then((res) => {
			console.log(res.data);
			setFriends(res.data);
		});
	}, []);

	const item = (obj) => {
		return (
			<div
				style={{
					height: "50px",
					border: "0.5px solid lightgrey",
					borderRadius: "10px",
					marginTop: "5px",
				}}
			>
				<div style={{ padding: "5px" }}>
					<Avatar
						style={{ float: "left" }}
						circle
						src="https://avatars.githubusercontent.com/u/12592949"
					></Avatar>
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

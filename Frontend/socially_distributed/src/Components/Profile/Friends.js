import React, { useState } from "react";
import { Avatar } from "rsuite";

function FRIENDS() {
	// make a get request to get author and every post the author made and comments on the posts
	// make a get request to get all the friends of an author
	const friends = {
		type: "followers",
		items: [
			{
				type: "author",
				id: "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
				url: "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
				host: "http://127.0.0.1:5454/",
				displayName: "Greg Johnson",
				github: "http://github.com/gjohnson",
				profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
			},
			{
				type: "author",
				id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
				host: "http://127.0.0.1:5454/",
				displayName: "Lara Croft",
				url: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
				github: "http://github.com/laracroft",
				profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
			},
		],
	};

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

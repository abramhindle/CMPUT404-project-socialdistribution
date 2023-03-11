import React, { useState } from "react";
import { Button, Avatar, Panel } from "rsuite";
import axios from "axios";
// Component Imports

// {
//     type: "Follow",
//     summary: "Greg wants to follow Lara",
//     actor: {
//         type: "author",
//         id: "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
//         url: "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
//         host: "http://127.0.0.1:5454/",
//         displayName: "Greg Johnson",
//         github: "http://github.com/gjohnson",
//         profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
//     },
//     object: {
//         type: "author",
//         // # ID of the Author
//         id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
//         // # the home host of the author
//         host: "http://127.0.0.1:5454/",
//         // # the display name of the author
//         displayName: "Lara Croft",
//         // # url to the authors profile
//         url: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
//         // # HATEOS url for Github API
//         github: "http://github.com/laracroft",
//         // # Image from a public domain
//         profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
//     },
// },

function FOLLOWREQ({ obj }) {
	const [follow, setFollow] = useState(obj);

	return (
		<Panel
			bordered
			style={{
				marginBottom: "5px",
			}}
		>
			<div>
				<Avatar
					style={{ float: "left", marginBotton: "5px" }}
					circle
					src="https://avatars.githubusercontent.com/u/12592949" //{follow[actor][profileImage]} replace this with the actors profile image url
				/>
				<div
					style={{
						marginLeft: "50px",
						fontFamily: "Times New Roman",
						fontWeight: "bold",
						fontSize: "20px",
					}}
				>
					{follow["summary"]}
				</div>
			</div>

			<div style={{ marginTop: "10px" }}>
				<Button block appearance="primary">
					Accept
				</Button>
				<Button block>Deny</Button>
			</div>
		</Panel>
	);
}

export default FOLLOWREQ;

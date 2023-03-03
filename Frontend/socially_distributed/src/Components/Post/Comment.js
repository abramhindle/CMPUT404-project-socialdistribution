import React, { useState, useEffect } from "react";
import { Input, InputGroup, Panel } from "rsuite";
import { Scrollbars } from "react-custom-scrollbars-2";
// Component Imports

function COMMENTS({ postobj }) {
	const commentOBj = {
		type: "comments",
		page: 1,
		size: 5,
		post: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
		id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
		comments: [
			{
				type: "comment",
				author: {
					type: "author",
					// ID of the Author (UUID)
					id: "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
					// # url to the authors information
					url: "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
					host: "http://127.0.0.1:5454/",
					displayName: "Greg Johnson",
					// # HATEOS url for Github API
					github: "http://github.com/gjohnson",
					// # Image from a public domain
					profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
				},
				comment: "Sick Olde English",
				contentType: "text/markdown",
				// # ISO 8601 TIMESTAMP
				published: "2015-03-09T13:07:04+00:00",
				// # ID of the Comment (UUID)
				id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
			},
			{
				type: "comment",
				author: {
					type: "author",
					// ID of the Author (UUID)
					id: "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
					// # url to the authors information
					url: "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
					host: "http://127.0.0.1:5454/",
					displayName: "Greg Johnson",
					// # HATEOS url for Github API
					github: "http://github.com/gjohnson",
					// # Image from a public domain
					profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
				},
				comment: "Sick Olde English",
				contentType: "text/markdown",
				// # ISO 8601 TIMESTAMP
				published: "2015-03-09T13:07:04+00:00",
				// # ID of the Comment (UUID)
				id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
			},
		],
	};
	const [new_comment, set_new_comment] = useState("");

	return (
		<div>
			{commentOBj.comments.map((obj) => (
				<div
					style={{
						width: "100%",
						border: "0.5px solid lightgrey",
						padding: "2px",
						marginBottom: "2px",
					}}
				>
					<text
						style={{
							marginLeft: "10px",
							fontWeight: "bold",
						}}
					>
						{obj["author"]["displayName"]}
					</text>
					<text>: {obj["comment"]}</text>
				</div>
			))}

			<InputGroup inside style={{ marginTop: "5px" }}>
				<Input
					onChange={(e) => set_new_comment(e)}
					value={new_comment}
					placeholder="comment"
				/>
				<InputGroup.Button>Submit</InputGroup.Button>
			</InputGroup>
		</div>
	);
}

export default COMMENTS;

import React, { useState, useEffect, useLayoutEffect } from "react";
import { Input, InputGroup, Panel } from "rsuite";
import { Scrollbars } from "react-custom-scrollbars-2";
import axios from "axios";
// Component Imports

function COMMENTS({ postobj }) {
	const [commentObj, setCommentObj] = useState({ comments: [] });
	const [postObj, setPostObj] = useState(postobj);
	const [new_comment, set_new_comment] = useState("");

	const getComments = (url) => {
		axios({ method: "get", url: url })
			.then((res) => {
				setCommentObj(res.data);
			})
			.catch((err) => console.log(err));
	};

	useLayoutEffect(() => {
		const author = JSON.parse(localStorage.getItem("user"));
		const len = 36;
		const author_id = author.id.slice(
			author.id.length - len,
			author.id.length
		);
		const post_id = postObj.id.slice(
			postObj.id.length - len,
			postObj.id.length
		);
		console.log(post_id);
		getComments(`posts/authors/${author_id}/posts/${post_id}/comments`);
	}, []);

	const handleSubmitClick = () => {
		const author = JSON.parse(localStorage.getItem("user"));
		const len = 36;
		const author_id = author.id.slice(
			author.id.length - len,
			author.id.length
		);
		const post_id = postObj.id.slice(
			postObj.id.length - len,
			postObj.id.length
		);
		const params = { comment: new_comment };
		const url = `posts/authors/${author_id}/posts/${post_id}/comments/`;
		axios({ method: "post", url: url, data: params })
			.then((res) => {
				if (res.status === 200) {
					getComments(url);
					set_new_comment("");
				}
			})
			.catch((err) => console.log(err));
	};

	return (
		<div>
			{commentObj.comments.map((obj) => (
				<div
					key={obj.id}
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
				<InputGroup.Button onClick={handleSubmitClick}>
					Submit
				</InputGroup.Button>
			</InputGroup>
		</div>
	);
}

export default COMMENTS;

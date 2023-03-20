import React, { useState, useEffect, useLayoutEffect } from "react";
import { Input, InputGroup } from "rsuite";
import axios from "axios";
import { getAuthorId } from "../utils/auth";
// Component Imports
import COMMENTLIKE from "./LikeComment";

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
		const author_id = getAuthorId(null);
		const post_id = getAuthorId(postObj.id);
		getComments(`posts/authors/${author_id}/posts/${post_id}/comments`);
	}, []);

	const handleSubmitClick = () => {
		const FAID = getAuthorId(postObj.author["id"]);
		const author_id = getAuthorId(null);
		const post_id = getAuthorId(postObj.id);
		const params = { comment: new_comment, author_id: author_id };
		const url = `posts/authors/${FAID}/posts/${post_id}/comments/`;
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
					{/* <text>{obj.id}</text> */}
					<text
						style={{
							marginLeft: "10px",
							fontWeight: "bold",
						}}
					>
						{obj["author"]["displayName"]}
					</text>
					<text>: {obj["comment"]}</text>
					<COMMENTLIKE obj={obj.id} />
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

import React, { useState, useEffect } from "react";
import { Input, InputGroup, Panel } from "rsuite";
import { Scrollbars } from "react-custom-scrollbars-2";
import axios from "axios";

// Component Imports

function LIKE({ likeobj }) {
	const [like, set_like] = useState(likeobj);
	const [postObj, setPostObj] = useState(postobj);
	const [new_like, set_new_like] = useState("");

	// const getLike = (url) => {
	// 	axios({method: "get", url: url})
	// 		.then((res) => {
	// 			set_like(res.data)
	// 		})
	// 		.catch((err) => console.log(err));
	// };
	// const getComments = (url) => {
	// 	axios({ method: "get", url: url })
	// 		.then((res) => {
	// 			setCommentObj(res.data);
	// 		})
	// 		.catch((err) => console.log(err));
	// };

	const handleSubmitClick = () => {
		const author = JSON.parse(localStorage.getItem("user"));
		const len = 36
		const author_id = author.id.slice(
			author.id.length - len,
			author.id.length
		);
		const post_id = postObj.id.slice(
			postObj.id.length - len,
			postObj.id.length
		);
		//const params = { ? };
		const url = `posts/authors/${author_id}/inbox`;
	};
	// const handleSubmitClick = () => {
	// 	const author = JSON.parse(localStorage.getItem("user"));
	// 	const len = 36;
	// 	const author_id = author.id.slice(
	// 		author.id.length - len,
	// 		author.id.length
	// 	);
	// 	const post_id = postObj.id.slice(
	// 		postObj.id.length - len,
	// 		postObj.id.length
	// 	);
	// 	const params = { comment: new_comment };
	// 	const url = `posts/authors/${author_id}/posts/${post_id}/comments/`;
	// 	axios({ method: "post", url: url, data: params })
	// 		.then((res) => {
	// 			if (res.status === 200) {
	// 				getComments(url);
	// 			}
	// 		})
	// 		.catch((err) => console.log(err));
	// };


	return (
		<Panel bordered style={{ marginBottom: "5px" }}>
			<Avatar
				style={{ float: "left", marginBotton: "5px" }}
				circle
				src="https://avatars.githubusercontent.com/u/12592949"
			></Avatar>
			<h4 style={{ marginLeft: "50px" }}>{like["summary"]}</h4>
		</Panel>
	);
}

export default LIKE;

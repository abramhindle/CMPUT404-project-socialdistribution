import React, { useState, useEffect } from "react";
import { IconButton } from "rsuite";
import ThumbsUpIcon from "@rsuite/icons/legacy/ThumbsUp";
import axios from "axios";

// Component Imports

function LIKE({ postObj }) {
	// const [like, set_like] = useState(likeobj);
	const [new_like, set_new_like] = useState("");
	const postObjUrl = postObj.url;

	//Confirm the name of the button
	const handleSubmitClick = () => {
		const author = JSON.parse(localStorage.getItem("user"));
		const len = 36;
		const author_name = author.displayName;
		const author_id = author.id.slice(
			author.id.length - len,
			author.id.length
		);
		const post_id = postObj.id.slice(
			postObj.id.length - len,
			postObj.id.length
		);
		const message = author_name + " Liked your post.";
		const params = {
			author: author_id,
			object: postObjUrl,
			summary: message,
		};
		const url = `posts/authors/${author_id}/inbox`;

		//Confirm what to add into the params and send inbox
		axios({ method: "post", url: url, data: params })
			.then((res) => {
				console.log(res.data);
			})
			.catch((err) => console.log(err));
	};

	return (
		<IconButton
			style={{ float: "right", marginRight: "10px" }}
			appearance="subtle"
			icon={<ThumbsUpIcon />}
			onClick={handleSubmitClick}
		/>
	);
}

export default LIKE;

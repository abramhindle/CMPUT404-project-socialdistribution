import React, { useState, useEffect } from "react";
import { IconButton, useToaster, Message } from "rsuite";
import ThumbsUpIcon from "@rsuite/icons/legacy/ThumbsUp";
import axios from "axios";
import { getAuthorId } from "../utils/auth";

// Component Imports
function LIKE({ postObj }) {
	// const [like, set_like] = useState(likeobj);
	const [new_like, set_new_like] = useState("");
	const toaster = useToaster();
	const postObjUrl = postObj.url;

	//Confirm the name of the button
	const handleSubmitClick = () => {
		const FAID = postObj.author["id"];
		console.log(FAID);
		const author_id = getAuthorId(FAID);
		const params = {
			type: "Like",
			author_id: author_id,
			object: postObjUrl,
		};
		const url = `authors/${author_id}/inbox`;

		//Confirm what to add into the params and send inbox
		axios({ method: "post", url: url, data: params })
			.then((res) => {
				console.log(res.data);
				toaster.push(
					<Message type="success">Successful Like</Message>,
					{
						placement: "topEnd",
						duration: 5000,
					}
				);
			})
			.catch((err) => {
				toaster.push(<Message type="error">{err}</Message>, {
					placement: "topEnd",
					duration: 5000,
				});
			});
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

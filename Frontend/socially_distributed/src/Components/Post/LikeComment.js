import React, { useState, useEffect } from "react";
import { IconButton, useToaster, Message } from "rsuite";
import ThumbsUpIcon from "@rsuite/icons/legacy/ThumbsUp";
import axios from "axios";
import { getAuthorId } from "../utils/auth";

// Component Imports
function COMMENTLIKE({ obj }) {
	// const [like, set_like] = useState(likeobj);
	const [new_like, set_new_like] = useState("");
	const toaster = useToaster();

	//Confirm the name of the button
	async function handleSubmitClick() {
		const curr_author_id = getAuthorId(null);
		var FAID = "";
		const url2 = obj;

		await axios({ method: "get", url: url2 }).then((res) => {
			console.log(res.data.author);
			FAID = getAuthorId(res.data.author.id);
		});

		const params = {
			type: "Like",
			author_id: curr_author_id,
			object: url2,
		};
		const url = `authors/${FAID}/inbox`;

		//Confirm what to add into the params and send inbox
		axios({ method: "post", url: url, data: params })
			.then((res) => {
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
	}

	return (
		<IconButton
			style={{ float: "right", marginRight: "10px" }}
			appearance="subtle"
			icon={<ThumbsUpIcon />}
			onClick={handleSubmitClick}
		/>
	);
}

export default COMMENTLIKE;

import React, { useState } from "react";
import { IconButton } from "rsuite";
import ThumbsUpIcon from "@rsuite/icons/legacy/ThumbsUp";
import "./Post.css";
// Component Imports

function LIKE() {
	return (
		<IconButton
			style={{ float: "right", marginRight: "10px" }}
			appearance="subtle"
			icon={<ThumbsUpIcon />}
		/>
	);
}

export default LIKE;

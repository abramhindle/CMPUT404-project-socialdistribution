import React from "react";
import { Avatar } from "rsuite";
import { getProfileImageUrl } from "../utils/auth";

function PROFILEIMAGE({ size }) {
	return (
		<Avatar
			style={{ float: "left" }}
			circle
			src={getProfileImageUrl()}
			size={size}
		></Avatar>
	);
}

export default PROFILEIMAGE;

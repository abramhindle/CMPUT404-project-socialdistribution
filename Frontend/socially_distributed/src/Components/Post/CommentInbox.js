import React, { useEffect, useState } from "react";
import { Avatar, Panel } from "rsuite";
import PROFILEIMAGE from "../Profile/ProfileImage";
// Component Imports

function COMMENTINBOX({ obj }) {
	const [comment, set_comment] = useState(obj);

	return (
		<Panel bordered style={{ marginBottom: "5px" }}>
			<PROFILEIMAGE size="md" />
			<div
				style={{
					marginLeft: "50px",
					fontFamily: "Times New Roman",
					fontWeight: "bold",
					fontSize: "20px",
				}}
			>
				{comment.author["displayName"] +
					" commented " +
					comment.comment +
					" on your post"}
			</div>
		</Panel>
	);
}

export default COMMENTINBOX;

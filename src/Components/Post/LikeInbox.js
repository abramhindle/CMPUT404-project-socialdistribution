import React, { useState, useEffect } from "react";
import { Avatar, Panel } from "rsuite";
import PROFILEIMAGE from "../Profile/ProfileImage";
// Component Imports

function LIKEINBOX({ likeobj }) {
	const [like, set_like] = useState(likeobj);

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
				{like["summary"]}
			</div>
		</Panel>
	);
}

export default LIKEINBOX;

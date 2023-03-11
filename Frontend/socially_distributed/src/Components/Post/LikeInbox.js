import React, { useState, useEffect } from "react";
import { Avatar, Panel } from "rsuite";
// Component Imports

function LIKEINBOX({ likeobj }) {
	const [like, set_like] = useState(likeobj);

	return (
		<Panel bordered style={{ marginBottom: "5px" }}>
			<Avatar
				style={{ float: "left", marginBotton: "5px" }}
				circle
				src="https://avatars.githubusercontent.com/u/12592949"
			></Avatar>
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

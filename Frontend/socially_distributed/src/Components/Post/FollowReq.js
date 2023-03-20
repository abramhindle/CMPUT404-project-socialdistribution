import React, { useState } from "react";
import { Button, Avatar, Panel } from "rsuite";
import axios from "axios";
import PROFILEIMAGE from "../Profile/ProfileImage";

function FOLLOWREQ({ obj }) {
	const [follow, setFollow] = useState(obj);

	return (
		<Panel
			bordered
			style={{
				marginBottom: "5px",
			}}
		>
			<div>
				<Avatar
					style={{ float: "left", marginBotton: "5px" }}
					circle
					src={follow["actor"]["profileImage"]} //{follow[actor][profileImage]} replace this with the actors profile image url
				/>
				<div
					style={{
						marginLeft: "50px",
						fontFamily: "Times New Roman",
						fontWeight: "bold",
						fontSize: "20px",
					}}
				>
					{follow["summary"]}
				</div>
			</div>

			<div style={{ marginTop: "10px" }}>
				<Button block appearance="primary">
					Accept
				</Button>
				<Button block>Deny</Button>
			</div>
		</Panel>
	);
}

export default FOLLOWREQ;

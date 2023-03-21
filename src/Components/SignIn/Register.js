import React, { useState } from "react";
import { Button, Input, Panel, InputGroup, Message, useToaster } from "rsuite";
import EyeIcon from "@rsuite/icons/legacy/Eye";
import EyeSlashIcon from "@rsuite/icons/legacy/EyeSlash";
import axios from "axios";

function REGISTER() {
	const [username, set_username] = useState("");
	const [password, set_password] = useState("");
	const [fullname, set_fullname] = useState("");
	const [email, set_email] = useState("");
	const [visible, setVisible] = React.useState(false);
	let toaster = useToaster();

	const handleChange = () => {
		setVisible(!visible);
	};

	const notifySuccessPost = (message) => {
		toaster.push(<Message type="success">{message}</Message>, {
			placement: "topEnd",
			duration: 5000,
		});
	};

	const notifyFailedPost = (error) => {
		toaster.push(<Message type="error">{error}</Message>, {
			placement: "topEnd",
			duration: 5000,
		});
	};

	const handleSubmitClick = () => {
		var params = {
			username: username,
			password: password,
			fullname: fullname,
			email: email,
		};
		axios({ method: "post", url: "register", data: params })
			.then((res) => {
				notifySuccessPost("Registration Successful");
			})
			.catch((err) => notifyFailedPost(err));
	};

	return (
		<div>
			<Panel
				header="Register"
				shaded
				style={{ margin: "auto", textAlign: "center" }}
			>
				<Input
					onChange={(e) => set_email(e)}
					placeholder="Email"
					style={{ width: "70%", margin: "auto" }}
				/>
				<Input
					onChange={(e) => set_fullname(e)}
					placeholder="Full Name"
					style={{ width: "70%", margin: "auto", marginTop: "10px" }}
				/>
				<Input
					onChange={(e) => set_username(e)}
					placeholder="Display Name"
					style={{ width: "70%", margin: "auto", marginTop: "10px" }}
				/>
				<InputGroup
					inside
					style={{ width: "70%", margin: "auto", marginTop: "10px" }}
				>
					<Input
						onChange={(e) => set_password(e)}
						placeholder="password"
						type={visible ? "text" : "password"}
					/>
					<InputGroup.Button onClick={handleChange}>
						{visible ? <EyeIcon /> : <EyeSlashIcon />}
					</InputGroup.Button>
				</InputGroup>
				<Button
					apperance="Primary"
					block
					style={{ width: "70%", margin: "auto", marginTop: "10px" }}
					onClick={handleSubmitClick}
				>
					Register
				</Button>
			</Panel>
		</div>
	);
}

export default REGISTER;

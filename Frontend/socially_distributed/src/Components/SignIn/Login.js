import React, { useEffect, useState } from "react";
import { Button, Input, Panel, InputGroup } from "rsuite";
import EyeIcon from "@rsuite/icons/legacy/Eye";
import EyeSlashIcon from "@rsuite/icons/legacy/EyeSlash";
import axios from "axios";
import {
	getCsrfToken,
	setCurrentUser,
	setLoggedIn,
	unsetCurrentUser,
} from "../utils/auth";
import { useNavigate } from "react-router-dom";

function LOGIN() {
	const [username, set_username] = useState("");
	const [password, set_password] = useState("");
	const [visible, setVisible] = React.useState(false);

	let navigate = useNavigate();

	useEffect(() => {
		if (localStorage.getItem("loggedIn")) {
			navigate("/");
		} else {
			unsetCurrentUser();
			getCsrfToken();
		}
	}, []);

	const handleChange = () => {
		setVisible(!visible);
	};

	async function handleLoginClick() {
		var params = {
			username: username,
			password: password,
		};

		await axios({ method: "post", url: "login", data: params })
			.then(async (res) => {
				await setCurrentUser(res.data).then(navigate("/"));
				getCsrfToken();
				setLoggedIn(true);
			})
			.catch((err) => console.log(err));
	}

	return (
		<div>
			<Panel header="Login" shaded style={{ textAlign: "center" }}>
				<Input
					onChange={(e) => set_username(e)}
					value={username}
					placeholder="username"
					style={{ width: "70%", margin: "auto" }}
				/>
				<InputGroup
					inside
					style={{ width: "70%", margin: "auto", marginTop: "10px" }}
				>
					<Input
						onChange={(e) => set_password(e)}
						value={password}
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
					style={{ width: "70%", margin: "auto", marginTop: 10 }}
					onClick={handleLoginClick}
				>
					Login
				</Button>
			</Panel>
		</div>
	);
}

export default LOGIN;

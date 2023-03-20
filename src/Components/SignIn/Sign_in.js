import React, { useState } from "react";
import { Button, ButtonToolbar, ButtonGroup } from "rsuite";
// Component Imports
import LOGIN from "./Login";
import REGISTER from "./Register";

function SIGN_IN() {
	const [Login, setLogin] = React.useState(true);
	const [appearance, setAppearance] = React.useState({
		login: "primary",
		register: "ghost",
	});

	const handleLoginBtnClick = () => {
		setLogin(true);
		setAppearance({ login: "primary", register: "ghost" });
	};

	const handleRegisterBtnClick = () => {
		setLogin(false);
		setAppearance({ login: "ghost", register: "primary" });
	};

	return (
		<div style={{ width: "40%", margin: "auto" }}>
			<ButtonToolbar style={{ width: "100%" }}>
				<ButtonGroup justified>
					<Button
						style={{ textAlign: "center" }}
						appearance={appearance["login"]}
						onClick={handleLoginBtnClick}
					>
						Login
					</Button>
					<Button
						style={{ textAlign: "center" }}
						appearance={appearance["register"]}
						onClick={handleRegisterBtnClick}
					>
						Register
					</Button>
				</ButtonGroup>
			</ButtonToolbar>
			{Login ? <LOGIN /> : <REGISTER />}
		</div>
	);
}

export default SIGN_IN;

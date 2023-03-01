import { BrowserRouter, Routes, Route } from "react-router-dom";
import SIGN_IN from "./Components/SignIn/Sign_in";
import INBOX from "./Components/Post/Inbox";
import PROFILE from "./Components/Profile/Profile";

function App() {
	return (
		<div className="App">
			<BrowserRouter>
				<Routes>
					<Route path="/login" element={<SIGN_IN />} />
					<Route path="/inbox" element={<INBOX />} />
					<Route path="/profile" element={<PROFILE />} />
				</Routes>
			</BrowserRouter>
		</div>
	);
}

export default App;

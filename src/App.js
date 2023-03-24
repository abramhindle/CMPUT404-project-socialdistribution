import { BrowserRouter, Routes, Route } from "react-router-dom";
import SIGN_IN from "./Components/SignIn/Sign_in";
import INBOX from "./Components/Post/inbox";
import PROFILE from "./Components/Profile/Profile";
import CREATEPOST from "./Components/Post/CreatePost";

function App() {
	return (
		<div className="App">
			<BrowserRouter>
				<Routes>
					<Route path="/login" exact element={<SIGN_IN />} />
					<Route path="/" exact element={<INBOX />} />
					<Route path="/profile" exact element={<PROFILE />} />
				</Routes>
			</BrowserRouter>
		</div>
	);
}

export default App;

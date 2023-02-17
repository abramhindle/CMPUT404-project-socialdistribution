import {BrowserRouter, Routes, Route} from "react-router-dom"
import SIGN_IN from "./Components/sign_in";


function App() {
	return (
		<div className="App">
			<BrowserRouter>
				<Routes>
					<Route path="/login" element={ <SIGN_IN/> } />
				</Routes>
			</BrowserRouter>
		</div>
	);
}

export default App;

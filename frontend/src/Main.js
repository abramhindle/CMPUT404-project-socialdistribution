import { useContext } from "react";
import AuthContext from "./Auth";

function Main() {
  const { logoutUser } = useContext(AuthContext);

  return (
    <div>
      Main!
      <button onClick={logoutUser}> Sign Out </button>
    </div>
  );
}

export default Main;

import { useSelector } from "react-redux";
import Inbox from "./Inbox/inbox";

function Stream(filter) {
  const user = useSelector((state) => state.user);

  return (
    <div>
      Main Stream! Welcome {user.displayName}
      <Inbox filter={filter}/>
    </div>
  );
}

export default Stream;

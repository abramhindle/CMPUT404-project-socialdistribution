import { useSelector } from "react-redux";
import Inbox from "./Inbox/inbox";

function Stream(filter) {
  return (
    <div>
      <Inbox filter={filter}/>
    </div>
  );
}

export default Stream;

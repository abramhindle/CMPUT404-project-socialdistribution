import Post from "../components/Post";
import Like from "../components/Like";
import Follow from "../components/Follow";
import { UserContext } from "../UserContext";
import { useContext } from "react";
import authorService from "../services/author";
import jsCookies from "js-cookies";

const Home = ({ inbox, setInbox }) => {
  const { user } = useContext(UserContext);

  const clearInbox = async () => {
    try {
      const response = await authorService.clearInbox(jsCookies.getItem("csrftoken"), user.author.authorID);
      setInbox([])
    } catch {
      console.log("OH NO!!!!")
    }
  };

  return (
    <div>
      <div>
      { inbox && inbox.map((item) => {
        console.log(item);
        if (item.type === "Post") {
          return <Post key={item.id} post={item} />
        } else if (item.type === "Follow") {
          return <Follow key={`${item.actor.id};${item.object.id}`} follow={item} />
        } else if (item.type === "Like") {
          return <Like key={`${item.object};${item.author.id}`} like={item} />
        } else {
          return <p>messed</p>
        }
      })}
      </div>
      <button onClick={clearInbox}>clear the ol box</button>
    </div>
  );
}

export default Home;
import "./post-list.css";
import DisplayItem from "../Posts/display";

function PostList({ user_list }) {
  //gets a json object, and returns a list item for it

  return (
    <div className="posts">
      <ul className="postsList">
        {console.log(user_list)}
        {user_list.items.map((list_item) => (
          <li className="list-item" key={list_item.id}>
            <DisplayItem data={list_item}/>
          </li>
        ))}
        end of items
      </ul>
    </div>
  );
}

export default PostList;

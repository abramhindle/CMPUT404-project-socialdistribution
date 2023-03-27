import Sidebar from "../../components/Sidebar/sidebar";
import '../pages.css';
import "./inbox.css";
import { get_inbox_posts } from "../../api/post_display_api";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import PostList from "../../components/ListItems/post-list";
import { useSelector } from "react-redux";

function Inbox(filter) {
  //Get user info
  let id = useSelector((state) => state.user).id;
  const author_id = `${id}/inbox`;
  const [author, setAuthor] = useState({});
  const [post_list, setList] = useState({ items: [] });

  let page = 1; //default page 1
  const navigate = useNavigate();
  const location = useLocation();

  const get_search_params = () => {
    const queryParams = new URLSearchParams(location.search);
    const query_page = queryParams.get("page");

    if (query_page) page = parseInt(query_page);
  };

  get_search_params();

  useEffect(() => {
    //only runs once
    get_inbox_posts(author_id, page, setList);
  }, [author_id]);

  const populateList = () => {
    if (!post_list || !post_list.items || post_list.items.length == 0) {
      return (
        <div className="emptyList">
          <h3>Nothing to see here yet!</h3>
        </div>
      );
    } else {
      return <PostList user_list={post_list} />;
    }
  };

  const insert_query = () => {
    <button href={insert_query}>Next Page</button>;
  };

  return (
    post_list && (
      <div className="Page">
        <Sidebar />
        <div className="Inbox sidebar-offset">
          <div className="pageContent">{populateList()}</div>
          {/*{page_buttons()}*/}
        </div>
      </div>
    )
  );
}

export default Inbox;

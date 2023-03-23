import Sidebar from "../../components/Sidebar/sidebar";
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

  const page_buttons = () => {
    if (!post_list) {
      return;
    }

    if (post_list.items.length < 5 && page == 1) {
      return;
    } else if (page == 1) {
      return <button onClick={forward_page}>Next Page</button>; //only 1 button
    } else if (post_list.items.length < 5) {
      return <button onClick={back_page}>Prev Page</button>;
    } else {
      return (
        <div>
          <button onClick={back_page}>Prev Page</button>
          <button onClick={forward_page}>Next Page</button>
        </div>
      ); //only 1 button
    }
  };

  const forward_page = () => {
    page = page + 1;
    navigate(`/inbox/${filter}?page=${page}`);
    navigate(0); //WHY?
  };

  const back_page = () => {
    page = page - 1;
    navigate(`/inbox/${filter}?page=${page}`);
    navigate(0);
  };

  return (
    post_list && (
      <div className="Page">
        <div>
          <Sidebar />
        </div>
        <div className="Inbox">
          <div className="profileContent">{populateList()};</div>
          {page_buttons()}
        </div>
      </div>
    )
  );
}

export default Inbox;

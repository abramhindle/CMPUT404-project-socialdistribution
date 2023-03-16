import Sidebar from "../../components/Sidebar/sidebar";
import '../pages.css'
import "./profile.css";
import { get_author } from "../../api/author_api";
import { useEffect, useState } from "react";
import {
  Navigate,
  Route,
  useLocation,
  useNavigate,
  useParams,
  useSearchParams,
} from "react-router-dom";
import { get_author_posts } from "../../api/post_display_api";
import { get_followers_for_author } from "../../api/follower_api";
import PostList from "../../components/ListItems/post-list";
import AuthorList from "../../components/ListItems/author-list";

function Profile() {
  const { author_id } = useParams();
  const [author, setAuthor] = useState({});
  const [user_list, setList] = useState({ items: [] });

  let tab = "posts"; // default posts
  let page = 1; //default page 1

  const location = useLocation();

  const get_search_params = () => {
    const queryParams = new URLSearchParams(location.search);
    const query_page = queryParams.get("page");
    const query_tab = queryParams.get("tab");

    if (query_page) page = parseInt(query_page);
    if (query_tab) tab = query_tab;
  };

  get_search_params();

  useEffect(() => {
    //only runs once
    get_author(`http://localhost/authors/${author_id}/`, setAuthor);

    if (tab === "followers") {
      get_followers_for_author(
        `http://localhost/authors/${author_id}`,
        setList
      );
    } else if (tab === "posts") {
      get_author_posts(`http://localhost/authors/${author_id}`, page, setList);
    }
  }, []);

  const populateList = () => {
    if (user_list.items.length === 0) {
      return (
        <div className="emptyList">
          <h3>Nothing to see here yet!</h3>
        </div>
      );
    }

    switch (tab) {
      case "posts":
        return <PostList user_list={user_list} />;
      case "followers":
        return <AuthorList user_list={user_list} />;
    }
  };

  const navigate = useNavigate();

  const insert_query = () => {
    <button href={insert_query}>Next Page</button>;
  };

  const page_buttons = () => {
    if (user_list.items.length < 5 && page === 1) {
      return;
    } else if (page === 1) {
      return <button onClick={forward_page}>Next Page</button>; //only 1 button
    } else if (user_list.items.length < 5) {
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
    navigate(`/user/${author_id}/?tab=${tab}&page=${page}`);
    navigate(0); //WHY?
  };

  const back_page = () => {
    page = page - 1;
    navigate(`/user/${author_id}/?tab=${tab}&page=${page}`);
    navigate(0);
  };

  return (
    <div className="Page">
      <div>
        <Sidebar />
      </div>
      <div className="myprofile page-content">
        <div className="profileHead">
          <h1>{author.displayName}</h1>
          GitHub: {author.github}
        </div>
        <div>
          <nav className="navbar">
            <ul>
              <a href="?tab=posts">Posts</a>
              <a href="?tab=followers">Followers</a>
            </ul>
          </nav>
        </div>
        <div className="profileContent">{populateList()};</div>
        {page_buttons()}
      </div>
    </div>
  );
}

export default Profile;

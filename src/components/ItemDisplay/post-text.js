//Styles
import "./posts.css";
//Functions
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { post_comment } from "../../api/comment_api";
import { post_like } from "../../api/like_api";
import { get_liked } from "../../api/like_api";
//Components
import ReactMarkdown from "react-markdown";
import LikeHeart from "../Buttons/like_button";
import CommentArrow from "../Buttons/comment_button";
import ShareIcon from "../Buttons/share_button";

export default function PlainPost(data) {
  // Visibility
  let markdown = data["post"]["contentType"] === "text/markdown" ? true : false;
  let shareable =
    data["post"]["visibility"] === "PUBLIC" ||
    data["post"]["visibility"] === "FRIENDS"
      ? true
      : false;

  // Urls
  const user = useSelector((state) => state.user);
  const port = window.location.port ? `:${window.location.port}` : "";
  const authorUrl = `//${window.location.hostname}${port}/user/${(
    data.post.author.id ?? ""
  )
    .split("/")
    .pop()}`; // allows linking to the author who wrote the post

  const postUrl = `//${window.location.hostname}${port}/user/${(
    data.post.author.id ?? ""
  )
    .split("/")
    .pop()}/post/${(data.post.id ?? "").split("/").pop()}`;

  // Like Handling
  const [liked, setLiked] = useState(data.liked);

  const like_success = (bool) => {
    setLiked(bool); // Changes heart colour
    get_liked(user.id, data.updateList); // Triggers rerender
  };

  const handleLike = () => {
    if (!liked) {
      post_like(
        data.post.author.id,
        user,
        data.post.id,
        "context",
        like_success
      );
    } else {
      //TODO delete like object
      console.log("Liked already");
    }
  };

  //Comment Handling
  const [comment, setComment] = useState("");
  const [commentType, setCommentType] = useState("text/plain");

  const submitComment = () => {
    if (comment) {
      post_comment(
        data.post.author.id,
        data.post.id,
        commentType,
        comment,
        user.id
      );
      setComment("");
    } else {
      alert("enter the comment");
    }
  };

  return (
    <div className="vflex">
      <div className="list-item">
        {/* Profile image w/link to post author's profile */}
        <div className="profile from">
          <a href={authorUrl}>
            {<img alt="author" src={data.post.author.profileImage}></img>}
          </a>
        </div>

        {/* Will need to handle other post types here, plain for now */}
        <div className="post">
          <h5>
            <Link to={postUrl}>{data["post"]["title"]}</Link>
          </h5>
          {markdown && (
            <ReactMarkdown
              className="content"
              children={data["post"]["content"]}
            />
          )}
          {!markdown && (
            <div className="content">{data["post"]["content"]}</div>
          )}
        </div>
        <div className="interaction-options">
          <LikeHeart handleLike={handleLike} liked={liked} />
          <CommentArrow
            setCommentType={setCommentType}
            setComment={setComment}
            submit={submitComment}
          />
          {/* Share Button */}
          {shareable && <ShareIcon />}
        </div>
      </div>
      <div className="timestamp">{data["post"]["published"]}</div>
    </div>
  );
}

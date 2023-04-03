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

import profile from "../../images/profile.png";

export default function Post(data) {
  // Visibility
  let markdown = data["post"]["contentType"] === "text/markdown" ? true : false;
  let image =
    data["post"]["contentType"].split("/")[0] === "image" ? true : false;
  console.log(data);
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
  const [commentFieldVisibilty, setCommentFieldVisibilty] = useState(false);

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
      setCommentFieldVisibilty(false);
    } else {
      alert("enter the comment");
    }
  };

  return (
    <div className="vflex center">
      <div className="list-item">
        {/* Profile image w/link to post author's profile */}
        <div className="profile from">
          <a href={authorUrl}>
            {<img alt="author" src={data.post.author.profileImage === "" ? profile : data.post.author.profileImage}></img>}
          </a>
        </div>

        {/* Will need to handle other post types here, plain for now */}
        <div className="post">
          <h5>
            <Link to={postUrl}>{data["post"]["title"]}</Link>
          </h5>
          {image && (
            <img
              className="posted-image"
              alt={data["post"]["description"]}
              src={"data:"+data["post"]["contentType"]+";base64,"+data["post"]["content"]}
            />
          )}
          {markdown && (
            <ReactMarkdown
              className="content"
              children={data["post"]["content"]}
            />
          )}
          {!markdown && !image && (
            <div className="content">{data["post"]["content"]}</div>
          )}
        </div>
        <div className="interaction-options">
          <LikeHeart handleLike={handleLike} liked={liked} />
          <CommentArrow
            setCommentFieldVisibilty={setCommentFieldVisibilty}
           />
          {/* Share Button */}
          {shareable && <ShareIcon />}
        </div>
      </div>
      {commentFieldVisibilty && (
            <div className="comment-input-form">
            <input
                type="radio"
                id="text"
                name="contentType"
                value="text/plain"
                defaultChecked
                onChange={(e) => setCommentType(e.target.value)}
            />
            <label htmlFor="text">Text</label>
            <input
                type="radio"
                id="markdown"
                name="contentType"
                value="text/markdown"
                onChange={(e) => setCommentType(e.target.value)}
            />
            <label htmlFor="markdown">Markdown</label>
            <input
                onChange={(e) => setComment(e.target.value)}
                placeholder="Enter the comment here"
                type="text"
            />
            <button onClick={submitComment}>Submit</button>
            </div>
            )}
      <div className="timestamp">{data["post"]["published"]}</div>
    </div>
  );
}

import "./posts.css";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { useSelector } from "react-redux";
import ReactMarkdown from "react-markdown";
import { post_comment } from "../../api/comment_api";
import { post_like } from "../../api/like_api";
import { get_liked } from "../../api/like_api";

export default function PlainPost(data) {
  const user = useSelector((state) => state.user);
  //Check if markdown
  let markdown = data["post"]["contentType"] === "text/markdown" ? true : false;
  //Decide if shareable
  let shareable =
    data["post"]["visibility"] === "PUBLIC" ||
    data["post"]["visibility"] === "FRIENDS"
      ? true
      : false;

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

  const [changes, setChanges] = useState(0);
  var liked = data.liked;

  const like_success = (bool) => {
    /* Show Success Snackbar? */
    liked = bool;
    setChanges(changes+1);
  };

  const handleLike = () => {
    if (!liked){
      post_like(data.post.author.id, user, data.post.id, "context", like_success);
    }
    else {
      //TODO delete like object
      console.log("Liked already")
    }
  }

  useEffect(() => {
    console.log("Use effect triggered");
    get_liked(data.post.author.id, data.updateList);
  }, [changes]);

  const [commentFieldVisibilty, setCommentFieldVisibilty] = useState(false);
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
      setCommentFieldVisibilty(false);
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
        <h5><Link to={postUrl}>{data["post"]["title"]}</Link></h5>
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
          {/* Like Button */}
          <button className="interact"
              onClick={handleLike}
            >
              <svg version="1.1" id="heart-15" xmlns="http://www.w3.org/2000/svg" width="2.5em" height="2.5em" viewBox="0 0 15 15">
                <path className="heart" fill={data.liked ? "var(--scarlet)" : "var(--driftwood)"}
                  d="M13.91,6.75c-1.17,2.25-4.3,5.31-6.07,6.94c-0.1903,0.1718-0.4797,0.1718-0.67,0C5.39,12.06,2.26,9,1.09,6.75&#xA;&#x9;C-1.48,1.8,5-1.5,7.5,3.45C10-1.5,16.48,1.8,13.91,6.75z"/>
              </svg>
          </button>
          
          {/* Comment Button */}
          <button
            onClick={() =>
              setCommentFieldVisibilty(commentFieldVisibilty ? false : true)
            }
          >
            comment
          </button>
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
            {/* Share Button */}
          {shareable && (
          <div className="share">
            {/* Only show if shareable */}
            <button>share</button>
          </div> )}
        </div>
      </div>
      <div className="timestamp">{data["post"]["published"]}</div>
    </div>
  );
}

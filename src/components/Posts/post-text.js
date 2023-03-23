import "./posts.css";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { useSelector } from "react-redux";
import ReactMarkdown from "react-markdown";
import { post_comment } from "../../api/comment_api";
import { post_like } from "../../api/like_api";

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

  const like_success = () => {
    /* Show Success Snackbar? */
  };

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
    <div className="post">
      <div className="message">
        <div className="from profile">
          <h6>
            <a href={authorUrl}>{data.post.author.displayName}</a>
          </h6>
          {<img alt="author" src={data.post.author.profileImage}></img>}
        </div>
        <div className="postBody">
          {/* Will need to handle other post types here, plain for now */}
          <div className="content-container">
            <h5>
              <Link to={postUrl}>{data["post"]["title"]}</Link>
            </h5>
            {markdown && (
              <ReactMarkdown
                className="content line"
                children={data["post"]["content"]}
              >
                {/* Mardown doesn't like leading whitespace */}
              </ReactMarkdown>
            )}
            {!markdown && (
              <div className="content line">{data["post"]["content"]}</div>
            )}
          </div>
          <div className="interaction-options">
            <button
              disabled={data.liked}
              onClick={() =>
                post_like(
                  data.post.author.id,
                  user,
                  data.post.id,
                  "context",
                  like_success
                )
              }
            >
              {data.liked ? "liked" : "like"}
            </button>

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

            {shareable && (
              <div className="share">
                {/* Only show if shareable */}
                <button>share</button>
              </div>
            )}
          </div>
        </div>
      </div>
      <div className="timestamp">{data["post"]["published"]}</div>
    </div>
  );
}

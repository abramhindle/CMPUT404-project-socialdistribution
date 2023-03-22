import "./posts.css";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import ReactMarkdown from "react-markdown";
import { post_comment } from "../../api/comment_api";
import { post_like } from "../../api/like_api";

export default function Comment(data) {
  let id = useSelector((state) => state.user).id;
  console.log(typeof data["data"]["comment"]);
  const user = useSelector((state) => state.user);
  //Check if markdown
  let markdown = data["data"]["contentType"] === "text/markdown" ? true : false;

  const port = window.location.port ? `:${window.location.port}` : "";
  const commentUrl = `${data.data.id}`;
  const postUrl = commentUrl.split("comment")[0];
  const authorUrl = `//${window.location.hostname}${port}/user/${(
    data.data.author.id ?? ""
  )
    .split("/")
    .pop()}`; // allows linking to the author who wrote the comment



  const like_success = () => {
    /* Show Success Snackbar? */
  };

  // TODO: CAN WE COMMENT ON COMMENTS?
//   const [commentFieldVisibilty, setCommentFieldVisibilty] = useState(false);
//   const [comment, setComment] = useState("");
//   const [commentType, setCommentType] = useState("text/plain");
//   const submitComment = () => {
//     if (comment) {
//       post_comment(
//         data.post.author.id,
//         data.post.id,
//         commentType,
//         comment,
//         user.id
//       );
//       setComment("");
//       setCommentFieldVisibilty(false);
//     } else {
//       alert("enter the comment");
//     }
//   };

  return (
    <div className="comment">
      <div className="message">
        <div className="profile from">
          <h6>
            <a href={authorUrl}>{data.data.author.displayName}</a>
          </h6>
          {<img alt="author" src={data.data.author.profileImage}></img>}
          {/**Add comment indicator */}
        </div>
        <div className="postBody">
          <div className="content-container">
            <h5>Commented on your <a href={postUrl}>post</a></h5>
            {markdown && (
              <ReactMarkdown
                className="content line"
                children={data["data"]["comment"]}
              >
                {/* Mardown doesn't like leading whitespace */}
              </ReactMarkdown>
            )}
            {!markdown && (
              <div className="content line">{data["data"]["comment"]}</div>
            )}
          </div>
          <div className="interaction-options">
            <button
              disabled={data.liked}
              onClick={() =>
                post_like(
                  data.data.author.id,
                  user,
                  data.data.id,
                  "context",
                  like_success
                )
              }
            >
              {data.liked ? "liked" : "like"}
            </button>
{/*
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
            */}

          </div>
        </div>
      </div>
      <div className="timestamp">{data["data"]["published"]}</div>
    </div>
  );
}
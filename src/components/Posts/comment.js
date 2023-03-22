import "./posts.css";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import ReactMarkdown from "react-markdown";
import { post_comment } from "../../api/comment_api";
import { comment_like } from "../../api/like_api";

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

  const handleLike = () => {
    if (!data.liked){
      comment_like(data.data.author.id, user, data.data.id, "context", like_success);
      document.getElementsByClassName("heart")
    }
    else {
      //delete like object
    }
  }

  return (
    <div className="vflex">
      <h5><a href={authorUrl}>{data.data.author.displayName}</a> commented on your <a href={postUrl}>post</a></h5>
      
      <div className="list-item">
        {/* Profile image w/link to post author's profile */}
        <div className="profile from">
          <a href={authorUrl}>
          {<img alt="author" src={data.data.author.profileImage}></img>}
          </a>
        </div>

        {/* Title, message */}

          <div className="comment">
            {markdown && (
              <ReactMarkdown
                className="content"
                children={data["data"]["comment"]}
              >
                {/* Mardown doesn't like leading whitespace */}
              </ReactMarkdown>
            )}
            {!markdown && (
              <div className="content">{data["data"]["comment"]}</div>
            )}
          </div>
                  {/* Interaction Options (like, share) */}
        <div>
            <button className="interact"
              onClick={handleLike}
            >
              <svg version="1.1" id="heart-15" xmlns="http://www.w3.org/2000/svg" width="2.5em" height="2.5em" viewBox="0 0 15 15">
                <path className="heart" fill={data.data.liked ? "red" : "var(--driftwood)"}
                  d="M13.91,6.75c-1.17,2.25-4.3,5.31-6.07,6.94c-0.1903,0.1718-0.4797,0.1718-0.67,0C5.39,12.06,2.26,9,1.09,6.75&#xA;&#x9;C-1.48,1.8,5-1.5,7.5,3.45C10-1.5,16.48,1.8,13.91,6.75z"/>
              </svg>
            </button>
        </div>
        </div>
        <div className="timestamp">{data["data"]["published"]}</div>
      </div>
  );
}
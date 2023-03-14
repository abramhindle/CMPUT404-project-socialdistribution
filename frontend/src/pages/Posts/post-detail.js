import { useParams, useLocation } from "react-router-dom";
import { get_post } from "../../api/post_display_api";
import { Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import { useEffect, useState } from "react";
import Sidebar from "../../components/Sidebar/sidebar";
import "./post-detail.css";
import { get_post_comments } from "../../api/comment_api";

function PostDetail() {
  const { data } = useLocation().state;

  const [postInfo, setPostInfo] = useState(null);
  const [commentsInfo, setCommentsInfo] = useState(null);

  const successPost = (postData) => {
    setPostInfo(postData);
  };

  const successComment = (commentData) => {
    setCommentsInfo(commentData);
  };

  console.log(commentsInfo);

  useEffect(() => {
    get_post(data.author.id, data.id, successPost);
    get_post_comments(data.author.id, data.id, successComment, 1, 5);
    console.log(data.id);
  }, []);

  const port = window.location.port ? `:${window.location.port}` : "";
  const authorUrl = `//${window.location.hostname}${port}/user/${(
    data.author.id ?? ""
  )
    .split("/")
    .pop()}`;

  const postUrl = `//${window.location.hostname}${port}/post/${(data.id ?? "")
    .split("/")
    .pop()}`;

  let markdown = data.contentType === "text/markdown" ? true : false;
  //Decide if shareable
  let shareable =
    data["visibility"] === "PUBLIC" || data["visibility"] === "FRIENDS"
      ? true
      : false;

  return (
    <div className="Page">
      <Sidebar />
      <div className="Fragment">
        <div className="message">
          <div className="from">
            <h6>
              <a href={authorUrl}>{data.author.displayName}</a>
            </h6>
            {<img alt="author" src={data.author.profileImage}></img>}
          </div>
          <div className="postBody">
            {/* Will need to handle other post types here, plain for now */}
            <div className="content-container">
              <h3>{data.title}</h3>
              {markdown && (
                <ReactMarkdown className="content line" children={data.content}>
                  {/* Mardown doesn't like leading whitespace */}
                </ReactMarkdown>
              )}
              {!markdown && <div className="content line">{data.content}</div>}
            </div>
            <div className="timestamp">{data.published}</div>
          </div>
        </div>
        <div className="comments">
          {commentsInfo &&
            commentsInfo.items.map((comment) => <div>{comment.comment}</div>)}
        </div>
      </div>
    </div>
  );
}

export default PostDetail;

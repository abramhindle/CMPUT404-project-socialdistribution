import { useParams, useLocation } from "react-router-dom";
import { useSelector } from "react-redux";
import { get_post } from "../../api/post_display_api";
import { Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import { useEffect, useState } from "react";
import Sidebar from "../../components/Sidebar/sidebar";
import "./post-detail.css";
import { get_post_comments, post_comment } from "../../api/comment_api";
import { get_post_like } from "../../api/like_api";

function PostDetail() {
  const { data } = useLocation().state;
  const user = useSelector((state) => state.user);

  const [postInfo, setPostInfo] = useState(null);
  const [likeInfo, setLikeInfo] = useState(null);
  const [commentsInfo, setCommentsInfo] = useState(null);
  const [comment, setComment] = useState("");
  const [commentType, setCommentType] = useState("text/plain");
  const [commentPage, setCommentPage] = useState(1);
  const [commentSize, setCommentSize] = useState(5);

  const nextCommentPage = () => {
    setCommentPage(commentPage + 1);
  };

  const prevCommentPage = () => {
    if (commentPage > 1) {
      setCommentPage(commentPage - 1);
    }
  };

  console.log(commentPage);

  const submitComment = () => {
    if (comment) {
      post_comment(data.author.id, data.id, commentType, comment, user.id);
      setComment("");
    } else {
      alert("enter the comment");
    }
  };

  const successPost = (postData) => {
    setPostInfo(postData);
  };

  const successLike = (likeData) => {
    setLikeInfo(likeData);
  };

  const successComment = (commentData) => {
    setCommentsInfo(commentData);
  };

  console.log(commentsInfo);

  useEffect(() => {
    get_post(data.author.id, data.id, successPost);
    get_post_like(data.author.id, data.id, successLike);
  }, [data]);

  useEffect(() => {
    get_post_comments(
      data.author.id,
      data.id,
      successComment,
      commentPage,
      commentSize
    );
  }, [commentPage, commentSize]);

  const port = window.location.port ? `:${window.location.port}` : "";
  const authorUrl = `//${window.location.hostname}${port}/user/${(
    data.author.id ?? ""
  )
    .split("/")
    .pop()}`;

  let markdown = data.contentType === "text/markdown" ? true : false;
  //Decide if shareable
  let shareable =
    data.visibility === "PUBLIC" || data.visibility === "FRIENDS"
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
            <img alt="author" src={data.author.profileImage}></img>
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
        <div className="Social">
          <button>Like</button>
          {shareable && (
            <div className="share">
              {/* Only show if shareable */}
              <button>share</button>
            </div>
          )}
        </div>
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
        <div className="comments">
          {commentsInfo &&
            commentsInfo.items.map((comment) => <div>{comment.comment}</div>)}
          <button onClick={prevCommentPage}>prev</button>
          <button onClick={nextCommentPage}>next</button>
        </div>
      </div>
    </div>
  );
}

export default PostDetail;

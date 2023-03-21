import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import { useEffect, useState } from "react";
import Sidebar from "../../components/Sidebar/sidebar";
import "./post-detail.css";
import { get_post } from "../../api/post_display_api";
import { get_post_comments, post_comment } from "../../api/comment_api";
import { get_post_like, post_like } from "../../api/like_api.js";

function PostDetail() {
  const { author_id, post_id } = useParams();
  const user = useSelector((state) => state.user);

  const [postInfo, setPostInfo] = useState(null);
  const [likeInfo, setLikeInfo] = useState(null);
  const [commentsInfo, setCommentsInfo] = useState(null);
  const [comment, setComment] = useState("");
  const [commentType, setCommentType] = useState("text/plain");
  const [commentPage, setCommentPage] = useState(1);
  const [commentSize, setCommentSize] = useState(5);
  const [nextCommentPageInfo, setNextCommentPageInfo] = useState(null);

  const nextCommentPage = () => {
    setCommentPage(commentPage + 1);
  };

  const prevCommentPage = () => {
    setCommentPage(commentPage - 1);
  };

  const submitComment = async () => {
    if (comment) {
      await post_comment(
        `http://localhost/authors/${author_id}`,
        `http://localhost/authors/${author_id}/posts/${post_id}`,
        commentType,
        comment,
        user.id
      );
      get_post_comments(
        `http://localhost/authors/${author_id}`,
        `http://localhost/authors/${author_id}/posts/${post_id}`,
        successComment,
        commentPage,
        commentSize
      );
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
    if (commentData.items.length < commentSize) {
      setNextCommentPageInfo(null);
    } else if (commentData.items.length === commentSize) {
      get_post_comments(
        `http://localhost/authors/${author_id}`,
        `http://localhost/authors/${author_id}/posts/${post_id}`,
        preCheckNextCommentPage,
        commentPage + 1,
        commentSize
      );
    }
  };

  const preCheckNextCommentPage = (commentData) => {
    if (commentData.items.length === 0) {
      setNextCommentPageInfo(null);
    } else {
      setNextCommentPageInfo(commentData);
    }
  };

  useEffect(() => {
    get_post(
      `http://localhost/authors/${author_id}`,
      `http://localhost/authors/${author_id}/posts/${post_id}`,
      successPost
    );
    get_post_like(
      `http://localhost/authors/${author_id}`,
      `http://localhost/authors/${author_id}/posts/${post_id}`,
      successLike
    );
  }, [author_id, post_id]);

  useEffect(() => {
    get_post_comments(
      `http://localhost/authors/${author_id}`,
      `http://localhost/authors/${author_id}/posts/${post_id}`,
      successComment,
      commentPage,
      commentSize
    );
  }, [commentPage, commentSize, author_id, post_id]);

  const port = window.location.port ? `:${window.location.port}` : "";
  const authorUrl = `//${window.location.hostname}${port}/user/${author_id}`;

  let markdown;
  let shareable;
  if (postInfo) {
    markdown = postInfo.contentType === "text/markdown" ? true : false;
    //Decide if shareable
    shareable =
      postInfo.visibility === "PUBLIC" || postInfo.visibility === "FRIENDS"
        ? true
        : false;
  }

  return (
    postInfo && (
      <div className="Page">
        <Sidebar />
        <div className="Fragment">
          <div className="message">
            <div className="from">
              <h6>
                <Link to={authorUrl}>{postInfo.author.displayName}</Link>
              </h6>
              <img alt="author" src={postInfo.author.profileImage}></img>
            </div>
            <div className="postBody">
              {/* Will need to handle other post types here, plain for now */}
              <div className="content-container">
                <h3 id="title">{postInfo.title}</h3>
                {markdown && (
                  <ReactMarkdown
                    className="content line"
                    children={postInfo.content}
                  >
                    {/* Mardown doesn't like leading whitespace */}
                  </ReactMarkdown>
                )}
                {!markdown && (
                  <div className="content line">{postInfo.content}</div>
                )}
              </div>
              <div className="timestamp">{postInfo.published}</div>
            </div>
          </div>
          <div className="Social">
            {likeInfo && <div>{likeInfo.items.length} Liked this post</div>}
            <div className="interaction-options">
              <button
                onClick={() =>
                  post_like(
                    `http://localhost/authors/${author_id}`,
                    user,
                    `http://localhost/authors/${author_id}/posts/${post_id}`,
                    "context"
                  )
                }
              >
                Like
              </button>
              {shareable && (
                <div className="share">
                  {/* Only show if shareable */}
                  <button>share</button>
                </div>
              )}
            </div>
          </div>

          <div className="comments">
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
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Enter the comment here"
                type="text"
              />
              <button onClick={submitComment}>Submit</button>
            </div>
            <div>
              {commentsInfo &&
                commentsInfo.items.map((comment) => (
                  /** TODO: Use Comment View once it is implemented */
                  <div key={comment.id}>{comment.comment}</div>
                ))}
              <button
                onClick={prevCommentPage}
                disabled={commentPage === 1 ? true : false}
              >
                prev
              </button>
              <button
                onClick={nextCommentPage}
                disabled={nextCommentPageInfo ? false : true}
              >
                next
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  );
}

export default PostDetail;

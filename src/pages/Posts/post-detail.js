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
import LikeHeart from "../../components/Buttons/like_button";
import ShareIcon from "../../components/Buttons/share_button";
import PostList from "../../components/ListItems/post-list";

function PostDetail() {
  const { author_id, post_id } = useParams();
  const user = useSelector((state) => state.user);
  
  const [mine, setMine] = useState(false);
  const [postInfo, setPostInfo] = useState(null);
  const [markdown, setMarkdown] = useState(false);
  const [shareable, setShareable] = useState(false);
  const [likeInfo, setLikeInfo] = useState(null);
  const [liked, setLiked] = useState(false);
  const [commentsInfo, setCommentsInfo] = useState(null);
  const [comment, setComment] = useState("");
  const [commentType, setCommentType] = useState("text/plain");
  const [commentPage, setCommentPage] = useState(1);
  const [commentSize, setCommentSize] = useState(5);
  const [nextCommentPageInfo, setNextCommentPageInfo] = useState(null);

  const successPostLike = (success) => {
    setLiked(success);
    get_post_like(
      `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}`,
      `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}/posts/${post_id}`,
      successLike
    );
  };

  const nextCommentPage = () => {
    setCommentPage(commentPage + 1);
  };

  const prevCommentPage = () => {
    setCommentPage(commentPage - 1);
  };

  const submitComment = async () => {
    if (comment) {
      await post_comment(
        `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}`,
        `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}/posts/${post_id}`,
        commentType,
        comment,
        user.id
      );
      get_post_comments(
        `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}`,
        `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}/posts/${post_id}`,
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
    if (postData.contentType === "text/markdown") {
      setMarkdown(true);
    }
    if (postData.visibility === "PUBLIC" || postData.visibility === "FRIENDS") {
      setShareable(true);
    }
    if (postData.author.id === user.id) {
      setMine(true);
    }
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
        `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}`,
        `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}/posts/${post_id}`,
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
    if (likeInfo) {
      for (var i = 0; i < likeInfo.items.length; i++) {
        if (likeInfo.items[i].author.id === user.id) {
          setLiked(true);
          break;
        }
      }
    }
  }, [likeInfo]);

  useEffect(() => {
    get_post(
      `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}`,
      `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}/posts/${post_id}`,
      successPost
    );
    get_post_like(
      `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}`,
      `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}/posts/${post_id}`,
      successLike
    );
  }, [author_id, post_id]);

  useEffect(() => {
    get_post_comments(
      `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}`,
      `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}/posts/${post_id}`,
      successComment,
      commentPage,
      commentSize
    );
  }, [commentPage, commentSize, author_id, post_id]);

  const port = window.location.port ? `:${window.location.port}` : "";
  const authorUrl = `//${window.location.hostname}${port}/user/${author_id}`;

  return (
    postInfo && (
      <div className="Page detail">
        <Sidebar />
        <div className="Fragment sidebar-offset">
          <div className="message">
            <div className="from">
              <img alt="author" src={postInfo.author.profileImage}></img>
              <h6>
                <Link to={authorUrl}>{postInfo.author.displayName}</Link>
              </h6>
              {mine && <button>EDIT</button>}
            </div>
            <div className="postBody">
              {/* Will need to handle other post types here, plain for now */}
              <div className="content-container">
                <h3 id="title">{postInfo.title}</h3>
                {markdown ? (
                  <ReactMarkdown
                    className="content line"
                    children={postInfo.content}
                  >
                    {/* Mardown doesn't like leading whitespace */}
                  </ReactMarkdown>
                ) : (
                  <div className="content line">{postInfo.content}</div>
                )}
              </div>
              <div className="timestamp">{postInfo.published}</div>
            </div>
          </div>
          <div className="Social">
            {likeInfo && <div>{likeInfo.items.length} Liked this post</div>}
            <div className="interaction-options">
              <LikeHeart
                handleLike={() =>
                  post_like(
                    `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}`,
                    user,
                    `https://social-distribution-w23-t17.herokuapp.com/authors/${author_id}/posts/${post_id}`,
                    "context",
                    successPostLike
                  )
                }
                liked={liked}
              />
              {shareable && <ShareIcon />}
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
                  id="comment-input"
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="Enter the comment here"
                  type="text"
                />
                <button
                  id="comment-submit"
                  disabled={comment ? false : true}
                  onClick={submitComment}
                >
                  Submit
                </button>
              </div>
            </div>
            <div className="comments">
              {commentsInfo && (
                <div>
                  <PostList user_list={commentsInfo} />
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
              )}
            </div>
          </div>
        </div>
      </div>
    )
  );
}

export default PostDetail;

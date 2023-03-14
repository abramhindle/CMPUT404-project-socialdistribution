import { useParams, useLocation } from "react-router-dom";
import { get_post } from "../../api/post_display_api";
import { Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";

function PostDetail() {
  const { data } = useLocation().state;

  const port = window.location.port ? `:${window.location.port}` : "";
  //   const authorUrl = `//${window.location.hostname}${port}/user/${(
  //     data.post.author.id ?? ""
  //   )
  //     .split("/")
  //     .pop()}`;
  const postUrl = `//${window.location.hostname}${port}/post/${(
    data.post.id ?? ""
  )
    .split("/")
    .pop()}`;

  let markdown = data["post"]["contentType"] === "text/markdown" ? true : false;
  //Decide if shareable
  let shareable =
    data["post"]["visibility"] === "PUBLIC" ||
    data["post"]["visibility"] === "FRIENDS"
      ? true
      : false;
  console.log(data);

  return (
    <div className="message">
      <div className="from">
        <h6>
          <a href={authorUrl}>{data.post.author.displayName}</a>
        </h6>
        {<img alt="author" src={data.post.author.profileImage}></img>}
      </div>
      <div className="postBody">
        {/* Will need to handle other post types here, plain for now */}
        <div className="content-container">
          <h5>
            <Link to={postUrl} state={{ id: data.post }}>
              {data["post"]["title"]}
            </Link>
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
      </div>
    </div>
  );
}

export default PostDetail;

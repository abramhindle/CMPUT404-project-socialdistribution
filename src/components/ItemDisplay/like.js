import "./posts.css";
import { useSelector } from "react-redux";
import profile from "../../images/profile.png";
import { Link } from "react-router-dom";

export default function Like(data) {
  console.log("Data passed to Like obj:", data);

  const port = window.location.port ? `:${window.location.port}` : "";
  const urlSegments = data.data.object.split("/");

  console.log("URL", urlSegments);

  //check type, build links
  const type = data.data.summary.split(" ").pop();
  let postUrl = "";
  const authorUrl = `//${window.location.hostname}${port}/user/${(
    urlSegments[4] ?? ""
  )
    .split("/")
    .pop()}`; // allows linking to the author who wrote the comment
  const objectAuthorUrl = `//${window.location.hostname}${port}/user/${(
    urlSegments[4] ?? ""
  )
    .split("/")
    .pop()}`; // allows linking to the author who wrote the comment

  if (type === "post") {
    console.log(urlSegments);
    let postId = urlSegments.pop();
    // console.log(postId);
    postUrl = objectAuthorUrl + `/post/${postId}`;
  } else if (type === "comment") {
    //Popping 'comments' and 'commentID' off first
    urlSegments.pop();
    urlSegments.pop();
    let postId = urlSegments.pop(); //link to post
    postUrl = objectAuthorUrl + `/post/${postId}`;
  }

  return (
    <div className="hflex like">
      <div className="list-item">
        {/* Profile image w/link to post author's profile */}
        <div className="profile from">
          <a href={authorUrl}>
            {<img alt="author" src={data.data.author.profileImage === "" ? profile : data.data.author.profileImage}></img>}
          </a>
        </div>
        <svg
          version="1.1"
          id="heart-15"
          xmlns="http://www.w3.org/2000/svg"
          width="3em"
          height="3em"
          viewBox="0 0 15 15"
        >
          <path
            className="heart"
            fill="var(--scarlet)"
            d="M13.91,6.75c-1.17,2.25-4.3,5.31-6.07,6.94c-0.1903,0.1718-0.4797,0.1718-0.67,0C5.39,12.06,2.26,9,1.09,6.75&#xA;&#x9;C-1.48,1.8,5-1.5,7.5,3.45C10-1.5,16.48,1.8,13.91,6.75z"
          />
        </svg>

        <h5>
          <Link to={authorUrl}>{data.data.author.displayName}</Link> liked your{" "}
          {type === "post" ? (
            <Link to={postUrl}>post</Link>
          ) : (
            <Link to={postUrl}> comment</Link>
          )}
        </h5>
      </div>
    </div>
  );
}

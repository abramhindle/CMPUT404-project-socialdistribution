import "./posts.css";
import { useSelector } from "react-redux";

export default function FollowRequest(data) {
  const user = useSelector((state) => state.user);
  console.log("Data passed to FollowRequest obj:", data);

  const port = window.location.port ? `:${window.location.port}` : "";
  const authorUrl = `//${window.location.hostname}${port}/user/${(
    data.data.author.id ?? ""
  )
    .split("/")
    .pop()}`; // allows linking to the author who sent request

  return (
    <div className="hflex">
      <div className="list-item">
        {/* Profile image w/link to post author's profile */}
        <div className="profile from">
          <a href={authorUrl}>
          {<img alt="author" src={data.data.author.profileImage}></img>}
          </a>
        </div>
        <h5 style={{"marginLeft":"0", "color":"white"}}>
            <a href={authorUrl}>{data.data.author.displayName}</a>
             wants to follow you!
             <div className="vflex">
                <button>accept</button>
                <button>reject</button>
             </div>
        </h5>

      </div>
    </div>
  );
}
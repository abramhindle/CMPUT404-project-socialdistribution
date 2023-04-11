import "./posts.css";
import { useSelector } from "react-redux";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { get_request } from '../../api/follower_api';
import { delete_request } from '../../api/follower_api';
import { add_followers_for_author } from '../../api/follower_api';
import profile from "../../images/profile.png";

export default function FollowRequest(data) {
  const user = useSelector((state) => state.user);
  console.log("Data passed to FollowRequest obj:", data);
  const [follow_list, setList] = useState({"items": []}); 
  const [success, setSuccess] = useState(false); 
  const navigate = useNavigate();

  const port = window.location.port ? `:${window.location.port}` : "";
  const authorUrl = `//${window.location.hostname}${port}/user/${(
    data.data.actor.id ?? ""
  )
    .split("/")
    .pop()}`; // allows linking to the author who sent request

  useEffect(() => { 
      get_request(user.id, setList)
  }, [success]);

  const DeleteRequest= () => {
    delete_request(user.id, data.data.actor.id, onSuccess)
  }

  const AcceptRequest= () => {
      add_followers_for_author(user.id, data.data.actor.id, onSuccess)
      delete_request(user.id, data.data.actor.id, onSuccess)
  }

  const onSuccess = () => {
      setSuccess(true);
  }

  return (
    <div className="hflex">
      <div className="list-item">
        {/* Profile image w/link to post author's profile */}
        <div className="profile from">
          <a href={authorUrl}>
          {<img alt="author" src={data.data.actor.profileImage === "" ? profile : data.data.actor.profileImage}></img>}
          </a>
        </div>
        <h5>
            <a href={authorUrl}>{data.data.actor.displayName}</a> wants to follow you!
        </h5>

      </div>
      <div className="buttons hflex">
                <button onClick={AcceptRequest}>accept</button>
                <button onClick={DeleteRequest}>reject</button>
      </div>
    </div>
  );
}
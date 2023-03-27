import "./posts.css";
import { useSelector } from "react-redux";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { get_request } from '../../api/follower_api';
import { delete_request } from '../../api/follower_api';
import { add_followers_for_author } from '../../api/follower_api';

export default function FollowRequest(data) {
  const user = useSelector((state) => state.user);
  console.log("Data passed to FollowRequest obj:", data);
  const [follow_list, setList] = useState({"items": []}); 
  const [success, setSuccess] = useState(null); 
  const navigate = useNavigate();

  const port = window.location.port ? `:${window.location.port}` : "";
  const authorUrl = `//${window.location.hostname}${port}/user/${(
    data.data.author.id ?? ""
  )
    .split("/")
    .pop()}`; // allows linking to the author who sent request

    useEffect(() => { 
        get_request(user.id, setList)
      
    }, []);
  
    const DeleteRequest= (actor_id) => {
        delete_request(user.id, actor_id, onSuccess)
    }
  
    const AcceptRequest= (actor_id) => {
        add_followers_for_author(user.id, actor_id, onSuccess)
        delete_request(user.id, actor_id, onSuccess)
    }

    const onSuccess = () => {
        setSuccess(true);
    }
    
    const goBack = () => {
        navigate("/");
    };

  return (
    <div className="hflex">
      <div className="list-item">
        {/* Profile image w/link to post author's profile */}
        <div className="profile from">
          <a href={authorUrl}>
          {<img alt="author" src={data.author.profileImage}></img>}
          </a>
        </div>
        <h5 style={{"marginLeft":"0", "color":"white"}}>
            <a href={authorUrl}>{data.author.displayName}</a>
             wants to follow you!
             <div className="vflex">
                <button onClick={AcceptRequest}>accept</button>
                <button onClick={DeleteRequest}>reject</button>
             </div>
        </h5>

      </div>
    </div>
  );
}
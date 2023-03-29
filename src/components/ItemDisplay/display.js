import Comment from "./comment";
import Post from "./post";
import Like from "./like";
import FollowRequest from "./follow-request";

export default function DisplayItem(props) {
  const data = props.data;
  const liked = props.liked;

  if (data.type === "comment") {
    //display comment
    return <Comment data={data} liked={liked} updateList={props.updateList} />;
  } else if (data.type === "post") {
    //display post
    return (
      <Post post={data} liked={liked} updateList={props.updateList} />
    );
  } else if (data.type === "like") {
    //display like object
    return <Like data={data} />;
  } else if (data.type === "follow") {
    //display follow request object
    return <FollowRequest data={data.object} />;
  } else {
    return;
  }
}

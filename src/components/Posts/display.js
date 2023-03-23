import Comment from "./comment";
import PlainPost from "./post-text";
//TODO : like / follow request objects

export default function DisplayItem(props) {
    const data = props.data;
    const liked = props.liked;

    if (data.type === "comment"){
        //display comment
        return (<Comment data={data} liked={liked}/>);
    }
    else if (data.type === "post"){
        //display post
        return (<PlainPost post={data} liked={liked}/>);
    }
    else if (data.type === "like"){
        //display like object
    }
    else if (data.type === "follow"){
        //display follow request object
    }
    else{
        return;
    }
}
import Comment from "./comment";
import PlainPost from "./post-text";
import Like from "./like";

//TODO : follow request objects

export default function DisplayItem(props) {
    const data = props.data;
    const liked = props.liked;

    if (data.type === "comment"){
        //display comment
        return (<Comment data={data} liked={liked} updateList={props.updateList}/>);
    }
    else if (data.type === "post"){
        //display post
        return (<PlainPost post={data} liked={liked} updateList={props.updateList}/>);
    }
    else if (data.type === "like"){
        //display like object
        return (<Like data={data}/>);
    }
    else if (data.type === "follow"){
        //display follow request object
    }
    else{
        return;
    }
}
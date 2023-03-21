import Comment from "./comment";
import PlainPost from "./post-text";
//TODO : like / follow request objects

export default function DisplayItem(data) {
    if (data.type === "comment"){
        //display comment
    }
    else if (data.type === "post"){
        //display post
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
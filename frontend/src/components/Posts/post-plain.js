import "./posts.css"
import { useState } from "react";
import { author_api } from "../../api/post_display_api";

export default function PlainPost(data) {
    //Get Author data
    const [author, setAuthor] = useState("");
    author_api(data["post"]["author"], setAuthor);
    
    //Decide if shareable
    let shareable = (data["post"]["visibility"] === "PUBLIC" || data["post"]["visibility"] === "FRIENDS") ? true : false

    return (
        <div className="message">
            <div className="from">
                <img alt="author" src={author["profileImage"]}></img>
            </div>
            {/* Will need to handle other post types here, plain for now */}
            <div className="content-container">
                <h5>{data["post"]["title"]}</h5>
                <div className="content">
                    {data["post"]["content"]}
                </div>
                <div className="timestamp">{data["post"]["published"]}</div>
                </div>
            <div className="interaction-options">
                <button>like</button>
            {shareable && <div className="share">        {/* Only show if shareable */}
                <button>share</button>
            </div>}
            </div>
        </div>

    );
}
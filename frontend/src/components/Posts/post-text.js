import "./posts.css"
import { useState } from "react";
import { author_api } from "../../api/post_display_api";
import ReactMarkdown from 'react-markdown'

export default function PlainPost(data) {
    //Get Author data -> author data is attached to data
    
    //Decide if shareable
    let shareable = (data["post"]["visibility"] === "PUBLIC" || data["post"]["visibility"] === "FRIENDS") ? true : false;
    console.log(data)
    let markdown = data["post"]["contentType"] === "text/markdown" ? true : false;

    const port = window.location.port ? `:${window.location.port}` : "";
    const authorUrl = `//${window.location.hostname}${port}/user/${(data.post.author.id ?? "").split('/').pop()}`; // allows linking to the author who wrote the post

    if (markdown) {
        console.log(data["post"], " is a markdown post");
    }
    
    return (
        <div>
            <div className="message">
                <div className="from">
                    <h6><a href={authorUrl}>{data.post.author.displayName}</a></h6>
                    {<img alt="author" src={data.post.author.profileImage}></img>}
                </div>
                <div className="postBody">
                        {/* Will need to handle other post types here, plain for now */}
                    <div className="content-container">
                        <h5>{data["post"]["title"]}</h5>
                        {markdown && <ReactMarkdown className="content line">
{data["post"]["content"]}
                        </ReactMarkdown>}
                        {(!markdown) && <div className="content line">
                            {data["post"]["content"]}
                        </div>}
                        </div>
                        <div className="interaction-options">
                            <button>like</button>
                            {shareable && <div className="share">        {/* Only show if shareable */}
                            <button>share</button>
                        </div>}
                    </div>
                </div>
            </div>
            <div className="timestamp">{data["post"]["published"]}</div>
        </div>

    );
}
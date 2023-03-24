import { useState } from "react";

export default function CommentArrow(props){
    const [commentFieldVisibilty, setCommentFieldVisibilty] = useState(false);

    const submitComment = () => {
        setCommentFieldVisibilty(false);
        props.submit();
    }

    return (
        <>
        <button className="interact"
            onClick={() =>
            setCommentFieldVisibilty(commentFieldVisibilty ? false : true)
            }
        >
            <svg width="calc(2.5em)" height="calc(0.77*2.5em)" viewBox="0 0 18 14" version="1.1" >
            {/*-- Generator: Sketch 52.5 (67469) - http://www.bohemiancoding.com/sketch --*/}
            <title>Comment</title>
            <desc>Created with Sketch.</desc>
            <g id="Icons" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                <g id="Rounded" transform="translate(-579.000000, -1532.000000)">
                    <g id="Content" transform="translate(100.000000, 1428.000000)">
                        <g id="-Round-/-Content-/-reply" transform="translate(476.000000, 98.000000)">
                            <g>
                                <polygon id="Path" points="0 0 24 0 24 24 0 24"></polygon>
                                <path d="M10,9 L10,7.41 C10,6.52 8.92,6.07 8.29,6.7 L3.7,11.29 C3.31,11.68 3.31,12.31 3.7,12.7 L8.29,17.29 C8.92,17.92 10,17.48 10,16.59 L10,14.9 C15,14.9 18.5,16.5 21,20 C20,15 17,10 10,9 Z" id="🔹Icon-Color" fill="#1D1D1D"></path>
                            </g>
                        </g>
                    </g>
                </g>
            </g>
            </svg>
        </button>
      
        {commentFieldVisibilty && (
            <div className="comment-input-form">
            <input
                type="radio"
                id="text"
                name="contentType"
                value="text/plain"
                defaultChecked
                onChange={(e) => props.setCommentType(e.target.value)}
            />
            <label htmlFor="text">Text</label>
            <input
                type="radio"
                id="markdown"
                name="contentType"
                value="text/markdown"
                onChange={(e) => props.setCommentType(e.target.value)}
            />
            <label htmlFor="markdown">Markdown</label>
            <input
                onChange={(e) => props.setComment(e.target.value)}
                placeholder="Enter the comment here"
                type="text"
            />
            <button onClick={submitComment}>Submit</button>
            </div>
            )}
        </>
    );
}
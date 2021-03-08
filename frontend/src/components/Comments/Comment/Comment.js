import React from 'react'

export default function Comment(props) {
    return (
        <div>
            <p>Comment by: {props.comment.author.displayName}</p>
            <p>Content: {props.comment.comment}</p>
        </div>
    )
}

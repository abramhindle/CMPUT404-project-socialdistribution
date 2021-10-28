import React from "react"
import { Parser, HtmlRenderer } from "commonmark";

const TextPost = ({ post }) => {
  const CMParser = new Parser({ safe: true });
  const CMWriter = new HtmlRenderer();

  console.log(post)

  return (
    <>{ post.contentType === "text/plain" ?
        <p>{post.content}</p>
      :
        <div
          className='cmPreview'
          dangerouslySetInnerHTML={{
            __html: CMWriter.render(CMParser.parse(post.content)),
          }}
        ></div>
    }</>
  )
}

export default TextPost;
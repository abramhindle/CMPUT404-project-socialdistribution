import { Parser, HtmlRenderer } from "commonmark";

const Comment = ({ comment }) => {
  const CMParser = new Parser({ safe: true });
  const CMWriter = new HtmlRenderer();

  console.log(comment)

  return (
    <div>
      { comment?.author &&
      <>
        <h2>{comment.author.displayName}</h2>
        { comment.contentType === "text/plain" ? 
            <div className='cmPreview'>{comment.comment}</div> 
          :
            <div
              className='cmPreview'
              dangerouslySetInnerHTML={{
                __html: CMWriter.render(CMParser.parse(comment.comment)),
              }}
            ></div>
      }</>}
    </div>
  );
};

export default Comment;
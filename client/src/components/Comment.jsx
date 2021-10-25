import { Parser, HtmlRenderer } from "commonmark";

const Comment = ({ comment }) => {
  const CMParser = new Parser();
  const CMWriter = new HtmlRenderer();

  return (
    <div>
      { comment?.author &&
      <>
        <h2>{comment.author.displayName}</h2>
        { comment.contentType === "text/plain" ? 
            <div className='cmPreview'>{comment}</div> 
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
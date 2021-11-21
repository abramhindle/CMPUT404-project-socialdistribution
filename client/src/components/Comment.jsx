import { Parser, HtmlRenderer } from "commonmark";
import MiniProfile from "./MiniProfile";

const Comment = ({ comment }) => {
  const CMParser = new Parser({ safe: true });
  const CMWriter = new HtmlRenderer();

  console.log(comment)

  return (
    <div>
      { comment?.author &&
      <>
        <MiniProfile author={comment.author} />
        { comment.contentType === "text/plain" ? 
            <div className='comment'>{comment.comment}</div> 
          :
            <div
              className='comment'
              dangerouslySetInnerHTML={{
                __html: CMWriter.render(CMParser.parse(comment.comment)),
              }}
            ></div>
      }</>}
    </div>
  );
};

export default Comment;
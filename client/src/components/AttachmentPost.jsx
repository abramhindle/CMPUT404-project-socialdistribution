const AttachmentPost = ({ post }) => {
    return (
      <div>
        <p>{post.description}</p>
        <a download={post.title} href={post.content}>Download</a>
        <br></br>
        <br></br>
      </div>
    )
};

export default AttachmentPost;
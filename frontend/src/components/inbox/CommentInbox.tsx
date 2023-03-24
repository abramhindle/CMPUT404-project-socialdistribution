import React from 'react'
import { Comment } from '@/index';
interface CommentInboxProps {
    comment: Comment
}

const CommentInbox: React.FC<CommentInboxProps> = ({comment}) => {
        return (<div className="border border-gray-200 rounded-md p-4">
            <div className="flex  mb-3 space-x-3 font-medium text-gray-700">
               {comment.author.displayName} commented on your post.
            </div>
            <div className='text-sm text-gray-600'> 
                {comment.comment}
            </div>
        </div>);
}
export default CommentInbox
import React from 'react'
import { Comment } from '@/index';
import Link from 'next/link';
interface CommentInboxProps {
    comment: Comment
}

const CommentInbox: React.FC<CommentInboxProps> = ({comment}) => {
        return (<div className="border border-gray-200 rounded-md p-4">
            <div className="flex  mb-3 space-x-3 font-medium text-gray-700">
               <span><Link 
                className=' text-gray-500 hover:underline'
               href={
                    `/authors/${comment.author?.id.split('/').pop()}`
               }>{comment.author?.displayName}</Link> commented on your post.</span>
            </div>

            <div className='text-sm text-gray-600'> 
                {comment.comment}
            </div>
        </div>);
}
export default CommentInbox
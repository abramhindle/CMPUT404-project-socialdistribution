import React from 'react'
import { Like } from '@/index';
import Link from 'next/link';
interface LikeInboxProps {
    like: Like
}

const LikeInbox: React.FC<LikeInboxProps> = ({like}) => {
        return (<div className='border border-gray-200 rounded-md p-4 shadow-sm'>
            <Link 
            href={
                 `/authors/${like.author.id.split('/').pop()}/posts/${like.object.match(/(?<=\/posts\/)(.*?)(?=\/comments)/g)}`  
            }
            dangerouslySetInnerHTML={{__html: like.summary}}
            className="flex space-x-3 font-medium text-gray-500 hover:underline">     
            </Link>
        </div>);
}
export default LikeInbox
import React from 'react'
import { Like } from '@/index';
interface LikeInboxProps {
    like: Like
}

const LikeInbox: React.FC<LikeInboxProps> = ({like}) => {
        return (<div className='border border-gray-200 rounded-md p-4 shadow-sm'>
            <div 
            dangerouslySetInnerHTML={{__html: like.summary}}
            className="flex space-x-3 font-medium text-gray-600">
               
            </div>
        </div>);
}
export default LikeInbox
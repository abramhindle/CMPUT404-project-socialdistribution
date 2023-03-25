import React, {useEffect} from 'react'
import {  Follow } from '@/index';
import NodeManager from '@/nodes';
import Link from 'next/link';

interface CommentInboxProps {
    follow: Follow
}

const FollowInbox: React.FC<CommentInboxProps> = ({follow}) => {
    const [isFollow, setIsFollow] = React.useState(false)

    useEffect(() => {
        let actorId = follow.actor.id.split('/').pop() || ''
        let objectId = follow.object.id.split('/').pop() || ''

        NodeManager.checkFollowerStatus(objectId, actorId).then((isfollow) => {
            setIsFollow(isfollow !== 'pending')
        })
    }, [isFollow])

    const approveFollow = async () => {
        let actorId = follow.actor.id.split('/').pop() || ''
        let objectId = follow.object.id.split('/').pop() || ''
        await NodeManager.addFollower(objectId, actorId)
        setIsFollow(true)
    }

    const rejectFollow = async () => {
        let actorId = follow.actor.id.split('/').pop() || ''
        let objectId = follow.object.id.split('/').pop() || ''
        await NodeManager.removeFollower(objectId, actorId)
        setIsFollow(true)
    }

        return (<div className="border border-gray-200 rounded-md p-4">
            <div className="flex space-x-3 font-medium items-center justify-between text-gray-700">
               <span>{follow.summary}</span>
               <Link href={
                    `/authors/${follow.actor.id.split('/').pop()}`
               } className='text-sm text-gray-500 hover:underline'>
                     {follow.actor.displayName}
                </Link>
            </div>
            {follow.summary.includes('wants') && !isFollow && <div className='space-x-3'>
            <button className='border text-gray-500 hover:bg-gray-50 border-gray-300 shadow-sm rounded-md px-3 py-1 text-sm' onClick={approveFollow}>Approve</button>
            <button className='text-red-500 border-red-500 border hover:bg-gray-50 bg-white rounded-md px-3 py-1 text-sm' onClick={rejectFollow}>Reject</button>
            </div>}
        </div>);
}
export default FollowInbox
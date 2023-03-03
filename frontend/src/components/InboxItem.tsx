import React from 'react'
import Link from 'next/link';



interface AuthorProps {
	id?: string;
	host?: string;
	displayName: string;
	url: string;
	github?: string;
	profileImage: string;
}

interface InboxItemProps {
	type: 'follow' | 'like' | 'comment' | 'reshare'
	author: AuthorProps;
}

const InboxItem: React.FC<InboxItemProps> = ({author, type}) => {
		return (<div>
			<div className="flex items-center space-x-3  p-4 border-b border-gray-100">
			  <img className="w-10 h-10 rounded-full" src={author.profileImage} alt=""/>
			  <div className="text-sm">
				<Link href={author.url} className="text-gray-900 dark:text-gray-100">{author.displayName}</Link>
				{
					type === 'follow' && <p className="text-gray-600 dark:text-gray-400">started following you</p>
				}
				{
					type === 'like' && <p className="text-gray-600 dark:text-gray-400">liked your post</p>
				}
				{
					type === 'comment' && <p className="text-gray-600 dark:text-gray-400">commented on your post</p>
				} {
					type === 'reshare' && <p className="text-gray-600 dark:text-gray-400">reshared your post</p>
				}

			  </div>
			</div>
			
		</div>);
}
export default InboxItem
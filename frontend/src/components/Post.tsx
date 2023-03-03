import React, {useEffect} from 'react'
import Link from 'next/link';
import Markdown from 'markdown-to-jsx';
import {HandThumbUpIcon} from '@heroicons/react/24/outline';
import {HandThumbUpIcon as HandThumbUpIconSolid} from '@heroicons/react/24/solid';

interface AuthorProps {
	id: string;
	host: string;
	displayName: string;
	url: string;
	github: string;
	profileImage: string;
}

interface PostProps {
	title: string;
	id: string;
	source: string;
	origin: string;
	description: string;
	contentType: 'text/markdown' | 'text/plain' | 'image/*' | 'image/link';
	content: string;
	author: AuthorProps;
	categories: string[];
	count: number;
	visibility?: string;
	unlisted?: boolean;
	published?: string;
	comments: string;
}

const ThumbUp = ({...props}) => {
	return (
		<svg {...props} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className='w-6 h-6 mr-8 cursor-pointer text-gray-700' >
  <path strokeLinecap="round" strokeLinejoin="round" d="M6.633 10.5c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 012.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 00.322-1.672V3a.75.75 0 01.75-.75A2.25 2.25 0 0116.5 4.5c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 01-2.649 7.521c-.388.482-.987.729-1.605.729H13.48c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 00-1.423-.23H5.904M14.25 9h2.25M5.904 18.75c.083.205.173.405.27.602.197.4-.078.898-.523.898h-.908c-.889 0-1.713-.518-1.972-1.368a12 12 0 01-.521-3.507c0-1.553.295-3.036.831-4.398C3.387 10.203 4.167 9.75 5 9.75h1.053c.472 0 .745.556.5.96a8.958 8.958 0 00-1.302 4.665c0 1.194.232 2.333.654 3.375z" />
</svg>
	)
	
}


const ThumbUpSolid = ({...props}) => {
	return (
		<svg {...props} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className='w-6 h-6 mr-8 cursor-pointer text-gray-700'>
  <path d="M7.493 18.75c-.425 0-.82-.236-.975-.632A7.48 7.48 0 016 15.375c0-1.75.599-3.358 1.602-4.634.151-.192.373-.309.6-.397.473-.183.89-.514 1.212-.924a9.042 9.042 0 012.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 00.322-1.672V3a.75.75 0 01.75-.75 2.25 2.25 0 012.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 01-2.649 7.521c-.388.482-.987.729-1.605.729H14.23c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 00-1.423-.23h-.777zM2.331 10.977a11.969 11.969 0 00-.831 4.398 12 12 0 00.52 3.507c.26.85 1.084 1.368 1.973 1.368H4.9c.445 0 .72-.498.523-.898a8.963 8.963 0 01-.924-3.977c0-1.708.476-3.305 1.302-4.666.245-.403-.028-.959-.5-.959H4.25c-.832 0-1.612.453-1.918 1.227z" />
</svg>
	)
}
const Post: React.FC<PostProps> = ({title, description, contentType, content, source, categories, author, count, comments}) => {
	const [liked, setLiked] = React.useState(false);
		return (<div>
			<div className="flex flex-col border border-gray-100 shadow-sm rounded-sm mb-4">
				<h2 className='text-xl text-gray-700 font-semibold px-6 pt-4'>{title}</h2>
				
				<div className={`my-3 border-t border-b border-gray-100 ${!contentType.includes('image')? 'p-5':''}`}>
					<>{contentType === 'text/markdown' && 
					<Markdown
					options={{
						overrides: {
							h1: { component: 'h1', props: { className: 'text-2xl font-semibold text-gray-700' } },
							h2: { component: 'h2', props: { className: 'text-xl font-semibold text-gray-700' } },
							h3: { component: 'h3', props: { className: 'text-lg font-semibold text-gray-700' } },
							h4: { component: 'h4', props: { className: 'text-base font-semibold text-gray-700' } },
							h5: { component: 'h5', props: { className: 'text-sm font-semibold text-gray-700' } },
							h6: { component: 'h6', props: { className: 'text-xs font-semibold text-gray-700' } },
							p: { component: 'p', props: { className: 'text-gray-700' } },
							a: { component: 'a', props: { className: 'text-blue-500' } },
							ul: { component: 'ul', props: { className: 'list-disc list-inside' } },
							ol: { component: 'ol', props: { className: 'list-decimal list-inside' } },
							li: { component: 'li', props: { className: 'text-gray-700' } },
							table: { component: 'table', props: { className: 'table-auto' } },
							th: { component: 'th', props: { className: 'border px-4 py-2' } },
							td: { component: 'td', props: { className: 'border px-4 py-2' } },
							tr: { component: 'tr', props: { className: 'bg-gray-100' } },
							thead: { component: 'thead', props: { className: 'bg-gray-200' } },
							tbody: { component: 'tbody', props: { className: 'bg-gray-100' } },
							blockquote: { component: 'blockquote', props: { className: 'border-l-4 border-gray-200 pl-4 italic' } },
							img: { component: 'img', props: { className: 'w-full' } },
							br: { component: 'br', props: { className: 'w-full' } },
							b: { component: 'b', props: { className: 'font-bold' } },
							i: { component: 'i', props: { className: 'italic' } },
							em: { component: 'em', props: { className: 'italic' } },
							strong: { component: 'strong', props: { className: 'font-bold' } },
							code: { component: 'code', props: { className: 'bg-gray-200 rounded-sm px-1' } },
							pre: { component: 'pre', props: { className: 'bg-gray-200 rounded-sm px-1' } },
							hr: { component: 'hr', props: { className: 'border-gray-200' } },
						}
					}}
					>{content}</Markdown>
					}
					{contentType === 'text/plain' && <p>{content}</p>}
					{contentType === 'image/*' && <img className='object-cover w-full' src={content} alt={title} />}
					{contentType === 'image/link' && <img className='object-cover w-full' src={content} alt={title} />}</>
				</div>
				<div className='flex flex-row items-center justify-between'>
				<p className='text-sm text-gray-500 px-6'>{description}</p>
				<span className='ml-6'>
				{!liked && <ThumbUp className='h-6 w-6 text-gray-400 hover:text-gray-500 px-6 cursor-pointer' onClick={() => setLiked(true)} />}
				{liked && <ThumbUpSolid className='h-6 w-6 text-gray-400 hover:text-gray-500 px-6 cursor-pointer' onClick={() => setLiked(false)} />}
				</span>
				</div>
				<p className='px-6'>{
					
					categories.map((category, index) => {
						let comma = index === categories.length - 1 ? '' : ', ';
						return (<span key={index} className='text-gray-400 text-sm'>{category}{comma} </span>);
					})}

					</p>
					<div className='flex flex-row justify-between items-center mb-2 px-6'>
				<Link href={source} className='text-blue-500 hover:underline text-sm'>source</Link>
				<Link className={'text-gray-500 font-medium text-sm'} href={author.url}>Posted By {author.displayName}</Link>
				</div>
				<div className='px-6 py-2 flex flex-row items-center justify-between text-gray-400 border-t border-gray-200 text-sm'>
					<span>{count} comments</span>
					<Link href={comments}>View all comments</Link>
				</div>
			</div>	
		</div>);
}
export default Post
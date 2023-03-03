/* eslint-disable @next/next/no-img-element */
import React, {useEffect} from 'react'
import Link from 'next/link';
import Markdown from 'markdown-to-jsx';
import { EllipsisHorizontalIcon } from '@heroicons/react/24/outline';
import { ThumbsUp, Share, Link2 } from 'react-feather';
import { Tooltip } from '@material-tailwind/react';
import { Menu } from '@headlessui/react'
import {Post as PostProps} from '@/index';
import axios from '@/utils/axios';
import { useRouter } from 'next/router';


const Post: React.FC<PostProps> = ({title, description, contentType, content, source, categories, author, count, comments, id}) => {
	const [liked, setLiked] = React.useState(false);
	const router = useRouter()
		return (<div >
			<div className="flex flex-col border border-gray-100 shadow-sm rounded-sm mb-4"> 
				<div className="flex flex-row justify-between items-center pt-4 px-5"><Link href={`/post/${id}`}><h2 className='text-base hover:underline text-gray-700 font-semibold'>{title}</h2></Link>
					<div>
					<Menu as='div' className='relative'>
						<Menu.Button>
					<EllipsisHorizontalIcon className='w-7 h-7 text-gray-700 cursor-pointer' />
						</Menu.Button>
						<Menu.Items className={'absolute right-0 mt-0 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none'}>
							<Menu.Item>
								{({ active }) => (
									<Link className={`block px-4 py-2 text-sm text-gray-700 ${active ? 'bg-gray-100' : ''}`} href={`/post/${id}/edit`}>
										Edit
									</Link>
								)}
							</Menu.Item>
							<Menu.Item>
								{({ active }) => (
									<Link onClick={
										async () => {
											await axios.delete(`/authors/${author.id}/posts/${id}`)
											if (router.pathname === `/post/${id}`) {
												router.push('/')
											} else  {
												router.reload()
											}
							
										}	
									} className={`block px-4 py-2 text-sm text-gray-700 ${active ? 'bg-gray-100' : ''}`} href="#">
										Delete
									</Link>
								)}
							</Menu.Item>
						</Menu.Items>
					</Menu>
					</div>
				</div>
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
					{contentType === 'image/*' && <img className='object-cover w-full h-full' src={content} alt={title} />}
					{contentType === 'image/link' && <img className='object-cover w-full h-full' src={content} alt={title} />}</>
				</div>
				<div className='flex flex-row items-center justify-between px-6'>
				<p className='text-sm text-gray-500 '>{description}</p>
				<span className='flex flex-row space-x-3 '>
				<div className='border-r border-gray-200 pr-3'>
				{!liked && <ThumbsUp className='h-5 w-5 text-gray-400 hover:text-gray-500 cursor-pointer' onClick={() => setLiked(true)} />}
				{liked && <ThumbsUp className='h-5 w-5  fill-pink-600 text-pink-600 hover:text-pink-600 cursor-pointer' onClick={() => setLiked(false)} />}
				</div>
				<Tooltip content='Reshare Post'>
				<Share className='h-5 w-5 text-gray-400 hover:text-gray-500 cursor-pointer' />
				
				</Tooltip>
				<Tooltip content='Copy Link'>
				<Link2 className='h-5 w-5 text-gray-400 hover:text-gray-500 cursor-pointer'  onClick={() => {
					navigator.clipboard.writeText(
						`${window.location.protocol}//${window.location.host}/post/${id}`
					);
				}}/>
				</Tooltip>
				</span>
				</div>
				<p className='px-6'>{
					categories.map((category, index) => {
						let comma = index === categories.length - 1 ? '' : ', ';
						return (<span key={index} className='text-gray-400 text-sm'>{category}{comma} </span>);
					})}
					</p>
					<div className='flex flex-row justify-between items-center mb-2 px-6'>
				<Link href={source || '#'} className='text-blue-500 hover:underline text-sm'>source</Link>
				<Link className={'text-gray-500 font-medium text-sm mt-1'} href={author.url || '/authors/'+ author.id}>Posted By {author.displayName}</Link>
				</div>
				<div className='px-6 py-2 flex flex-row items-center justify-between text-gray-400 border-t border-gray-200 text-sm'>
					<span>{count} comments</span>
					<Link href={comments}>View all comments</Link>
				</div>
			</div>	
		</div>);
}
export default Post
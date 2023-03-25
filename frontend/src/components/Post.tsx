/* eslint-disable @next/next/no-img-element */
import React, { useEffect,Fragment } from 'react'
import Link from 'next/link';
import Markdown from 'markdown-to-jsx';
import { EllipsisHorizontalIcon } from '@heroicons/react/24/outline';
import { ThumbsUp, Share, Link2, MessageCircle } from 'react-feather';
import { Tooltip } from '@material-tailwind/react';
import { Menu } from '@headlessui/react'
import {Post as PostProps, Comment as CommentI} from '@/index';
import NodeManager from '@/nodes';
import { useRouter } from 'next/router';
import { useUser } from '@supabase/auth-helpers-react';
import { Transition, Dialog } from '@headlessui/react';
import {useForm, FormProvider } from 'react-hook-form';
import TextArea from './Textarea';
import Button from './Button';
import Comment from './Comment';

interface PostPr {
	post: PostProps
	comments?: CommentI[]
}

const Post: React.FC<PostPr> = ({post, comments}) => {
	const [liked, setLiked] = React.useState(false);
	const user = useUser()
	const router = useRouter();
	const [isOpen, setIsOpen] = React.useState(false)
	const commentForm = useForm();
	const closeModal = () => {
		setIsOpen(false);
		commentForm.reset();
	}
	
	useEffect(() => {
		
		let postId = post.id.split('/').pop()
		if (!user)
			return;
		NodeManager.isPostLiked(postId || '', user?.id || ``).then((res) => {
			if (res) {
				setLiked(true)
			}
		})
		

	}, [user])

	const likePost =async () => {
		let authorId = post.author.id.split('/').pop() || '';
		if (liked)
			return;
		let authorUser = await NodeManager.getAuthor(user?.id || ``)
		if (authorUser) {
			await NodeManager.createLike(authorId, post, authorUser);
			setLiked(true)
		}
		
	}

	const onSubmit = async (data:any) => {
		let authorId = post.author.id.split('/').pop() || '';
		let postId = post.id.split('/').pop() || '';
		let authorUser = await NodeManager.getAuthor(user?.id || ``)
		
		if (authorUser) {
			let comment:CommentI = {
			type:'comment',
			comment: data.comment,
			contentType: 'text/plain',
			published: new Date().toISOString(),
			author:authorUser
		}
		await NodeManager.createComment(authorId, postId, comment);
		let link = `/authors/${post.author.id.split('/').pop()}/posts/${post.id.split('/').pop()}`;
		await router.push(link);
		}
		
		closeModal()
	}

	
		return (<div >
			<div className="flex flex-col border border-gray-100 shadow-sm rounded-sm mb-4"> 
				<div className="flex flex-row justify-between items-center pt-4 px-5"><Link href={`/authors/${post.author.id.split('/').slice(-1)}/posts/${post.id.split('/').slice(-1)}`}><h2 className='text-base hover:underline text-gray-700 font-semibold'>{post.title}</h2></Link>
					<div>
					{post.author.id.includes(user?.id || '') && <Menu as='div' className='relative'>
						<Menu.Button>
					<EllipsisHorizontalIcon className='w-7 h-7 text-gray-700 cursor-pointer' />
						</Menu.Button>
						<Menu.Items className={'absolute right-0 mt-0 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none'}>
							<Menu.Item>
								{({ active }) => (
									<Link className={`block px-4 py-2 text-sm text-gray-700 ${active ? 'bg-gray-100' : ''}`} href={`/authors/${user?.id || ''}/posts/${post.id.split('/').slice(-1)}/edit`}>
										Edit
									</Link>
								)}
							</Menu.Item>
							<Menu.Item>
								{({ active }) => (
									<Link onClick={
										async () => {
											let postId = post.id.split('/').pop() 
											let authorId = post.author.id.split('/').pop()
											await NodeManager.deletePost(authorId || '', postId || '');
											await router.reload();
										}	
									} className={`block px-4 py-2 text-sm text-gray-700 ${active ? 'bg-gray-100' : ''}`} href="#">
										Delete
									</Link>
								)}
							</Menu.Item>
						</Menu.Items>
					</Menu>}
					</div>
				</div>
				<div className={`my-3 border-t border-b border-gray-100 ${!post.contentType.includes('image')? 'p-5':''}`}>
					<>{post.contentType === 'text/markdown' && 
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
					>{post.content}</Markdown>
					}
					{post.contentType === 'text/plain' && <p>{post.content}</p>}
					{post.contentType === 'image/*' && <img className='object-cover w-full h-full' src={post.content} alt={post.title} />}
					{post.contentType === 'image/link' && <img className='object-cover w-full h-full' src={post.content} alt={post.title} />}</>
				</div>
				<div className='flex flex-row items-center justify-between px-6'>
				<p className='text-sm text-gray-500 '>{post.description}</p>
				<span className='flex flex-row space-x-3 '>
				<div className='border-r border-gray-200 pr-3 flex space-x-2 items-center justify-center'>
					<MessageCircle className='h-5 w-5 text-gray-400 hover:text-gray-500 cursor-pointer' onClick={() => setIsOpen(true)}/>
				{!liked && <ThumbsUp className='h-5 w-5 text-gray-400 hover:text-gray-500 cursor-pointer' onClick={likePost} />}
				{liked && <ThumbsUp className='h-5 w-5 text-pink-600 hover:text-pink-600 cursor-pointer'  />}
				</div>
				<Tooltip content='Reshare Post'>
				<Share className='h-5 w-5 text-gray-400 hover:text-gray-500 cursor-pointer' />
				
				</Tooltip>
				<Tooltip content='Copy Link'>
				<Link2 className='h-5 w-5 text-gray-400 hover:text-gray-500 cursor-pointer'  onClick={() => {
					navigator.clipboard.writeText(
						`${window.location.protocol}//${window.location.host}/authors/${post.author.id.split('/').pop()}/posts/${post.id.split('/').pop()}`
					);
				}}/>
				</Tooltip>
				</span>
				</div>
				<p className='px-6'>{
					post.categories.map((category, index) => {
						let comma = index === post.categories.length - 1 ? '' : ', ';
						return (<span key={index} className='text-gray-400 text-sm'>{category}{comma} </span>);
					})}
					</p>
					<div className='flex flex-row justify-between items-center mb-2 px-6'>
				<Link href={post.source || '#'} className='text-blue-500 hover:underline text-sm'>source</Link>
				<Link className={'text-gray-500 font-medium text-sm mt-1'} href={post.author.url || '/authors/'+ post.author.id}>Posted By {post.author.displayName}</Link>
				</div>
				<div className='px-6 py-2 flex flex-row items-center justify-between text-gray-400 border-t border-gray-200 text-sm'>
					<span>{comments ? comments.length: post.count} comments</span>
					{!comments && <Link href={`/authors/${post.author.id.split('/').pop()}/posts/${post.id.split('/').pop()}`}>View all comments</Link>}
					
				</div>
				<div className=' border-t border-gray-200'>
					{comments && comments.map((comment, index) => {
						return <Comment {...comment} key={index} />
					})}
					</div>
				<Transition appear show={isOpen} as={Fragment}>
        <Dialog as="div" className="relative z-10" onClose={closeModal}>
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-black bg-opacity-25" />
          </Transition.Child>

          <div className="fixed inset-0 overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4 text-center">
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 scale-95"
                enterTo="opacity-100 scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 scale-100"
                leaveTo="opacity-0 scale-95"
              >
                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                  <Dialog.Title
                    as="h3"
                    className="text-lg font-medium leading-6 text-gray-900"
                  >
                    {post.title} Comment
                  </Dialog.Title>
				  <FormProvider {...commentForm}>
						<form onSubmit={commentForm.handleSubmit(onSubmit)}>
							<div className="mt-4">
								<TextArea register={commentForm.register} id='comment' name='' placeholder='Say Something...' />
							</div>
							<div className="mt-4">
								<Button name='Submit' className='w-full text-white'/>
							</div>
						</form>
					</FormProvider>
                 
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </Dialog>
      </Transition>
			</div>	
		</div>);
}
export default Post
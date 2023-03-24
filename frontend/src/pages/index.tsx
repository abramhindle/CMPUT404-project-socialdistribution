import React from 'react'
import dynamic from 'next/dynamic';
const Post = dynamic(() => import('@/components/Post'), { ssr: false });
import Sidebar from '@/components/Sidebar';
import Head from 'next/head';
import { GetServerSideProps } from 'next';
import { createServerSupabaseClient } from '@supabase/auth-helpers-nextjs';
import NodeManager from '@/nodes';
import { Follow, InboxListItem, Post, Comment, Like } from '@/index';
import CommentInbox from '@/components/inbox/CommentInbox';
import FollowInbox from '@/components/inbox/FollowInbox';
import LikeInbox from '@/components/inbox/LikeInbox';

interface streamProps {
	inbox: InboxListItem
}

const Stream: React.FC<streamProps> = ({inbox}) => {

		return (
			
			<div className='flex flex-col h-screen'>
				<Head>
					<title>Stream</title>
				</Head>
		<div className='flex flex-1 overflow-hidden'>
				<Sidebar/>
		<div className='flex flex-1 flex-col overflow-y-auto w-full py-12'>
			
		<div className='w-full mx-auto bg-white px-6 max-w-4xl space-y-2'>
			{inbox.items.map((item) => {
				
				switch (item.type.toLowerCase()) {
					case 'post':
						item = item as Post;
						return <Post post={item} key={item.id} />;
					case 'follow':
						item = item as Follow;
						return <FollowInbox follow={item} key={item.summary} />;
					case 'like':
						item = item as Like;
						return <LikeInbox like={item} key={item.summary} />;
					case 'comment':
						item = item as Comment;
						return <CommentInbox comment={item} key={item.id || item.published} />;
				}
			})}
		</div>
		{
			inbox.items.length === 0 && (
				<div className='w-full mx-auto bg-white px-6 max-w-4xl'>
					<div className='flex flex-col items-center justify-center h-full'>
						<h1 className='text-3xl font-bold text-gray-700 mb-3'>No Activity Yet</h1>
						<p className='text-gray-500'>
							Maybe follow some friends so you can have some activity?
						</p>
					</div>
				</div>
			)
		}
		</div>
		</div></div>);
}
export default Stream

export const getServerSideProps:GetServerSideProps = async (context) => {

	const supabaseServerClient = createServerSupabaseClient(context)
	  const {
		data: { user },
	  } = await supabaseServerClient.auth.getUser();

	  if (!user) {
		return {
		  redirect: {
			destination: '/auth',
			permanent: false
		  }
		}
	  }

	   if (!await NodeManager.checkAuthorExists(user.id)) {
		return {
			redirect: {
				destination: '/onboarding',
				permanent: false
			}
		}
	  }
 
	let inbox = await NodeManager.getInbox(user.id)
	
	let inboxItems = inbox.items.map(async (item) => {
		try {
			if (item.type.toLowerCase() === 'post') {
			item = item as Post;
			let url = item.id.split('/')
			let id = url[url.length - 1]
			let authorId = url[url.length - 3] 
			let it = await NodeManager.getPost(authorId, id);
			if (!it) {
				return item;
			}
			return it;
		} else {
			return item;
		}
		}	 catch (error) {
			return item;
		}
		
	})

	inbox.items = await Promise.all(inboxItems)
	  
	return {
	  props: {
		inbox
	  }
	}
  }


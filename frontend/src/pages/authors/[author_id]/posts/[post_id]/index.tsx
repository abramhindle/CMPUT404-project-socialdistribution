import React from 'react'
import { GetServerSideProps } from 'next';
import Button from '@/components/Button';
import { NextPage } from 'next';
import Link from 'next/link';
import SideBar from '@/components/Sidebar';
import Post from '@/components/Post';
import { useUser, useSupabaseClient } from '@supabase/auth-helpers-react'
import Head from 'next/head';
import { useRouter } from 'next/router';
import { createServerSupabaseClient } from '@supabase/auth-helpers-nextjs';
import { Author, Post as PostType, Comment } from '@/index';
import NodeManager from '@/nodes';

interface Props {
	post: PostType,
	comments: Comment[]
}

const Page: NextPage<Props> = ({post, comments}) => {
	const supabaseClient = useSupabaseClient()
  	const user = useUser();
	const router = useRouter();

		return (
		<div className='flex flex-col h-screen'>
		<Head>
			<title>{post.title}</title>
		</Head>
		
		<div className='flex flex-1 overflow-hidden'>
		<SideBar/>
		<div className='flex flex-1 flex-col overflow-y-auto w-full py-12'>
            <div className='w-full mx-auto bg-white px-6 max-w-5xl'>
	        <Post post={post} comments={comments}/>
            </div>
			</div>
		</div></div>);
}

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

	  try {
		let [authorId, postId] = [context.params?.author_id, context.params?.post_id]

        let post = await NodeManager.getPost(authorId as string, postId as string);
		let comments = await NodeManager.getComments(authorId as string, postId as string)

		if (!post) {
			return {
				redirect: {
					destination: '/onboarding',
					permanent: false
				}
			}
		}
		return {
			props: {
				post: post,
				comments: comments.comments
			}
	}	
	  }
	  catch {
		return {
			redirect: {
				destination: '/onboarding',
				permanent: false
			}
		}
	  }

	
}

export default Page;



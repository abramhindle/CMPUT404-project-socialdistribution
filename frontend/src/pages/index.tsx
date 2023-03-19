import React from 'react'
import dynamic from 'next/dynamic';
const Post = dynamic(() => import('@/components/Post'), { ssr: false });
import Sidebar from '@/components/Sidebar';
import { Auth } from '@supabase/auth-ui-react'
import {ThemeSupa} from '@supabase/auth-ui-shared'
import { useUser, useSupabaseClient } from '@supabase/auth-helpers-react'
import Head from 'next/head';
import { GetServerSideProps } from 'next';
import { createServerSupabaseClient } from '@supabase/auth-helpers-nextjs';
import axios, { remoteInstance } from '@/utils/axios'
import { Post } from '@/index';



interface streamProps {
	posts: Post[]
}

const Stream: React.FC<streamProps> = ({posts}) => {

	const supabaseClient = useSupabaseClient()
	const user = useUser()

  React.useEffect(() => {
	console.log(posts)
  }, []);

  if (!user)
  return (
	  <div className='container mx-auto mt-12'>
	<Auth
	  redirectTo="http://localhost:3000/"
	  appearance={{ theme: ThemeSupa }}
	  supabaseClient={supabaseClient}
	  socialLayout="horizontal"
	  providers={[]}
	/>
	</div>
  )
		return (
			
			<div className='flex flex-col h-screen'>
				<Head>
					<title>Post Stream</title>
				</Head>
		<div className='flex flex-1 overflow-hidden'>
				<Sidebar/>
		<div className='flex flex-1 flex-col overflow-y-auto w-full py-12'>
			
		<div className='w-full mx-auto bg-white px-6 max-w-4xl'>
			{posts.map((post) => {
				return <Post key={post.id} {...post}/>
			})}
		</div>
		{
			posts.length === 0 && (
				<div className='w-full mx-auto bg-white px-6 max-w-4xl'>
					<div className='flex flex-col items-center justify-center h-full'>
						<h1 className='text-3xl font-bold text-gray-700 mb-3'>No posts yet</h1>
						<p className='text-gray-500'>Follow some users to see their posts</p>
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

	  try {
		await axios.get(`/authors/${user?.id}`)
	  }
	  catch {
		return {
			redirect: {
				destination: '/onboarding',
				permanent: false
			}
		}
	  }

	  let resPosts = await axios.get(`/authors/${user.id}/posts/`, {		// CHANGED: "/posts" to "/posts/"
		params: {
			following: true
		}
	  });

	  let remotePosts = await remoteInstance.get("/authors/80e83b86-0d26-4189-b68a-bf57e8c87af1/posts/");
	//   console.log(remotePosts.data);

	return {
	  props: {
		posts: [...remotePosts.data.items, ...resPosts.data.posts]
	  }
	}
  }


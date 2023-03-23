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
import NodeManager from '@/nodes';
import { InboxListItem, Post } from '@/index';


interface streamProps {
	inbox: InboxListItem
}

const Stream: React.FC<streamProps> = ({inbox}) => {

	const supabaseClient = useSupabaseClient()
	const user = useUser()

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
					<title>Stream</title>
				</Head>
		<div className='flex flex-1 overflow-hidden'>
				<Sidebar/>
		<div className='flex flex-1 flex-col overflow-y-auto w-full py-12'>
			
		<div className='w-full mx-auto bg-white px-6 max-w-4xl'>
			{inbox.items.map((item) => {
				switch (item.type.toLowerCase()) {
					case 'post':
						item = item as Post;
						return <Post {...item} key={item.id} />;
					case 'Follow':
						return null;
					case 'Like':
						return null;
					case 'comment':
						return null;
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
	  
	return {
	  props: {
		inbox
	  }
	}
  }


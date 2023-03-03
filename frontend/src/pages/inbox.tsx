import React from 'react'
import Head from 'next/head'
import { useUser, useSupabaseClient } from '@supabase/auth-helpers-react'
import { Auth } from '@supabase/auth-ui-react'
import {ThemeSupa} from '@supabase/auth-ui-shared'
import { useRouter } from 'next/router'
import SideBar from '@/components/Sidebar'
import InboxItem from '@/components/InboxItem'
import { GetServerSideProps } from 'next'
import { createServerSupabaseClient } from '@supabase/auth-helpers-nextjs'
import axios from '@/utils/axios'

interface inboxProps {

}

const Inbox: React.FC<inboxProps> = ({}) => {
	const supabaseClient = useSupabaseClient();
	const user = useUser();
  	const router = useRouter();

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
		  <title>Profile</title>
	  </Head>
	  
	  <div className='flex flex-1 overflow-hidden'>
	  <SideBar/>
	  <div className='flex flex-1 flex-col overflow-y-auto w-full py-12'>
		
	  <div className='w-full mx-auto bg-white px-6 max-w-5xl'>
	  <h2 className='text-xl font-semibold mb-5'>Inbox</h2>
		<div className='border border-gray-100 rounded-md shadow-sm'>
			<InboxItem type='comment' author={{
				id: '1',
				host: 'https://example.com',
				displayName: 'John Doe',
				url: 'https://example.com',
				github: 'https://github.com',
				profileImage: 'https://i.imgur.com/4Z5ZQ0l.jpg'
			}}	/>
			<InboxItem  type='follow' author={{
				id: '1',
				host: 'https://example.com',
				displayName: 'Jane Doe',
				url: 'https://example.com',
				github: 'https://github.com',
				profileImage: 'https://i.imgur.com/4Z5ZQ0l.jpg'
			}}/>
			<InboxItem type='comment' author={{
				id: '1',
				host: 'https://example.com',
				displayName: 'John Doe',
				url: 'https://example.com',
				github: 'https://github.com',
				profileImage: 'https://i.imgur.com/4Z5ZQ0l.jpg'
			}}	/>
			<InboxItem  type='follow' author={{
				id: '1',
				host: 'https://example.com',
				displayName: 'Jane Doe',
				url: 'https://example.com',
				github: 'https://github.com',
				profileImage: 'https://i.imgur.com/4Z5ZQ0l.jpg'
			}}/><InboxItem type='comment' author={{
				id: '1',
				host: 'https://example.com',
				displayName: 'John Doe',
				url: 'https://example.com',
				github: 'https://github.com',
				profileImage: 'https://i.imgur.com/4Z5ZQ0l.jpg'
			}}	/>
			
		</div>
		</div>
		</div>
		</div>
		</div>
	  );
}
export default Inbox

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
	return {
	  props: {}
	}
  }
import React from 'react'
import dynamic from 'next/dynamic';
const Post = dynamic(() => import('@/components/Post'), { ssr: false });
import Sidebar from '@/components/Sidebar';
import { Auth } from '@supabase/auth-ui-react'
import {ThemeSupa} from '@supabase/auth-ui-shared'
import { useUser, useSupabaseClient } from '@supabase/auth-helpers-react'
import Head from 'next/head';


interface streamProps {

}

const Stream: React.FC<streamProps> = ({}) => {

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
			
			<Post 
				title="My First Post"
				description='This is my first post'
				id='1'
				source='https://i.imgur.com/4Z5ZQ0l.jpg'
				origin='ss'
				content='This is my first post'
				contentType='text/plain'
				count={100}
				comments={'https://comments.example.com/1'}
				categories={['software', 'engineering']}
				author={{
					id: '1',
					host: 'https://example.com',
					displayName: 'John Doe',
					url: 'https://example.com',
					github: 'https://github.com',
					profileImage: 'https://i.imgur.com/4Z5ZQ0l.jpg'
				}}
			
			/>
			<Post 
				title="My Second Post"
				description='This is my second post'
				id='2'
				source='https://i.imgur.com/4Z5ZQ0l.jpg'
				origin='ss'
				content={'# This is my second post\n **You can use markdown**'}
				contentType='text/markdown'
				count={250}
				comments={'https://comments.example.com/1'}
				categories={['software', 'engineering']}
				author={{
					id: '1',
					host: 'https://example.com',
					displayName: 'John Doe',
					url: 'https://example.com',
					github: 'https://github.com',
					profileImage: 'https://i.imgur.com/4Z5ZQ0l.jpg'
				}}
			
			/>
			<Post 
				title="My Third Post"
				description='I love shrek'
				id='3'
				source='https://i.imgur.com/4Z5ZQ0l.jpg'
				origin='ss'
				content={'https://www.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg'}
				contentType='image/link'
				count={250}
				comments={'https://comments.example.com/1'}
				categories={['you', 'suck']}
				author={{
					id: '1',
					host: 'https://example.com',
					displayName: 'John Doe',
					url: 'https://example.com',
					github: 'https://github.com',
					profileImage: 'https://i.imgur.com/4Z5ZQ0l.jpg'
				}}
			
			/>
		</div></div>
		</div></div>);
}
export default Stream


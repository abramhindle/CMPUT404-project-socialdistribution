import React from 'react'
import { GetServerSideProps } from 'next';
import Button from '@/components/Button';
import { NextPage } from 'next';
import Link from 'next/link';
import SideBar from '@/components/Sidebar';
import Post from '@/components/Post';
import { Auth } from '@supabase/auth-ui-react'
import {ThemeSupa} from '@supabase/auth-ui-shared'
import { useUser, useSupabaseClient } from '@supabase/auth-helpers-react'
import Head from 'next/head';
import { GitHub } from 'react-feather';
import { useRouter } from 'next/router';

interface Props {
	id: string;
	host: string;
	displayName: string;
	github: string;
	profileImage: string;
}

const Page: NextPage<Props> = ({id, host, displayName, github, profileImage}) => {
	const supabaseClient = useSupabaseClient()
  	const user = useUser()
	const router = useRouter()

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
			<div className=' max-w-4xl mx-auto px-8'>
			<div className='flex flex-col border-b border-slate-200 pb-6'>
			<img className='rounded-full w-24 h-24 object-cover mb-3 ' src={profileImage} width={100} height={100} alt={displayName}/>
			<div className='flex flex-row items-center justify-between'>
			<div className='text-2xl'>{displayName}</div>
			<div className='flex flex-row space-x-3'><Button name='Follow' className='text-white'/> {<Button name='Edit Profile' onClick={() => {
				router.push('/profile/edit')
			}} className='bg-white text-gray-600 border-2 border-gray-100 hover:bg-gray-50 focus:ring-gray-100'/>}</div>
			</div>
			<div className='text-gray'>
			<Link href={github} >
				<GitHub className='inline-block w-5 h-5 text-gray-500 hover:text-gray-700'/>
			</Link>
			</div>
			</div>
			<div className='my-4'>
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
			</div>
			</div>
			</div>
		</div></div>);
}

export const getServerSideProps:GetServerSideProps = async ({params}) => {
	return {
		props: {
			id: params?.slug || 'abcdedf',
			host: 'https://example.com',
			displayName: 'Tosin Kuye',
			github: 'https://github.com/example',
			profileImage: 'https://a1cf74336522e87f135f-2f21ace9a6cf0052456644b80fa06d4f.ssl.cf2.rackcdn.com/images/characters/large/800/Shrek.Shrek.webp'
		}
	}	
}

export default Page;



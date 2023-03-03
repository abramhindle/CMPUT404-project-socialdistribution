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
import { createServerSupabaseClient } from '@supabase/auth-helpers-nextjs';
import axios from '@/utils/axios';
import { Author, Post as PostType } from '@/index';

interface Props {
	author:Author
	posts: PostType[]
}

const Page: NextPage<Props> = ({author:{id, displayName, github, profileImage}, posts}) => {
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
			<title>Author Profile</title>
		</Head>
		
		<div className='flex flex-1 overflow-hidden'>
		<SideBar/>
		<div className='flex flex-1 flex-col overflow-y-auto w-full py-12'>
			<div className='max-w-4xl w-full mx-auto px-8'>
			<div className='flex flex-col border-b border-slate-200 pb-4'>
			<img className='rounded-full w-24 h-24 object-cover mb-3 ' src={profileImage} width={100} height={100} alt={displayName}/>
			<div className='flex flex-row items-center justify-between'>
			<div className='text-xl font-medium'>{displayName}</div>
			<div className='flex flex-row space-x-3'> 
			{user.id === id ? <Button name='Edit Profile' onClick={() => {
				router.push('/authors/' + id + '/edit')
			}} className='bg-white text-gray-600 border-2 border-gray-100 hover:bg-gray-50 focus:ring-gray-100'/>:<Button name='Friend' className='text-white'/>}</div>
			</div>
			<div className='text-gray'>
			<Link href={github} >
				<GitHub className='inline-block w-5 h-5 text-gray-500 hover:text-gray-700'/>
			</Link>
			</div>
			</div>
			<div className='my-4'>
			{posts.map((post) => {
				return <Post key={post.id} {...post}/>
			})}
			
			</div>
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
		let res = await axios.get(`/authors/${user.id}`);
		let resPosts = await axios.get(`/authors/${user.id}/posts`);
		let author = res.data;
		let posts = resPosts.data.posts;
		
		return {
			props: {
				author: author,
				posts: posts
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



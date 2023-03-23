import React, {useState} from 'react'
import dynamic from "next/dynamic";
import Input from "@/components/Input";
import Button from "@/components/Button";
import Head from 'next/head';
import File from "@/components/File";
import Sidebar from '@/components/Sidebar';
import GitHubUrl from '@/components/GitHubUrl';
import { Auth } from '@supabase/auth-ui-react'
import {ThemeSupa} from '@supabase/auth-ui-shared'
import { useUser, useSupabaseClient } from '@supabase/auth-helpers-react'
import { useForm } from "react-hook-form";
import { GetServerSideProps } from 'next';
import { createServerSupabaseClient } from '@supabase/auth-helpers-nextjs';
import axios from '@/utils/axios'
import { getBase64 } from '@/utils';
import { useRouter } from 'next/router';


interface createProps {
	type: string;
	id: string;
	host: string;
	displayName: string;
	github: string;
	profileImage: string;
}

const Create: React.FC<createProps> = ({displayName, github, profileImage}) => {

	const supabaseClient = useSupabaseClient()
  	const user = useUser()
	const router = useRouter()
	const { register, handleSubmit, watch, formState: { errors } } = useForm({
		defaultValues: {
			displayName,
			github,
			profile: new Blob([profileImage], {type: 'image/png'})
		}
	})

	const onSubmit = async (data:any) => {
		if (data.profile && data.profile.length > 0) {
			data.profileImage = await getBase64(data.profile[0])
		}
		
        data.id = user?.id
        data.github = 'https://github.com/' + data.github
        delete data.profile
        try {
           let res =  await axios.put(`/authors/${user?.id}`, data)
            router.push(`/authors/${user?.id}`)
        } catch (error) {
            console.log(error)
        }
	}

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
		return (<div className='flex flex-col h-screen'>
		<Head>
			<title>Edit Profile</title>
		</Head>
		<div className='flex flex-1 overflow-hidden'>
		<Sidebar/>
		<div className=' overflow-y-auto w-full py-12'>
		<form className='max-w-5xl mx-auto px-8' onSubmit={handleSubmit(onSubmit)}>
			<h2 className='text-xl font-semibold mb-5'>Edit Profile</h2>
			<Input register={register} extraClass='mb-6' id="displayName" name="Display Name" placeholder="John Doe" required={true}/>
			<span className='block mb-2 text-sm font-medium'>GitHub</span>
			<GitHubUrl register={register} extraClass='mb-6' id="github" placeholder="github" required={false}/>
			<span className='block mb-2 text-sm font-medium'>Profile Picture</span>
			<File register={register} id="profile" filePreviewClass="w-44 h-44 object-cover rounded-full" required={false}/>
			<Button name="Edit Profile" className='text-white'/>
		</form>
		</div>
		</div>
		</div>);
}
export default dynamic(() => Promise.resolve(Create), { ssr: false });

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
		let res = await axios.get(`/authors/${user?.id}`)
		let data = res.data
		if (data.github) {
			data.github = data.github.replace('https://github.com/', '')
		}
		return {
			props: data
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
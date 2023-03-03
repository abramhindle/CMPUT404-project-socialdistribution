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

const MDEditor = dynamic(
	() => import("@uiw/react-md-editor"),
	{ ssr: false }
  );
interface createProps {

}

const Create: React.FC<createProps> = ({}) => {
	const [selectValue, setSelectValue] = useState<string>("text/plain");
	const [markDownValue, setMarkDownValue] = useState<string | undefined>("");
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
		return (<div className='flex flex-col h-screen'>
		<Head>
			<title>Edit Profile</title>
		</Head>
		<div className='flex flex-1 overflow-hidden'>
		<Sidebar/>
		<div className=' overflow-y-auto w-full py-12'>
		<form className='max-w-5xl mx-auto px-8'>
			<h1 className='text-2xl mb-4 font-medium'>Edit Profile</h1>
			<Input extraClass='mb-6' id="name" name="Display Name" placeholder="John Doe" required={true}/>
			<span className='block mb-2 text-sm font-medium'>GitHub</span>
			<GitHubUrl extraClass='mb-6' id="github" placeholder="github" required={false}/>
			<span className='block mb-2 text-sm font-medium'>Profile Picture</span>
			<File id="profile" />
			<Button name="Edit Profile" className='text-white'/>
			
		</form></div></div></div>);
}
export default Create
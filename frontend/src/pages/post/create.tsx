import React, {useState} from 'react'
import dynamic from "next/dynamic";
import TextArea from "@/components/Textarea";
import Input from "@/components/Input";
import Button from "@/components/Button";
import Head from 'next/head';
import File from "@/components/File";
import Sidebar from '@/components/Sidebar';
import Select from "@/components/Select";
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
			<title>Create Post</title>
		</Head>
		<div className='flex flex-1 overflow-hidden'>
		<Sidebar/>
		<div className=' overflow-y-auto w-full py-12'>
		<form className='max-w-5xl mx-auto px-8'>
			<h1 className='text-2xl mb-4 font-medium'>Create Post</h1>
			<Input extraClass='mb-6' id="title" name="Title" placeholder="Enter a title" required={true}/>
			<TextArea id="description" name="Description" placeholder="Enter a description"/>
			<Select id="contentType" name="Post Type" value={
				selectValue
			} 
				setValue={setSelectValue}
			options={[{
				name: "Markdown",
				value: "text/markdown"
			}, {
				name: "Plain Text",
				value: "text/plain"
			}, {
				name: "Image",
				value: "image/*"
			}, {
				name: "Image Link",
				value: "image/link"
			}]}/>
			<div className='mb-2'>
			{selectValue === "image/*" && <File id="file" />}
			{selectValue === "image/link" && <Input extraClass='mb-6' id="imageLink" name="Image Link" placeholder="Enter an image link"/>}
			{selectValue === "text/markdown" && <><MDEditor style={{ minWidth: 480 }} value={markDownValue} onChange={setMarkDownValue}/>
			</>}
			{selectValue === "text/plain" && <TextArea id="content" name="Content" placeholder="Enter content"/>}
			</div>
			<div className='mb-6'>
			
			<Input extraClass='mb-4' id="categories" name="Categories" placeholder="Enter categories, seperated via comma. " required={true}/>
			<span className="block text-sm font-medium text-gray-900 dark:text-white">Post Visibility</span>
			<Select
				id="visibility"
				name={"Post Visibility"}
			options={
				[{
					name: "Public",
					value:"PUBLIC"
				}, {
					name: "Private",
					value:"PRIVATE"
				}, {
					name: "Unlisted",
					value:"UNLISTED"
				}]
			}/>
			</div>
			<Button name="Create Post" className="text-white"/>
			
		</form></div></div></div>);
}
export default Create
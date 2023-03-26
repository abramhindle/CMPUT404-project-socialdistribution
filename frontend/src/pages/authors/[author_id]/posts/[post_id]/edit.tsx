import React, {useState, useEffect} from 'react'
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
import { useForm, FormProvider } from "react-hook-form";
import { getBase64 } from '@/utils';
import NodeManager from '@/nodes';
import { useRouter } from 'next/router';
import { GetServerSideProps } from 'next';
import { createServerSupabaseClient } from '@supabase/auth-helpers-nextjs';
import { Post } from '@/index';
const MDEditor = dynamic(
	() => import("@uiw/react-md-editor"),
	{ ssr: false }
  );

interface createProps {
    post: Post
	authorId: string;
	postId: string;
}



const Edit: React.FC<createProps> = ({post, postId, authorId}) => {
	const [selectValue, setSelectValue] = useState<string>(post.contentType);
	const [markDownValue, setMarkDownValue] = useState<string | undefined>(
        post.contentType === 'text/markdown' ? post.content : undefined
    )
	const form= useForm({
        defaultValues: {
            title: post.title,
            description:post.description,
            categories: post.categories.join(','),
            contentType: post.contentType,
            visibility: post.visibility ? 'PUBLIC' : post.unlisted ? 'UNLISTED' : 'PRIVATE',
            content: post.content,

        }
    })
	const supabaseClient = useSupabaseClient()
  	const user = useUser()
	const router = useRouter()


	const onSubmit = async (data:any) => {
		if (data.contentType === 'text/markdown') {
			data.content = markDownValue
		}
		else if (data.contentType === 'image/*') {
			data.content = await getBase64(data.contentFile[0])
			
		}

		if (data.contentFile){
			delete data.contentFile
		}

		data.categories = data.categories.split(',')

		try {
			
			let post = {
				...data,
				source: process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000',
				origin: process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000',
				unlisted: data.visibility === 'UNLISTED',
				visibility: data.visibility,
			}

			let updatedPost = await NodeManager.updatePost(authorId, postId, post)
			if (updatedPost) {
				await NodeManager.alertNewPost(authorId, post)
			}
		
			console.log(`/authors/${authorId}/posts/${postId}`)
		await router.push(`/authors/${authorId}/posts/${postId}`)
		} catch (error) {
			console.log(error)
		}
		

		
		
}


		return (<div className='flex flex-col h-screen'>
		<Head>
			<title>Edit Post</title>
		</Head>
		<div className='flex flex-1 overflow-hidden'>
		<Sidebar/>
		<div className='overflow-y-auto w-full py-12'>
		<FormProvider {...form}>
		<form className='max-w-5xl mx-auto px-8' onSubmit={form.handleSubmit(onSubmit)}>
			<h2 className='text-xl font-semibold mb-5'>Edit Post</h2>
			<Input 
				register={form.register}
			extraClass='mb-6' id="title" name="Title" placeholder="Enter a title" required={true}/>
			<TextArea 
				register={form.register}
			id="description" name="Description" placeholder="Enter a description"/>

			<Select 
				register={form.register}
			id="contentType" name="Post Type" value={
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
			{selectValue === "image/*" && <File register={form.register} id="contentFile" />}
			{selectValue === "image/link" && <Input
				register={form.register}
			extraClass='mb-6' id="content" name="Image Link" placeholder="Enter an image link"/>}
			{selectValue === "text/markdown" && <><MDEditor style={{ minWidth: 480 }} value={markDownValue} onChange={setMarkDownValue}/>
			</>}
			{selectValue === "text/plain" && <TextArea
				register={form.register}
			id="content" name="Content" placeholder="Enter content"/>}
			</div>
			<div className='mb-6'>
			
			<Input
				register={form.register}
			extraClass='mb-4' id="categories" name="Categories" placeholder="Enter categories, seperated via comma. " required={true}/>
			<span className="block text-sm font-medium text-gray-900 dark:text-white">Post Visibility</span>
			<Select
				register={form.register}
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
			<Button name="Edit Post" className="text-white"/>
			
		</form>
		</FormProvider>
		</div></div></div>);
}
export default Edit

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
	  
	
	let  authorId = context.params?.author_id as string
	let postId = context.params?.post_id as string

	  if (!authorId.includes(user.id)) {
		return {
		  redirect: {
			destination: '/',
			permanent: false
		  }
	  }
	}

    let post = await NodeManager.getPost(authorId, postId) 

	if (!post) {
		return {
			notFound: true
		}
	}
  
	return {
	  props: {
		postId,
		authorId,
        post: post
      }
	}
  }
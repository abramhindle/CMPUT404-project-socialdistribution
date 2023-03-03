import Link from 'next/link';
import React from 'react'
import {Inbox, Home, User, FilePlus, LogOut, Search} from 'react-feather'
import { Tooltip} from "@material-tailwind/react";
import {  useSupabaseClient } from '@supabase/auth-helpers-react'
import { useRouter } from 'next/router';
interface sidebarProps {

}

const Sidebar: React.FC<sidebarProps> = ({}) => {
	const supabaseClient = useSupabaseClient();
	const router = useRouter();
		return (
		<div className='flex flex-col justify-between items-center w-16 h-screen border-r border-gray-100 '>
			<div className='flex  flex-col space-y-3'>
			<Link href='/'>
			<Tooltip placement="right" content="Home">
			<Home className={`w-6 h-6 mx-auto mt-4 text-gray-500 hover:text-gray-700 ${router.asPath === '/'? 'text-gray-800':''}`}/>
			</Tooltip>
			</Link>
			<Link href='/post/create'>
			<Tooltip placement="right" content="Create Post">
			<FilePlus className={`w-6 h-6 mx-auto mt-4 text-gray-500 hover:text-gray-700 ${router.asPath === '/post/create'? 'text-gray-800':''}`}/>
			</Tooltip>
			</Link>
			<Link href='/inbox'>
			<Tooltip placement="right" content="Inbox">
			<Inbox className={`w-6 h-6 mx-auto mt-4 text-gray-500 hover:text-gray-700 ${router.asPath === '/inbox'? 'text-gray-800':''}`}/>
			</Tooltip>
			</Link>
			<Link href='/search'>
			<Tooltip placement="right" content="Search">
			<Search className={`w-6 h-6 mx-auto mt-4 text-gray-500 hover:text-gray-700 ${router.asPath === '/search'? 'text-gray-800':''}`}/>
			</Tooltip>
			</Link>
			<Link href='/profile/1212'>
			<Tooltip placement="right" content="Profile">
			<User className={`w-6 h-6 mx-auto mt-4 text-gray-500 hover:text-gray-700 ${router.asPath.includes('/profile') ? 'text-gray-800':''}`}/>
			</Tooltip>
			</Link>
			</div>
			<div className=''>
			<Tooltip placement="right" content="Logout">
			<LogOut onClick={async () => {
    		let err=	await supabaseClient.auth.signOut();
			console.log(err)
    			router.push('/')
  }} className='w-6 h-6 mx-auto mb-8 text-gray-500 hover:text-gray-700 cursor-pointer'/>
			</Tooltip>
		</div>
		</div>
		);
}
export default Sidebar
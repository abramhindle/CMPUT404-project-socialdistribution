/* eslint-disable @next/next/no-img-element */
import React from 'react'
import {Author} from '@/index'
import {useRouter} from 'next/router'
interface ProfilePreviewProps {
    author: Author;
}

const ProfilePreview: React.FC<ProfilePreviewProps> = ({author}) => {
    const router = useRouter()
    const goToProfile = () => {
        // check if id is url
        if (author.id.startsWith('http')) {
            // get end of url
            const id = author.id.split('/').pop()
            router.push(`/authors/${id}`)
        } else {
            router.push(`/authors/${author.id}`)
        }
    }
        return (<div className='hover:bg-gray-50 cursor-pointer'
        onClick={goToProfile}
        >
            <div className='flex flex-row items-center border p-3 w-full space-x-3 rounded-lg'>
                <img src={author.profileImage} alt={author.displayName} className='w-20 h-20 rounded-full'/>
                <div className='text-lg font-medium'>{author.displayName}</div>
            </div>
        </div>);
}
export default ProfilePreview
import React from 'react'
import Search from '@/components/Search';
import { Auth } from '@supabase/auth-ui-react'
import {ThemeSupa} from '@supabase/auth-ui-shared'
import { useUser, useSupabaseClient } from '@supabase/auth-helpers-react'
interface searchProps {

}

const SearchPage: React.FC<searchProps> = ({}) => {
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
	
		return (<div className='mb-8 '>
		<Search id='stream-search' placeholder='Search for user...'/>
		</div>);
}
export default SearchPage;
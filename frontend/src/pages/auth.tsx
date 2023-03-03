import React from 'react'
import { Auth } from '@supabase/auth-ui-react'
import {ThemeSupa} from '@supabase/auth-ui-shared'
import { useUser, useSupabaseClient } from '@supabase/auth-helpers-react'
interface loginProps {

}

const AuthPage: React.FC<loginProps> = ({}) => {
    const supabaseClient = useSupabaseClient()
    return (
        <div className='container mx-auto mt-12'>
      <Auth
        redirectTo="/"
        appearance={{ theme: ThemeSupa }}
        supabaseClient={supabaseClient}
        socialLayout="horizontal"
        providers={[]}
      />
      </div>
    )
}
export default AuthPage;
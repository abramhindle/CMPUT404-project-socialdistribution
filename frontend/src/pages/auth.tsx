import React, {useEffect} from 'react'
import { Auth } from '@supabase/auth-ui-react'
import {ThemeSupa} from '@supabase/auth-ui-shared'
import { useUser, useSupabaseClient } from '@supabase/auth-helpers-react'
import { createServerSupabaseClient } from '@supabase/auth-helpers-nextjs'
import { GetServerSideProps } from 'next'
import { useRouter } from 'next/router'
interface loginProps {

}

const AuthPage: React.FC<loginProps> = ({}) => {
    const supabaseClient = useSupabaseClient()
    const user = useUser()
    const router = useRouter()

    useEffect(() => {
        if (user) {
            router.push('/')
        }
    }, [user, router])

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
}
export default AuthPage;

export const getServerSideProps:GetServerSideProps = async (context) => {
  
      const supabaseServerClient = createServerSupabaseClient(context)
        const {
          data: { user },
        } = await supabaseServerClient.auth.getUser();
  
        if (!user) {
          return {
            props: {},
          };
        }
  
        return {
          redirect: {
            destination: '/',
            permanent: false,
          },
        };
}
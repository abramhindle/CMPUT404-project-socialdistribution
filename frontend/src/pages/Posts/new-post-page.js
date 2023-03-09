import Sidebar from "../../components/Sidebar/sidebar";
import NewPost from "../../components/Posts/new-post";
import './posts.css'

function Posts() {
    return (
        <div className='Page'>
        <Sidebar/>
        <div className='Fragment'>
          <p>
              This is now the new post creation page
          </p>
          <NewPost/>
        </div>
      </div>
    
    );
}

export default Posts;
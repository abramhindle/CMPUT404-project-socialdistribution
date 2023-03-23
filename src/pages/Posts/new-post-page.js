import Sidebar from "../../components/Sidebar/sidebar";
import NewPost from "../../components/ItemDisplay/new-post";
import '../pages.css'
import './posts.css'

function Posts() {
    return (
        <div className='Page'>
        <Sidebar/>
        <div className='Fragment sidebar-offset'>
          <p>
              This is now the new post creation page
          </p>
          <NewPost/>
        </div>
      </div>
    
    );
}

export default Posts;
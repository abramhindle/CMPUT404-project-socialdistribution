import Sidebar from "../../components/Sidebar/sidebar";
import NewPost from "../../components/ItemDisplay/new-post";
import '../pages.css'
import './posts.css'

function Posts(props) {
    return (
        <div className='Page'>
        <Sidebar/>
        <div className='Fragment sidebar-offset'>
          <NewPost/>
        </div>
      </div>
    
    );
}

export default Posts;
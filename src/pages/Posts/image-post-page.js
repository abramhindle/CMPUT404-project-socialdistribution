import '../pages.css'
import './posts.css'
import Sidebar from "../../components/Sidebar/sidebar";
import ImageUpload from "../../components/ItemDisplay/image-upload";

export default function ImagePost() {
    return (
        <div className='Page'>
        <Sidebar/>
        <div className='Fragment sidebar-offset'>
          <p>
              This is the image post creation page
          </p>
          <ImageUpload/>
        </div>
      </div>
    
    );
};
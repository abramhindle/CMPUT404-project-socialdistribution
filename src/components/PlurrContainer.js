import React from 'react'
import { Image, Ratio } from 'react-bootstrap';
import { Link } from 'react-router-dom'; 
import CreatePostModal from '../components/CreatePostModal';
import './PlurrContainer.css'
import { useHistory, useLocation } from "react-router-dom"
import { useUserHandler } from "../UserContext"

// sidebar code adapted from https://startbootstrap.com/template/simple-sidebar
function PlurrContainer ({children})  {
  const { loggedInUser, setLoggedInUser } = useUserHandler()
  const [modalShowCreatePost, setModalShowCreatePost] = React.useState(false);

  // redirect away from PlurrContainer with useHistory
  const history = useHistory()

  const location = useLocation();
  const currentPath = location.pathname;

  const getInitialSidebarState = () => {
    if (localStorage.getItem('sb|sidebar-toggle') === 'false') {
      document.body.classList.add('sb-sidenav-toggled');
    } else {
      document.body.classList.remove('sb-sidenav-toggled');
    }
  }
  
  const toggleSidebar = () => {
    if (localStorage.getItem('sb|sidebar-toggle') === 'false') {
      document.body.classList.remove('sb-sidenav-toggled');
      localStorage.setItem('sb|sidebar-toggle', 'true');
    } else {
      document.body.classList.add('sb-sidenav-toggled');
      localStorage.setItem('sb|sidebar-toggle', 'false');
    }
  }

  const handleLogout = React.useCallback(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("refresh");
    history.push(`/`);
  }, [history])

  React.useEffect(() => {
    if ((localStorage.getItem('token') !== null) 
      && (localStorage.getItem('user') !== null)
      && (localStorage.getItem('refresh') !== null)) {
        setLoggedInUser(JSON.parse(localStorage.getItem('user')));
      } else {
        if (!((localStorage.getItem('token') === null) 
        && (localStorage.getItem('user') === null)
        && (localStorage.getItem('refresh') === null))) {
          setTimeout(() => {
            // alert the user that they are logged out
            alert("You session has ended. Please log in again.")
          }, 500)
        }
        handleLogout()
      }
  }, [setLoggedInUser, history, handleLogout]);

  React.useEffect(() => {
    getInitialSidebarState()
    
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
      sidebarToggle.addEventListener('click', event => {
        event.preventDefault();
        
        toggleSidebar();
          
      });
    }

  }, []);
  
  return (
    <React.Fragment>      
        <div className="d-flex" id="wrapper">
            <div id="sidebar-wrapper" style={{backgroundColor: "#1A1B1F", 
              height: "100vh", fontWeight: "600", color: "#EDEDED"}}>
                  <Ratio aspectRatio='1x1' 
                    className='w-75 mb-4' style={{margin: "72px auto 0"}}>
                      <Image className='fluid' 
                        src={loggedInUser?.profileImage} 
                        roundedCircle style={{objectFit: "cover", 
                          backgroundColor: "#EEE"}} />
                  </Ratio>
                  <h3 className='mb-4 text-center'>
                      {loggedInUser?.displayName}
                  </h3>
                  <div className="list-group list-group-flush" >
                      <Link className={`plurr-nav-item 
                        ${(currentPath === "/stream" ? "active" : "")}`} 
                        to="/stream">Stream</Link>
                      <div className="plurr-nav-item" 
                      onClick={() => setModalShowCreatePost(true)}> Create Post</div>
                                                      <CreatePostModal
                                    show={modalShowCreatePost}
                                    onHide={() => setModalShowCreatePost(false)}
                                    closeModal={() => setModalShowCreatePost(false)}
                                />
                      <Link className={`plurr-nav-item 
                        ${(currentPath === `/author/${loggedInUser?.uuid}` ? "active" : "")}`}
                        to={`/author/${loggedInUser?.uuid}`}>Profile</Link>
                      <div className="plurr-nav-item" 
                        onClick={() => {handleLogout()}}>Logout</div>
                  </div>
            </div>
            <div id="page-content-wrapper" 
              style={{backgroundColor: "#f7f7f9"}}>
                <nav 
                  className="navbar navbar-light bg-light border-bottom" 
                  style={{height: "57px"}}>
                    <div className="container-fluid">
                        <button 
                          className="navbar-toggler" id="sidebarToggle" type="button" 
                          data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" 
                          aria-controls="navbarSupportedContent" aria-expanded="false" 
                          aria-label="Toggle navigation">
                            <span className="navbar-toggler-icon"></span>
                        </button>
                    </div>
                </nav>
                <div className="pt-5" 
                  style={{margin: "0 auto", 
                    maxHeight: "calc(100vh - 57px)", overflowY: "auto"}}>
                      <div className="container" style={{maxWidth: "1024px"}}>
                          {children}
                        </div>
                </div>
            </div>
        </div>
      </React.Fragment>
  );
}

export default PlurrContainer;

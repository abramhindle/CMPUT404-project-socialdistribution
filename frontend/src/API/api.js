/*
 * Description: Define the URL path for api caller function
 */
const author = localStorage.getItem("author")
console.log("author", author)
const api = {
    //create post 
    
    createPost: '/api/authors/'+author.local_id+'/posts/',



}

export default api
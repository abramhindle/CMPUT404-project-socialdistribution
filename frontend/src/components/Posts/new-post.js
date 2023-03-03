import { useSelector } from "react-redux";
import { post_api } from "../../api/post_display_api";
import { useState } from "react";

export default function NewPost() {
    //Get user info
    const user = useSelector((state) => state.user);

    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [contentType, setContentType] = useState("text/plain");
    const [body, setBody] = useState("");
    const [visibility, setVisibility] = useState("");
    const [unlisted, setUnlisted] = useState(false);
    const [categories, setCategories] = useState([]);

    const [success, setSucess] = useState(null);

    const submit = async (e) => {
        let post = {"title": title,
                    "description": description,
                    "contentType": contentType,
                    "content": body,
                    "visibility": visibility,
                    "unlisted": unlisted,
                    "categories": categories};
        e.preventDefault();
        console.log(user.displayName, "is attempting to post", post);
        post_api(user.id, post, onSuccess, onFailure);
    };

    //For confirmation dialogs
    const onSuccess = () => {
        setSucess(true);
    }
    const onFailure = () => {
        setSucess(false);
    }

    /*EXAMPLE
    {
        "title": "This is my post!",
        "description": "this is a description",
        "contentType": "text/markdown",
        "content": "this is the content body",
        "visibility": "PUBLIC",
        "unlisted": false,
        "categories": ["web", "design"]
    }*/

    return (
        <div>
            <form justify-self="center">
                <label>Title</label><br/>
                <input
                    placeholder="Title.."
                    name="title"
                    type="text"
                    value={title}
                    required
                    onChange={(e) => setTitle(e.target.value)}
                /><br/>
                <label>Description</label><br/>
                <input
                    placeholder="Description.."
                    name="description"
                    type="text"
                    value={description}
                    required
                    onChange={(e) => setDescription(e.target.value)}
                /><br/>
                <label>Content Type: </label>
                    <input
                        name="type"
                        type="radio"
                        value="text/plain"
                        required
                        onChange={(e) => setContentType(e.target.value)}/>
                     Plain Text
                    <input
                        name="type"
                        type="radio"
                        value="text/markdown"
                        required
                        onChange={(e) => setContentType(e.target.value)}/>
                     Markdown
                     <br/>
                <label>Body</label><br/>
                    <input
                    placeholder="Content.."
                    name="content"
                    type="text"
                    value={body}
                    required
                    onChange={(e) => setBody(e.target.value)}
                /><br/>
                
                <label>Visibility</label><br/>
                Public
                    <input
                        name="visibility"
                        type="radio"
                        value="PUBLIC"
                        required
                        onChange={(e) => setVisibility(e.target.value)}
                    /><br/>
                Friends Only
                    <input
                            name="visibility"
                            type="radio"
                            value="FRIENDS"
                            required
                            onChange={(e) => setVisibility(e.target.value)}
                        /><br/>
                
                <label>Unlisted</label>
                <input
                    name="unlisted"
                    type="checkbox" 
                    checked={false}
                    onChange={(e) => setUnlisted(e.target.value)}
                /><br/>
                <label>Categories</label><br/>
                <input
                    placeholder="Categories.."
                    name="categories"
                    type="text"
                    value={categories}
                    required
                    onChange={(e) => setCategories(e.target.value)}
                /><br/>
                <button type="submit" onClick={submit}>Submit</button>
            </form>
        </div>

    );
}